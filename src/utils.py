import os
import json
import logging
from typing import List, Dict, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class OutputFormatter:
    @staticmethod
    def save_as_txt(text: str, output_path: str) -> None:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        logger.info(f"Text saved to: {output_path}")

    @staticmethod
    def save_as_json(data: Union[Dict, List], output_path: str) -> None:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"JSON saved to: {output_path}")

    @staticmethod
    def save_as_markdown(
        text: str,
        output_path: str,
        title: str = "OCR Result",
        metadata: Dict = None
    ) -> None:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            
            if metadata:
                f.write("## Metadata\n\n")
                for key, value in metadata.items():
                    f.write(f"- **{key}**: {value}\n")
                f.write("\n")
            
            f.write("## Content\n\n")
            f.write(text)
        
        logger.info(f"Markdown saved to: {output_path}")

    @staticmethod
    def create_output_filename(
        input_path: str,
        output_dir: str,
        suffix: str = "_ocr",
        extension: str = "txt"
    ) -> str:
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base_name}{suffix}_{timestamp}.{extension}"
        
        return os.path.join(output_dir, filename)


class FileScanner:
    @staticmethod
    def get_image_files(
        directory: str,
        extensions: List[str] = None
    ) -> List[str]:
        if extensions is None:
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
        
        image_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    image_files.append(os.path.join(root, file))
        
        return sorted(image_files)

    @staticmethod
    def get_pdf_files(directory: str) -> List[str]:
        pdf_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        
        return sorted(pdf_files)

    @staticmethod
    def validate_file(file_path: str) -> bool:
        return os.path.exists(file_path) and os.path.isfile(file_path)


def setup_logging(log_file: str = None, level: int = logging.INFO) -> None:
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )
