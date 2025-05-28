from flask import Flask, request, jsonify, render_template
from deepface import DeepFace
import numpy as np
import cv2
import base64
import tempfile
import os
import logging 

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

SUPPORTED_DETECTORS = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe', 'yolov8', 'yunet']
SUPPORTED_MODELS = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace']
REFERENCE_IMAGE_PATH = "reference_temp.jpg" # Path gambar referensi

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/face_matching")
def faceMatching():
    return render_template("faceMatching.html")

@app.route("/realtime")
def realtime():
    return render_template("realTimeRecognition.html")

@app.route("/match", methods=["POST"])
def match_faces():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    ref_img_data = data.get('ref_img')
    target_img_data = data.get('target_img')
    user_id = data.get('user_id', 'anonymous')
    detector = data.get('detector_backend', 'opencv')
    model = data.get('model_name', 'VGG-Face')

    if not ref_img_data or not target_img_data:
        return jsonify({"error": "Missing image data"}), 400
    
    ref_img_data = ref_img_data.split(',')[-1]
    target_img_data = target_img_data.split(',')[-1]

    if detector not in SUPPORTED_DETECTORS:
        return jsonify({"error": f"Detector model '{detector}' not supported."}), 400
    if model not in SUPPORTED_MODELS:
        return jsonify({"error": f"Recognition model '{model}' not supported."}), 400

    temp_files_to_remove = []
    try:
        ref_img_bytes = base64.b64decode(ref_img_data)
        target_img_bytes = base64.b64decode(target_img_data)

        ref_arr = np.frombuffer(ref_img_bytes, np.uint8)
        target_arr = np.frombuffer(target_img_bytes, np.uint8)

        ref_img = cv2.imdecode(ref_arr, cv2.IMREAD_COLOR)
        target_img = cv2.imdecode(target_arr, cv2.IMREAD_COLOR)

        if ref_img is None or target_img is None:
            return jsonify({"error": "Could not decode one or both images"}), 400

        ref_file_path = None
        tgt_file_path = None

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as ref_temp_file:
            cv2.imwrite(ref_temp_file.name, ref_img)
            ref_file_path = ref_temp_file.name
            temp_files_to_remove.append(ref_file_path)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tgt_temp_file:
            cv2.imwrite(tgt_temp_file.name, target_img)
            tgt_file_path = tgt_temp_file.name
            temp_files_to_remove.append(tgt_file_path)

        result = DeepFace.verify(
            img1_path=ref_file_path, 
            img2_path=tgt_file_path, 
            enforce_detection=False,
            detector_backend=detector,
            model_name=model
        )
        
        return jsonify(result)

    except base64.binascii.Error:
        return jsonify({"error": "Invalid base64 string"}), 400
    except Exception as e:
        app.logger.error(f"Error in /match: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        for f_path in temp_files_to_remove:
            if os.path.exists(f_path):
                os.remove(f_path)

@app.route("/upload", methods=["POST"])
def upload_ref():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    ref_file = request.files['file']
    if ref_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Simpan sebagai REFERENCE_IMAGE_PATH
        ref_file.save(REFERENCE_IMAGE_PATH)
        app.logger.info(f"Reference image saved to {REFERENCE_IMAGE_PATH}")
        return jsonify({"message": "Reference image uploaded successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error saving reference image: {e}")
        return jsonify({"error": f"Could not save reference image: {str(e)}"}), 500

@app.route("/realtime_verify", methods=["POST"])
def realtime_verify():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    frame_data_url = data.get('frame_data')
    detector = data.get('detector_backend', 'opencv')
    model = data.get('model_name', 'VGG-Face')

    if not frame_data_url:
        return jsonify({"error": "Missing frame_data"}), 400

    if not os.path.exists(REFERENCE_IMAGE_PATH):
        app.logger.error(f"Reference image not found at {REFERENCE_IMAGE_PATH}")
        return jsonify({"error": "Reference image not uploaded or found. Please upload one first."}), 400

    if detector not in SUPPORTED_DETECTORS:
        return jsonify({"error": f"Detector model '{detector}' not supported."}), 400
    if model not in SUPPORTED_MODELS:
        return jsonify({"error": f"Recognition model '{model}' not supported."}), 400

    temp_frame_file_path = None
    try:
        # Decode frame dari data URL
        frame_b64_data = frame_data_url.split(',')[-1]
        frame_bytes = base64.b64decode(frame_b64_data)
        frame_arr = np.frombuffer(frame_bytes, np.uint8)
        current_frame_img = cv2.imdecode(frame_arr, cv2.IMREAD_COLOR)

        if current_frame_img is None:
            return jsonify({"error": "Could not decode frame image"}), 400

        # Simpan frame sementara
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_frame_file:
            cv2.imwrite(temp_frame_file.name, current_frame_img)
            temp_frame_file_path = temp_frame_file.name
        
        app.logger.info(f"Verifying: Ref='{REFERENCE_IMAGE_PATH}', Target='{temp_frame_file_path}', Detector='{detector}', Model='{model}'")
        
        result = DeepFace.verify(
            img1_path=REFERENCE_IMAGE_PATH, 
            img2_path=temp_frame_file_path, 
            enforce_detection=False,
            detector_backend=detector,
            model_name=model
        )
    
        return jsonify(result)

    except base64.binascii.Error:
        return jsonify({"error": "Invalid base64 string for frame_data"}), 400
    except Exception as e:
        app.logger.error(f"Error in /realtime_verify: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if temp_frame_file_path and os.path.exists(temp_frame_file_path):
            os.remove(temp_frame_file_path)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000) # Jalankan di port 5000
