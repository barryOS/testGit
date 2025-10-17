#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ocr_engine import OCREngine
from src.image_processor import ImageProcessor
from src.text_processor import TextProcessor
from src.utils import setup_logging


def example_basic_ocr():
    print("=" * 50)
    print("示例1: 基本OCR识别")
    print("Example 1: Basic OCR Recognition")
    print("=" * 50)
    
    ocr = OCREngine(lang='ch', use_gpu=False, show_log=False)
    
    image_path = 'your_image.jpg'
    
    if os.path.exists(image_path):
        full_text, extracted_data = ocr.recognize_and_extract(image_path)
        
        print(f"\n识别文本 / Recognized Text:\n{full_text}")
        print(f"\n识别了 {len(extracted_data)} 个文本块")
        
        stats = TextProcessor.get_statistics(extracted_data)
        print(f"平均置信度: {stats['average_confidence']:.2%}")
    else:
        print(f"请将图片放置在: {image_path}")
        print(f"或修改代码中的图片路径")


def example_with_preprocessing():
    print("\n" + "=" * 50)
    print("示例2: 带图像预处理的OCR识别")
    print("Example 2: OCR with Image Preprocessing")
    print("=" * 50)
    
    ocr = OCREngine(lang='ch', use_gpu=False, show_log=False)
    
    image_path = 'your_image.jpg'
    
    if os.path.exists(image_path):
        processed_image = ImageProcessor.preprocess_for_ocr(
            image_path,
            apply_denoise=True,
            apply_deskew=True,
            enhance_contrast=True
        )
        
        ImageProcessor.save_image(processed_image, 'preprocessed_output.jpg')
        print("预处理后的图像已保存到: preprocessed_output.jpg")
        
        result = ocr.recognize_numpy(processed_image)
        extracted_data = ocr.extract_text(result)
        full_text = ocr.get_full_text(result)
        
        print(f"\n识别文本:\n{full_text}")
    else:
        print(f"请将图片放置在: {image_path}")


def example_batch_processing():
    print("\n" + "=" * 50)
    print("示例3: 批量处理")
    print("Example 3: Batch Processing")
    print("=" * 50)
    
    ocr = OCREngine(lang='ch', use_gpu=False, show_log=False)
    
    image_paths = [
        'image1.jpg',
        'image2.jpg',
        'image3.jpg'
    ]
    
    existing_images = [p for p in image_paths if os.path.exists(p)]
    
    if existing_images:
        results = ocr.batch_recognize(existing_images)
        
        for i, result in enumerate(results, 1):
            if result['success']:
                print(f"\n图片 {i}: {result['file']}")
                print(f"识别了 {len(result['details'])} 个文本块")
                print(f"文本预览: {result['text'][:100]}...")
            else:
                print(f"\n图片 {i} 处理失败: {result['error']}")
    else:
        print("未找到图片文件")
        print("请将图片命名为 image1.jpg, image2.jpg 等")


def example_text_processing():
    print("\n" + "=" * 50)
    print("示例4: 文本后处理")
    print("Example 4: Text Post-processing")
    print("=" * 50)
    
    sample_data = [
        {
            'text': '第一行文本',
            'confidence': 0.95,
            'position': [[10, 10], [100, 10], [100, 30], [10, 30]]
        },
        {
            'text': '第二行文本',
            'confidence': 0.88,
            'position': [[10, 40], [100, 40], [100, 60], [10, 60]]
        },
        {
            'text': '低置信度文本',
            'confidence': 0.45,
            'position': [[10, 70], [100, 70], [100, 90], [10, 90]]
        }
    ]
    
    filtered = TextProcessor.filter_by_confidence(sample_data, min_confidence=0.7)
    print(f"\n过滤后保留 {len(filtered)} 个高质量文本块")
    
    stats = TextProcessor.get_statistics(sample_data)
    print(f"\n统计信息:")
    print(f"  总文本块: {stats['total_items']}")
    print(f"  平均置信度: {stats['average_confidence']:.2%}")
    print(f"  最低置信度: {stats['min_confidence']:.2%}")
    print(f"  最高置信度: {stats['max_confidence']:.2%}")


def main():
    setup_logging()
    
    print("高精度中英文OCR文档识别系统 - 快速开始示例")
    print("High-Accuracy OCR System - Quick Start Examples")
    print("\n")
    
    example_basic_ocr()
    
    example_with_preprocessing()
    
    example_batch_processing()
    
    example_text_processing()
    
    print("\n" + "=" * 50)
    print("更多用法请查看 README.md")
    print("For more usage examples, see README.md")
    print("=" * 50)


if __name__ == '__main__':
    main()
