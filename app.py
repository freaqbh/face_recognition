from flask import Flask, request, jsonify, render_template
from deepface import DeepFace
import numpy as np
import cv2
import base64
import tempfile
import os
from firebase_config import db

app = Flask(__name__)

# Daftar model yang didukung (untuk validasi jika diperlukan)
SUPPORTED_DETECTORS = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe', 'yolov8', 'yunet']
SUPPORTED_MODELS = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace']

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
    ref_img_data = data['ref_img'].split(',')[-1]
    target_img_data = data['target_img'].split(',')[-1]
    user_id = data.get('user_id', 'anonymous')
    
    # Ambil nama model dari request, gunakan default jika tidak ada
    detector = data.get('detector_backend', 'opencv')
    model = data.get('model_name', 'VGG-Face')

    # (Opsional) Validasi apakah model didukung
    if detector not in SUPPORTED_DETECTORS:
        return jsonify({"error": f"Detector model '{detector}' not supported."}), 400
    if model not in SUPPORTED_MODELS:
        return jsonify({"error": f"Recognition model '{model}' not supported."}), 400

    ref_img_bytes = base64.b64decode(ref_img_data)
    target_img_bytes = base64.b64decode(target_img_data)

    ref_arr = np.frombuffer(ref_img_bytes, np.uint8)
    target_arr = np.frombuffer(target_img_bytes, np.uint8)

    ref_img = cv2.imdecode(ref_arr, cv2.IMREAD_COLOR)
    target_img = cv2.imdecode(target_arr, cv2.IMREAD_COLOR)

    ref_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tgt_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")

    try:
        ref_file.close()
        tgt_file.close()

        cv2.imwrite(ref_file.name, ref_img)
        cv2.imwrite(tgt_file.name, target_img)

        # Gunakan model yang dipilih dalam DeepFace.verify
        result = DeepFace.verify(
            ref_file.name, 
            tgt_file.name, 
            enforce_detection=False,
            detector_backend=detector, # Gunakan model detektor yang dipilih
            model_name=model           # Gunakan model pengenalan yang dipilih
        )

        db.collection("face_matches").add({
            "user": user_id,
            "distance": result['distance'],
            "verified": result['verified'],
            "detector": detector, # Simpan model yang digunakan
            "model": model        # Simpan model yang digunakan
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        os.remove(ref_file.name)
        os.remove(tgt_file.name)

@app.route("/upload", methods=["POST"])
def upload_ref():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    ref_file = request.files['file']
    ref_file.save("reference_temp.jpg")
    return jsonify({"message": "Reference image uploaded successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)