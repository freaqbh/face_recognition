# Face Recognition Benchmark Report

## Executive Summary

- **Benchmark Date**: 2025-06-18 04:17:50
- **Total Combinations Tested**: 72
- **Successful Tests**: 48
- **Failed Tests**: 24

## System Information

- **CPU Cores**: 12
- **Total Memory**: 7.21 GB
- **Python Version**: 3.10.9

## Performance Overview

### Top Performers

#### Best Accuracy
- **Combination**: opencv + SFace
- **Accuracy**: 1.0000
- **Processing Time**: 1.488s

#### Fastest Processing
- **Combination**: ssd + DeepID
- **Processing Time**: 0.371s
- **Accuracy**: 0.3750

#### Best F1-Score
- **Combination**: opencv + SFace
- **F1-Score**: 1.0000
- **Accuracy**: 1.0000

### Detailed Results

| Detector | Model | Accuracy | Precision | Recall | F1-Score | Avg Time (s) | Memory (MB) |
|----------|-------|----------|-----------|--------|----------|--------------|-------------|
| opencv | SFace | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.488 | 3.3 |
| dlib | Dlib | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 33.055 | -56.4 |
| mtcnn | VGG-Face | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 3.384 | 303.8 |
| mtcnn | ArcFace | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 2.725 | 45.1 |
| mtcnn | Dlib | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 3.829 | 88.6 |
| retinaface | Dlib | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 20.761 | -25.5 |
| yunet | ArcFace | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 3.267 | 0.1 |
| yunet | Dlib | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 3.750 | 42.4 |
| yunet | SFace | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 3.058 | -26.2 |
| retinaface | ArcFace | 0.8750 | 0.8333 | 1.0000 | 0.9091 | 19.843 | 34.2 |
| yunet | VGG-Face | 0.8750 | 1.0000 | 0.8000 | 0.8889 | 3.994 | -43.6 |
| ssd | VGG-Face | 0.7500 | 1.0000 | 0.6000 | 0.7500 | 0.888 | 118.9 |
| ssd | ArcFace | 0.7500 | 1.0000 | 0.6000 | 0.7500 | 0.739 | 10.9 |
| ssd | Dlib | 0.7500 | 1.0000 | 0.6000 | 0.7500 | 1.123 | -14.1 |
| dlib | VGG-Face | 0.7500 | 0.8000 | 0.8000 | 0.8000 | 55.653 | -139.7 |
| dlib | ArcFace | 0.7500 | 0.8000 | 0.8000 | 0.8000 | 40.287 | 43.4 |
| mtcnn | Facenet | 0.7500 | 1.0000 | 0.6667 | 0.8000 | 3.130 | 6.3 |
| mtcnn | SFace | 0.7500 | 0.7500 | 1.0000 | 0.8571 | 2.143 | 54.7 |
| retinaface | VGG-Face | 0.7500 | 0.8000 | 0.8000 | 0.8000 | 22.965 | -9.8 |
| retinaface | Facenet | 0.7500 | 0.8000 | 0.8000 | 0.8000 | 19.972 | 5.9 |
| retinaface | Facenet512 | 0.7500 | 1.0000 | 0.6000 | 0.7500 | 20.134 | -44.4 |
| retinaface | SFace | 0.7500 | 0.8000 | 0.8000 | 0.8000 | 18.896 | 2.4 |
| opencv | VGG-Face | 0.6250 | 0.6250 | 1.0000 | 0.7692 | 10.741 | -47.9 |
| opencv | ArcFace | 0.6250 | 0.6250 | 1.0000 | 0.7692 | 2.911 | 46.0 |
| opencv | Dlib | 0.6250 | 0.6667 | 0.8000 | 0.7273 | 1.568 | -7.7 |
| ssd | Facenet | 0.6250 | 1.0000 | 0.4000 | 0.5714 | 0.881 | -63.7 |
| ssd | Facenet512 | 0.6250 | 1.0000 | 0.4000 | 0.5714 | 0.761 | -31.9 |
| ssd | SFace | 0.6250 | 1.0000 | 0.4000 | 0.5714 | 0.381 | 15.4 |
| dlib | Facenet512 | 0.6250 | 1.0000 | 0.4000 | 0.5714 | 34.769 | 24.4 |
| dlib | SFace | 0.6250 | 0.6667 | 0.8000 | 0.7273 | 35.055 | 21.0 |
| yunet | Facenet | 0.6250 | 1.0000 | 0.4000 | 0.5714 | 3.316 | 7.1 |
| yunet | Facenet512 | 0.6250 | 1.0000 | 0.4000 | 0.5714 | 3.244 | -22.6 |
| opencv | Facenet | 0.5000 | 0.6000 | 0.6000 | 0.6000 | 1.380 | -27.1 |
| opencv | Facenet512 | 0.5000 | 1.0000 | 0.2000 | 0.3333 | 1.206 | 12.8 |
| opencv | OpenFace | 0.5000 | 1.0000 | 0.2000 | 0.3333 | 1.581 | -176.7 |
| opencv | DeepID | 0.5000 | 1.0000 | 0.2000 | 0.3333 | 1.010 | 87.0 |
| dlib | Facenet | 0.5000 | 0.6667 | 0.4000 | 0.5000 | 33.973 | -142.5 |
| mtcnn | Facenet512 | 0.5000 | 1.0000 | 0.3333 | 0.5000 | 2.975 | 81.1 |
| mtcnn | OpenFace | 0.5000 | 1.0000 | 0.3333 | 0.5000 | 2.373 | 87.9 |
| retinaface | OpenFace | 0.5000 | 1.0000 | 0.2000 | 0.3333 | 19.734 | 57.2 |
| ssd | OpenFace | 0.3750 | 0.0000 | 0.0000 | 0.0000 | 0.499 | 24.1 |
| ssd | DeepID | 0.3750 | 0.0000 | 0.0000 | 0.0000 | 0.371 | 11.4 |
| dlib | OpenFace | 0.3750 | 0.0000 | 0.0000 | 0.0000 | 35.430 | 33.1 |
| dlib | DeepID | 0.3750 | 0.0000 | 0.0000 | 0.0000 | 38.974 | -23.5 |
| retinaface | DeepID | 0.3750 | 0.0000 | 0.0000 | 0.0000 | 19.199 | -90.2 |
| yunet | OpenFace | 0.3750 | 0.0000 | 0.0000 | 0.0000 | 3.008 | 10.0 |
| yunet | DeepID | 0.3750 | 0.0000 | 0.0000 | 0.0000 | 2.894 | 5.7 |
| mtcnn | DeepID | 0.2500 | 0.0000 | 0.0000 | 0.0000 | 2.069 | 18.5 |


## Recommendations

Based on the benchmark results:

1. **For highest accuracy**: Choose the detector-model combination with the best accuracy score
2. **For fastest processing**: Consider combinations with the lowest processing time if speed is critical
3. **For balanced performance**: Look for combinations with high F1-scores that balance precision and recall
4. **For resource-constrained environments**: Consider memory usage alongside processing time

## Files Generated

- `benchmark_summary.csv`: Tabular summary of all results
- `detailed_results.json`: Complete benchmark data with all metrics
- `benchmark_visualizations.png`: Performance comparison charts
- `benchmark_report.md`: This report

---
*Report generated automatically by Face Recognition Benchmark Tool*
