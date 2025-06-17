#!/bin/bash
# Face Recognition Benchmark Setup and Usage Script
# This script helps set up the benchmark environment and provides usage examples

set -e

echo "=== Face Recognition Benchmark Setup ==="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create benchmark directory structure
echo "Creating benchmark directory structure..."
mkdir -p benchmark_data/test_images
mkdir -p benchmark_results

# Install requirements if they don't exist
if [ ! -f "benchmark_requirements.txt" ]; then
    echo "Error: benchmark_requirements.txt not found!"
    echo "Please ensure the requirements file is in the current directory."
    exit 1
fi

echo "Installing benchmark requirements..."
pip3 install -r benchmark_requirements.txt

# Create sample test data structure guide
cat > benchmark_data/README.md << 'EOF'
# Test Data Structure

Your test images should be organized as follows:

```
test_images/
├── person1/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
├── person2/
│   ├── image1.jpg
│   └── image2.jpg
├── person3/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
└── ...
```

## Guidelines:
- Each person should have their own directory
- Each person should have at least 2 images for genuine pair testing
- Use clear, front-facing photos when possible
- Supported formats: .jpg, .png
- Minimum 3 different people recommended
- 5-10 people with 3-5 images each is ideal for comprehensive testing

## Preparing Your Data:
1. Create directories named after each person (e.g., person1, person2, etc.)
2. Place multiple images of the same person in their respective directory
3. Ensure good image quality and proper face visibility
4. The benchmark will automatically create genuine pairs (same person) and impostor pairs (different people)
EOF

# Create benchmark configuration file
cat > benchmark_config.py << 'EOF'
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
EOF
