#!/usr/bin/env python3

import time
import argparse
from typing import Dict, List
import numpy as np

from src.ocr_engine import OCREngine
from src.image_processor import ImageProcessor
from src.utils import setup_logging, FileScanner

import logging
logger = logging.getLogger(__name__)


def benchmark_single_image(
    image_path: str,
    ocr_engine: OCREngine,
    runs: int = 3
) -> Dict:
    logger.info(f"Benchmarking single image: {image_path}")
    
    times = []
    for i in range(runs):
        start = time.time()
        full_text, extracted_data = ocr_engine.recognize_and_extract(image_path)
        elapsed = time.time() - start
        times.append(elapsed)
        logger.info(f"Run {i+1}/{runs}: {elapsed:.2f}s")
    
    return {
        'image': image_path,
        'avg_time': np.mean(times),
        'min_time': np.min(times),
        'max_time': np.max(times),
        'std_time': np.std(times),
        'text_blocks': len(extracted_data) if extracted_data else 0
    }


def benchmark_with_preprocessing(
    image_path: str,
    ocr_engine: OCREngine,
    runs: int = 3
) -> Dict:
    logger.info(f"Benchmarking with preprocessing: {image_path}")
    
    preprocess_times = []
    ocr_times = []
    total_times = []
    
    for i in range(runs):
        # Preprocessing
        start = time.time()
        processed = ImageProcessor.preprocess_for_ocr(image_path)
        preprocess_time = time.time() - start
        preprocess_times.append(preprocess_time)
        
        # OCR
        start = time.time()
        result = ocr_engine.recognize_numpy(processed)
        extracted_data = ocr_engine.extract_text(result)
        ocr_time = time.time() - start
        ocr_times.append(ocr_time)
        
        total_times.append(preprocess_time + ocr_time)
        logger.info(f"Run {i+1}/{runs}: preprocess={preprocess_time:.2f}s, ocr={ocr_time:.2f}s")
    
    return {
        'image': image_path,
        'avg_preprocess_time': np.mean(preprocess_times),
        'avg_ocr_time': np.mean(ocr_times),
        'avg_total_time': np.mean(total_times),
        'text_blocks': len(extracted_data) if extracted_data else 0
    }


def benchmark_batch_processing(
    image_paths: List[str],
    ocr_engine: OCREngine
) -> Dict:
    logger.info(f"Benchmarking batch processing: {len(image_paths)} images")
    
    start = time.time()
    results = ocr_engine.batch_recognize(image_paths)
    elapsed = time.time() - start
    
    successful = sum(1 for r in results if r.get('success', False))
    
    return {
        'total_images': len(image_paths),
        'successful': successful,
        'failed': len(image_paths) - successful,
        'total_time': elapsed,
        'avg_time_per_image': elapsed / len(image_paths),
        'images_per_second': len(image_paths) / elapsed
    }


def compare_cpu_gpu(image_path: str, runs: int = 3) -> Dict:
    logger.info("Comparing CPU vs GPU performance")
    
    # CPU
    logger.info("Testing CPU...")
    ocr_cpu = OCREngine(lang='ch', use_gpu=False, show_log=False)
    cpu_results = benchmark_single_image(image_path, ocr_cpu, runs)
    
    # GPU (if available)
    try:
        logger.info("Testing GPU...")
        ocr_gpu = OCREngine(lang='ch', use_gpu=True, show_log=False)
        gpu_results = benchmark_single_image(image_path, ocr_gpu, runs)
        
        speedup = cpu_results['avg_time'] / gpu_results['avg_time']
        
        return {
            'cpu_time': cpu_results['avg_time'],
            'gpu_time': gpu_results['avg_time'],
            'speedup': speedup,
            'gpu_available': True
        }
    except Exception as e:
        logger.warning(f"GPU test failed: {e}")
        return {
            'cpu_time': cpu_results['avg_time'],
            'gpu_time': None,
            'speedup': None,
            'gpu_available': False
        }


def print_results(results: Dict, title: str):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    for key, value in results.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
        else:
            print(f"{key}: {value}")


def main():
    parser = argparse.ArgumentParser(description='OCR Performance Benchmark')
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input image or directory'
    )
    
    parser.add_argument(
        '--runs',
        type=int,
        default=3,
        help='Number of runs for each test (default: 3)'
    )
    
    parser.add_argument(
        '--test',
        choices=['single', 'preprocess', 'batch', 'compare', 'all'],
        default='all',
        help='Test to run (default: all)'
    )
    
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Use GPU'
    )
    
    args = parser.parse_args()
    
    setup_logging()
    
    print("="*60)
    print("OCR Performance Benchmark")
    print("="*60)
    print(f"Input: {args.input}")
    print(f"Runs per test: {args.runs}")
    print(f"GPU: {'Enabled' if args.gpu else 'Disabled'}")
    print("="*60)
    
    ocr = OCREngine(lang='ch', use_gpu=args.gpu, show_log=False)
    
    if args.test in ['single', 'all']:
        if FileScanner.validate_file(args.input):
            results = benchmark_single_image(args.input, ocr, args.runs)
            print_results(results, "Single Image Benchmark")
    
    if args.test in ['preprocess', 'all']:
        if FileScanner.validate_file(args.input):
            results = benchmark_with_preprocessing(args.input, ocr, args.runs)
            print_results(results, "With Preprocessing Benchmark")
    
    if args.test in ['batch', 'all']:
        import os
        if os.path.isdir(args.input):
            images = FileScanner.get_image_files(args.input)[:10]
            if images:
                results = benchmark_batch_processing(images, ocr)
                print_results(results, "Batch Processing Benchmark")
        elif FileScanner.validate_file(args.input):
            results = benchmark_batch_processing([args.input], ocr)
            print_results(results, "Batch Processing Benchmark")
    
    if args.test in ['compare', 'all']:
        if FileScanner.validate_file(args.input):
            results = compare_cpu_gpu(args.input, args.runs)
            print_results(results, "CPU vs GPU Comparison")
    
    print("\n" + "="*60)
    print("Benchmark completed!")
    print("="*60)


if __name__ == '__main__':
    main()
