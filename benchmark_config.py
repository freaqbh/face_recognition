"""
Benchmark Configuration File
============================
Customize your benchmark settings here.
"""

# Quick benchmark settings (for fast testing)
QUICK_DETECTORS = ['opencv', 'mtcnn', 'retinaface']
QUICK_MODELS = ['VGG-Face', 'Facenet', 'ArcFace']

# Full benchmark settings (comprehensive testing)
FULL_DETECTORS = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe', 'yolov8', 'yunet']
FULL_MODELS = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace']

# Performance-focused benchmark (balanced speed and accuracy)
PERFORMANCE_DETECTORS = ['opencv', 'mtcnn', 'retinaface', 'mediapipe']
PERFORMANCE_MODELS = ['VGG-Face', 'Facenet', 'Facenet512', 'ArcFace']

# Speed-focused benchmark (fastest combinations)
SPEED_DETECTORS = ['opencv', 'mediapipe']
SPEED_MODELS = ['VGG-Face', 'OpenFace']

# Accuracy-focused benchmark (most accurate combinations)
ACCURACY_DETECTORS = ['mtcnn', 'retinaface']
ACCURACY_MODELS = ['Facenet512', 'ArcFace']