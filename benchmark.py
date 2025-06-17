#!/usr/bin/env python3
"""
Face Recognition Benchmarking Script
====================================
Automated benchmarking tool for testing different combinations of 
detector and recognizer models in DeepFace library.

This script performs comprehensive performance analysis including:
- Accuracy testing with genuine/impostor pairs
- Speed benchmarking
- Memory usage monitoring
- Model comparison reports

Usage:
    python benchmark_face_recognition.py --test-dir /path/to/test/images
"""

import os
import sys
import json
import time
import argparse
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from deepface import DeepFace
import psutil
import cv2
from itertools import combinations
import warnings

# Suppress TensorFlow warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('benchmark.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class FaceRecognitionBenchmark:
    """Main benchmarking class for face recognition models."""
    
    SUPPORTED_DETECTORS = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe', 'yolov8', 'yunet']
    SUPPORTED_MODELS = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib', 'SFace']
    
    def __init__(self, test_data_dir: str, output_dir: str = "benchmark_results"):
        """
        Initialize the benchmark system.
        
        Args:
            test_data_dir: Directory containing test images
            output_dir: Directory to save benchmark results
        """
        self.test_data_dir = Path(test_data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Results storage
        self.results = []
        self.performance_metrics = {}
        self.error_log = []
        
        # System info
        self.system_info = self._get_system_info()
        
        logger.info(f"Benchmark initialized with test data: {test_data_dir}")
        logger.info(f"Results will be saved to: {output_dir}")
    
    def _get_system_info(self) -> Dict:
        """Get system information for benchmark context."""
        return {
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'python_version': sys.version,
            'timestamp': datetime.now().isoformat()
        }
    
    def prepare_test_data(self) -> Tuple[List[Tuple], List[Tuple]]:
        """
        Prepare genuine and impostor pairs from test data.
        
        Expected directory structure:
        test_data_dir/
        ├── person1/
        │   ├── img1.jpg
        │   └── img2.jpg
        ├── person2/
        │   ├── img1.jpg
        │   └── img2.jpg
        
        Returns:
            Tuple of (genuine_pairs, impostor_pairs)
        """
        logger.info("Preparing test data...")
        
        # Get all person directories
        person_dirs = [d for d in self.test_data_dir.iterdir() if d.is_dir()]
        
        if len(person_dirs) < 2:
            raise ValueError("Need at least 2 person directories for testing")
        
        genuine_pairs = []
        impostor_pairs = []
        
        # Create genuine pairs (same person)
        for person_dir in person_dirs:
            images = list(person_dir.glob("*.jpg")) + list(person_dir.glob("*.png"))
            if len(images) >= 2:
                for img1, img2 in combinations(images, 2):
                    genuine_pairs.append((str(img1), str(img2), True))
        
        # Create impostor pairs (different persons)
        for i, person1_dir in enumerate(person_dirs):
            for person2_dir in person_dirs[i+1:]:
                images1 = list(person1_dir.glob("*.jpg")) + list(person1_dir.glob("*.png"))
                images2 = list(person2_dir.glob("*.jpg")) + list(person2_dir.glob("*.png"))
                
                if images1 and images2:
                    # Take first image from each person for impostor pair
                    impostor_pairs.append((str(images1[0]), str(images2[0]), False))
        
        logger.info(f"Created {len(genuine_pairs)} genuine pairs and {len(impostor_pairs)} impostor pairs")
        return genuine_pairs, impostor_pairs
    
    def benchmark_single_combination(self, detector: str, model: str, test_pairs: List[Tuple]) -> Dict:
        """
        Benchmark a single detector-model combination.
        
        Args:
            detector: Detector backend name
            model: Recognition model name
            test_pairs: List of (img1_path, img2_path, is_genuine) tuples
        
        Returns:
            Dictionary with benchmark results
        """
        logger.info(f"Benchmarking {detector} + {model}")
        
        results = {
            'detector': detector,
            'model': model,
            'total_pairs': len(test_pairs),
            'successful_pairs': 0,
            'failed_pairs': 0,
            'errors': [],
            'predictions': [],
            'ground_truth': [],
            'processing_times': [],
            'memory_usage': []
        }
        
        for i, (img1_path, img2_path, is_genuine) in enumerate(test_pairs):
            try:
                # Monitor memory before processing
                memory_before = psutil.virtual_memory().used / (1024**2)  # MB
                
                # Time the verification
                start_time = time.time()
                
                result = DeepFace.verify(
                    img1_path=img1_path,
                    img2_path=img2_path,
                    detector_backend=detector,
                    model_name=model,
                    enforce_detection=False
                )
                
                processing_time = time.time() - start_time
                
                # Monitor memory after processing
                memory_after = psutil.virtual_memory().used / (1024**2)  # MB
                memory_used = memory_after - memory_before
                
                # Store results
                results['successful_pairs'] += 1
                results['predictions'].append(result['verified'])
                results['ground_truth'].append(is_genuine)
                results['processing_times'].append(processing_time)
                results['memory_usage'].append(memory_used)
                
                logger.debug(f"Pair {i+1}/{len(test_pairs)}: {processing_time:.3f}s")
                
            except Exception as e:
                error_msg = f"Error processing pair {i+1}: {str(e)}"
                results['errors'].append(error_msg)
                results['failed_pairs'] += 1
                logger.warning(error_msg)
        
        # Calculate metrics
        if results['successful_pairs'] > 0:
            results.update(self._calculate_metrics(results))
        
        return results
    
    def _calculate_metrics(self, results: Dict) -> Dict:
        """Calculate performance metrics from results."""
        predictions = np.array(results['predictions'])
        ground_truth = np.array(results['ground_truth'])
        
        # Accuracy metrics
        tp = np.sum((predictions == True) & (ground_truth == True))
        tn = np.sum((predictions == False) & (ground_truth == False))
        fp = np.sum((predictions == True) & (ground_truth == False))
        fn = np.sum((predictions == False) & (ground_truth == True))
        
        accuracy = (tp + tn) / len(predictions) if len(predictions) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Speed metrics
        processing_times = results['processing_times']
        avg_processing_time = np.mean(processing_times)
        std_processing_time = np.std(processing_times)
        
        # Memory metrics
        memory_usage = results['memory_usage']
        avg_memory_usage = np.mean(memory_usage)
        max_memory_usage = np.max(memory_usage)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'true_positives': int(tp),
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'avg_processing_time': avg_processing_time,
            'std_processing_time': std_processing_time,
            'min_processing_time': np.min(processing_times),
            'max_processing_time': np.max(processing_times),
            'avg_memory_usage_mb': avg_memory_usage,
            'max_memory_usage_mb': max_memory_usage
        }
    
    def run_comprehensive_benchmark(self, detectors: List[str] = None, models: List[str] = None) -> None:
        """
        Run comprehensive benchmark across all combinations.
        
        Args:
            detectors: List of detectors to test (default: all supported)
            models: List of models to test (default: all supported)
        """
        if detectors is None:
            detectors = self.SUPPORTED_DETECTORS
        if models is None:
            models = self.SUPPORTED_MODELS
        
        logger.info(f"Starting comprehensive benchmark with {len(detectors)} detectors and {len(models)} models")
        
        # Prepare test data
        genuine_pairs, impostor_pairs = self.prepare_test_data()
        all_test_pairs = genuine_pairs + impostor_pairs
        
        total_combinations = len(detectors) * len(models)
        current_combination = 0
        
        # Test each combination
        for detector in detectors:
            for model in models:
                current_combination += 1
                logger.info(f"Progress: {current_combination}/{total_combinations}")
                
                try:
                    result = self.benchmark_single_combination(detector, model, all_test_pairs)
                    self.results.append(result)
                    
                    # Save intermediate results
                    self._save_intermediate_results()
                    
                except Exception as e:
                    error_msg = f"Failed to benchmark {detector} + {model}: {str(e)}"
                    logger.error(error_msg)
                    self.error_log.append({
                        'detector': detector,
                        'model': model,
                        'error': error_msg,
                        'traceback': traceback.format_exc()
                    })
        
        logger.info("Benchmark completed. Generating reports...")
        self._generate_reports()
    
    def _save_intermediate_results(self) -> None:
        """Save intermediate results to prevent data loss."""
        results_file = self.output_dir / "intermediate_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'results': self.results,
                'errors': self.error_log,
                'system_info': self.system_info
            }, f, indent=2, default=str)
    
    def _generate_reports(self) -> None:
        """Generate comprehensive benchmark reports."""
        # Save detailed results
        self._save_detailed_results()
        
        # Generate CSV summary
        self._generate_csv_summary()
        
        # Generate visualizations
        self._generate_visualizations()
        
        # Generate markdown report
        self._generate_markdown_report()
        
        logger.info(f"Reports generated in {self.output_dir}")
    
    def _save_detailed_results(self) -> None:
        """Save detailed results to JSON file."""
        results_file = self.output_dir / "detailed_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'benchmark_info': {
                    'timestamp': datetime.now().isoformat(),
                    'total_combinations': len(self.results),
                    'system_info': self.system_info
                },
                'results': self.results,
                'errors': self.error_log
            }, f, indent=2, default=str)
    
    def _generate_csv_summary(self) -> None:
        """Generate CSV summary of results."""
        if not self.results:
            return
        
        # Flatten results for CSV
        csv_data = []
        for result in self.results:
            if 'accuracy' in result:  # Only include successful benchmarks
                csv_data.append({
                    'Detector': result['detector'],
                    'Model': result['model'],
                    'Accuracy': result['accuracy'],
                    'Precision': result['precision'],
                    'Recall': result['recall'],
                    'F1_Score': result['f1_score'],
                    'Avg_Processing_Time_s': result['avg_processing_time'],
                    'Std_Processing_Time_s': result['std_processing_time'],
                    'Avg_Memory_Usage_MB': result['avg_memory_usage_mb'],
                    'Max_Memory_Usage_MB': result['max_memory_usage_mb'],
                    'Successful_Pairs': result['successful_pairs'],
                    'Failed_Pairs': result['failed_pairs'],
                    'Total_Pairs': result['total_pairs']
                })
        
        if csv_data:
            df = pd.DataFrame(csv_data)
            df.to_csv(self.output_dir / "benchmark_summary.csv", index=False)
            logger.info("CSV summary saved")
    
    def _generate_visualizations(self) -> None:
        """Generate benchmark visualization plots."""
        if not self.results:
            return
        
        # Filter successful results
        successful_results = [r for r in self.results if 'accuracy' in r]
        
        if not successful_results:
            logger.warning("No successful results to visualize")
            return
        
        # Create DataFrame for plotting
        df_data = []
        for result in successful_results:
            df_data.append({
                'Combination': f"{result['detector']}\n{result['model']}",
                'Detector': result['detector'],
                'Model': result['model'],
                'Accuracy': result['accuracy'],
                'Processing_Time': result['avg_processing_time'],
                'Memory_Usage': result['avg_memory_usage_mb'],
                'F1_Score': result['f1_score']
            })
        
        df = pd.DataFrame(df_data)
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Face Recognition Benchmark Results', fontsize=16, fontweight='bold')
        
        # 1. Accuracy heatmap
        accuracy_pivot = df.pivot(index='Detector', columns='Model', values='Accuracy')
        sns.heatmap(accuracy_pivot, annot=True, fmt='.3f', cmap='RdYlGn', 
                   ax=axes[0,0], cbar_kws={'label': 'Accuracy'})
        axes[0,0].set_title('Accuracy by Detector-Model Combination')
        axes[0,0].set_xlabel('Recognition Model')
        axes[0,0].set_ylabel('Detector')
        
        # 2. Processing time comparison
        time_pivot = df.pivot(index='Detector', columns='Model', values='Processing_Time')
        sns.heatmap(time_pivot, annot=True, fmt='.3f', cmap='RdYlBu_r', 
                   ax=axes[0,1], cbar_kws={'label': 'Time (seconds)'})
        axes[0,1].set_title('Average Processing Time')
        axes[0,1].set_xlabel('Recognition Model')
        axes[0,1].set_ylabel('Detector')
        
        # 3. Accuracy vs Processing Time scatter
        scatter = axes[1,0].scatter(df['Processing_Time'], df['Accuracy'], 
                                  s=100, alpha=0.7, c=range(len(df)), cmap='viridis')
        axes[1,0].set_xlabel('Average Processing Time (seconds)')
        axes[1,0].set_ylabel('Accuracy')
        axes[1,0].set_title('Accuracy vs Processing Time Trade-off')
        axes[1,0].grid(True, alpha=0.3)
        
        # Add labels for points
        for i, row in df.iterrows():
            axes[1,0].annotate(f"{row['Detector'][:3]}-{row['Model'][:3]}", 
                             (row['Processing_Time'], row['Accuracy']),
                             xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        # 4. Top performers comparison
        df_sorted = df.nlargest(10, 'Accuracy')
        bars = axes[1,1].bar(range(len(df_sorted)), df_sorted['Accuracy'])
        axes[1,1].set_xlabel('Detector-Model Combination')
        axes[1,1].set_ylabel('Accuracy')
        axes[1,1].set_title('Top 10 Performing Combinations')
        axes[1,1].set_xticks(range(len(df_sorted)))
        axes[1,1].set_xticklabels([f"{row['Detector'][:4]}\n{row['Model'][:6]}" 
                                  for _, row in df_sorted.iterrows()], rotation=45)
        
        # Color bars based on performance
        for i, bar in enumerate(bars):
            bar.set_color(plt.cm.RdYlGn(df_sorted.iloc[i]['Accuracy']))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "benchmark_visualizations.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Visualizations saved")
    
    def _generate_markdown_report(self) -> None:
        """Generate a comprehensive markdown report."""
        if not self.results:
            return
        
        successful_results = [r for r in self.results if 'accuracy' in r]
        
        report_content = f"""# Face Recognition Benchmark Report

## Executive Summary

- **Benchmark Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Total Combinations Tested**: {len(self.results)}
- **Successful Tests**: {len(successful_results)}
- **Failed Tests**: {len(self.results) - len(successful_results)}

## System Information

- **CPU Cores**: {self.system_info['cpu_count']}
- **Total Memory**: {self.system_info['memory_total_gb']} GB
- **Python Version**: {self.system_info['python_version'].split()[0]}

## Performance Overview

"""
        
        if successful_results:
            # Find best performers
            best_accuracy = max(successful_results, key=lambda x: x['accuracy'])
            best_speed = min(successful_results, key=lambda x: x['avg_processing_time'])
            best_f1 = max(successful_results, key=lambda x: x['f1_score'])
            
            report_content += f"""### Top Performers

#### Best Accuracy
- **Combination**: {best_accuracy['detector']} + {best_accuracy['model']}
- **Accuracy**: {best_accuracy['accuracy']:.4f}
- **Processing Time**: {best_accuracy['avg_processing_time']:.3f}s

#### Fastest Processing
- **Combination**: {best_speed['detector']} + {best_speed['model']}
- **Processing Time**: {best_speed['avg_processing_time']:.3f}s
- **Accuracy**: {best_speed['accuracy']:.4f}

#### Best F1-Score
- **Combination**: {best_f1['detector']} + {best_f1['model']}
- **F1-Score**: {best_f1['f1_score']:.4f}
- **Accuracy**: {best_f1['accuracy']:.4f}

### Detailed Results

| Detector | Model | Accuracy | Precision | Recall | F1-Score | Avg Time (s) | Memory (MB) |
|----------|-------|----------|-----------|--------|----------|--------------|-------------|
"""
            
            # Sort by accuracy for detailed table
            sorted_results = sorted(successful_results, key=lambda x: x['accuracy'], reverse=True)
            
            for result in sorted_results:
                report_content += f"| {result['detector']} | {result['model']} | {result['accuracy']:.4f} | {result['precision']:.4f} | {result['recall']:.4f} | {result['f1_score']:.4f} | {result['avg_processing_time']:.3f} | {result['avg_memory_usage_mb']:.1f} |\n"
        
        if self.error_log:
            report_content += f"""

## Errors and Issues

The following combinations failed during testing:

"""
            for error in self.error_log:
                report_content += f"- **{error['detector']} + {error['model']}**: {error['error']}\n"
        
        report_content += """

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
"""
        
        # Save report
        report_file = self.output_dir / "benchmark_report.md"
        with open(report_file, 'w') as f:
            f.write(report_content)
        
        logger.info("Markdown report generated")

