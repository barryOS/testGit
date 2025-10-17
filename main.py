#!/usr/bin/env python3
import os
import argparse
import logging
from tqdm import tqdm

from src.ocr_engine import OCREngine
from src.image_processor import ImageProcessor
from src.pdf_processor import PDFProcessor
from src.text_processor import TextProcessor
from src.utils import OutputFormatter, FileScanner, setup_logging

logger = logging.getLogger(__name__)


def process_single_image(
    image_path: str,
    ocr_engine: OCREngine,
    output_dir: str,
    preprocess: bool = False,
    confidence_threshold: float = 0.5,
    output_format: str = 'txt'
) -> None:
    try:
        if preprocess:
            logger.info(f"Preprocessing image: {image_path}")
            processed_image = ImageProcessor.preprocess_for_ocr(image_path)
            temp_path = os.path.join(output_dir, "temp_processed.jpg")
            ImageProcessor.save_image(processed_image, temp_path)
            full_text, extracted_data = ocr_engine.recognize_and_extract(
                temp_path,
                confidence_threshold
            )
            os.remove(temp_path)
        else:
            full_text, extracted_data = ocr_engine.recognize_and_extract(
                image_path,
                confidence_threshold
            )
        
        stats = TextProcessor.get_statistics(extracted_data)
        logger.info(f"OCR Statistics: {stats}")
        
        base_output_path = OutputFormatter.create_output_filename(
            image_path,
            output_dir,
            extension=output_format
        )
        
        if output_format == 'txt':
            OutputFormatter.save_as_txt(full_text, base_output_path)
        elif output_format == 'json':
            result = {
                'file': image_path,
                'text': full_text,
                'details': extracted_data,
                'statistics': stats
            }
            OutputFormatter.save_as_json(result, base_output_path)
        elif output_format == 'md':
            metadata = {
                'Source File': os.path.basename(image_path),
                'Total Items': stats['total_items'],
                'Average Confidence': f"{stats['average_confidence']:.2%}",
                'Total Characters': stats['total_characters']
            }
            OutputFormatter.save_as_markdown(
                full_text,
                base_output_path,
                title="OCR Recognition Result",
                metadata=metadata
            )
        
        logger.info(f"Successfully processed: {image_path}")
        
    except Exception as e:
        logger.error(f"Error processing {image_path}: {str(e)}")


def process_pdf(
    pdf_path: str,
    ocr_engine: OCREngine,
    pdf_processor: PDFProcessor,
    output_dir: str,
    confidence_threshold: float = 0.5,
    output_format: str = 'txt'
) -> None:
    try:
        temp_dir = os.path.join(output_dir, 'temp_pdf_images')
        os.makedirs(temp_dir, exist_ok=True)
        
        pdf_results = pdf_processor.process_pdf_with_ocr(
            pdf_path,
            ocr_engine,
            confidence_threshold,
            temp_dir
        )
        
        full_text = pdf_processor.get_full_pdf_text(pdf_results)
        
        base_output_path = OutputFormatter.create_output_filename(
            pdf_path,
            output_dir,
            extension=output_format
        )
        
        if output_format == 'txt':
            OutputFormatter.save_as_txt(full_text, base_output_path)
        elif output_format == 'json':
            OutputFormatter.save_as_json(pdf_results, base_output_path)
        elif output_format == 'md':
            metadata = {
                'Source File': os.path.basename(pdf_path),
                'Total Pages': pdf_results['total_pages']
            }
            OutputFormatter.save_as_markdown(
                full_text,
                base_output_path,
                title="PDF OCR Recognition Result",
                metadata=metadata
            )
        
        logger.info(f"Successfully processed PDF: {pdf_path}")
        
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description='高精度中英文OCR文档识别工具 / High-Accuracy Chinese-English OCR Tool'
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='输入文件或目录路径 / Input file or directory path'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='./output',
        help='输出目录路径 (默认: ./output) / Output directory path (default: ./output)'
    )
    
    parser.add_argument(
        '-l', '--lang',
        default='ch',
        choices=['ch', 'en', 'chinese_cht', 'korean', 'japan'],
        help='OCR语言 (默认: ch) / OCR language (default: ch)'
    )
    
    parser.add_argument(
        '-f', '--format',
        default='txt',
        choices=['txt', 'json', 'md'],
        help='输出格式 (默认: txt) / Output format (default: txt)'
    )
    
    parser.add_argument(
        '-c', '--confidence',
        type=float,
        default=0.5,
        help='置信度阈值 (0-1, 默认: 0.5) / Confidence threshold (0-1, default: 0.5)'
    )
    
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='使用GPU加速 / Use GPU acceleration'
    )
    
    parser.add_argument(
        '--preprocess',
        action='store_true',
        help='启用图像预处理 / Enable image preprocessing'
    )
    
    parser.add_argument(
        '--pdf',
        action='store_true',
        help='处理PDF文件 / Process PDF files'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='PDF转图像DPI (默认: 300) / PDF to image DPI (default: 300)'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='批量处理目录中的所有文件 / Batch process all files in directory'
    )
    
    parser.add_argument(
        '--log',
        default=None,
        help='日志文件路径 / Log file path'
    )
    
    args = parser.parse_args()
    
    setup_logging(args.log)
    
    os.makedirs(args.output, exist_ok=True)
    
    logger.info("Initializing OCR Engine...")
    ocr_engine = OCREngine(
        lang=args.lang,
        use_gpu=args.gpu,
        show_log=False
    )
    
    if args.pdf:
        pdf_processor = PDFProcessor(dpi=args.dpi)
        
        if args.batch and os.path.isdir(args.input):
            pdf_files = FileScanner.get_pdf_files(args.input)
            logger.info(f"Found {len(pdf_files)} PDF files")
            
            for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
                process_pdf(
                    pdf_file,
                    ocr_engine,
                    pdf_processor,
                    args.output,
                    args.confidence,
                    args.format
                )
        else:
            if not os.path.exists(args.input):
                logger.error(f"File not found: {args.input}")
                return
            
            process_pdf(
                args.input,
                ocr_engine,
                pdf_processor,
                args.output,
                args.confidence,
                args.format
            )
    else:
        if args.batch and os.path.isdir(args.input):
            image_files = FileScanner.get_image_files(args.input)
            logger.info(f"Found {len(image_files)} image files")
            
            for image_file in tqdm(image_files, desc="Processing images"):
                process_single_image(
                    image_file,
                    ocr_engine,
                    args.output,
                    args.preprocess,
                    args.confidence,
                    args.format
                )
        else:
            if not os.path.exists(args.input):
                logger.error(f"File not found: {args.input}")
                return
            
            process_single_image(
                args.input,
                ocr_engine,
                args.output,
                args.preprocess,
                args.confidence,
                args.format
            )
    
    logger.info("OCR processing completed!")


if __name__ == '__main__':
    main()
