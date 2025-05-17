import sys
import json
from deepface import DeepFace

if len(sys.argv) < 3:
    print(json.dumps({"error": "Image paths not provided"}))
    sys.exit(1)

reference_img_path = sys.argv[1]  # Reference image path from argument
img_path = sys.argv[2]            # Target image path from argument

try:
    result = DeepFace.verify(img1_path=reference_img_path, img2_path=img_path, enforce_detection=False)
    print(json.dumps({
        "verified": result['verified'],
        "distance": result['distance']
    }))
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
