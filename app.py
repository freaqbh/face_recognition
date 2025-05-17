from flask import Flask, request, jsonify, render_template
from deepface import DeepFace
import numpy as np
import cv2
import base64
import tempfile
import os
from firebase_config import db

app = Flask(__name__)

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

        result = DeepFace.verify(ref_file.name, tgt_file.name, enforce_detection=False)

        db.collection("face_matches").add({
            "user": user_id,
            "distance": result['distance'],
            "verified": result['verified']
        })

        return jsonify(result)

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