def main():
    """Main function to run the benchmark."""
    parser = argparse.ArgumentParser(description="Face Recognition Benchmarking Tool")
    parser.add_argument("--test-dir", required=True, help="Directory containing test images")
    parser.add_argument("--output-dir", default="benchmark_results", help="Output directory for results")
    parser.add_argument("--detectors", nargs="+", help="Specific detectors to test")
    parser.add_argument("--models", nargs="+", help="Specific models to test")
    parser.add_argument("--quick", action="store_true", help="Run quick benchmark with limited combinations")
    
    args = parser.parse_args()
    
    # Validate test directory
    if not os.path.exists(args.test_dir):
        logger.error(f"Test directory not found: {args.test_dir}")
        sys.exit(1)
    
    # Initialize benchmark
    benchmark = FaceRecognitionBenchmark(args.test_dir, args.output_dir)
    
    # Set up test parameters
    detectors = args.detectors
    models = args.models
    
    if args.quick:
        # Quick benchmark with popular combinations
        detectors = detectors or ['opencv', 'mtcnn', 'retinaface']
        models = models or ['VGG-Face', 'Facenet', 'ArcFace']
        logger.info("Running quick benchmark")
    
    try:
        # Run benchmark
        benchmark.run_comprehensive_benchmark(detectors, models)
        logger.info("Benchmark completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Benchmark failed: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()