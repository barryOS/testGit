import os
import logging
from typing import List, Dict, Tuple, Optional, Union
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCREngine:
    def __init__(
        self,
        use_angle_cls=True,
        lang='ch',
        use_gpu=False,
        show_log=False
    ):
        self.ocr = PaddleOCR(
            use_angle_cls=use_angle_cls,
            lang=lang,
            use_gpu=use_gpu,
            show_log=show_log
        )
        logger.info(f"OCR Engine initialized with lang={lang}, gpu={use_gpu}")

    def recognize_image(
        self,
        image_path: str,
        cls=True
    ) -> List[Tuple[List[List[int]], Tuple[str, float]]]:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        logger.info(f"Processing image: {image_path}")
        result = self.ocr.ocr(image_path, cls=cls)
        return result

    def recognize_numpy(
        self,
        image_array: np.ndarray,
        cls=True
    ) -> List[Tuple[List[List[int]], Tuple[str, float]]]:
        result = self.ocr.ocr(image_array, cls=cls)
        return result

    def extract_text(
        self,
        result: List[Tuple[List[List[int]], Tuple[str, float]]],
        confidence_threshold: float = 0.5
    ) -> List[Dict[str, Union[str, float, List[List[int]]]]]:
        if not result or not result[0]:
            return []
        
        extracted = []
        for line in result[0]:
            box, (text, confidence) = line
            if confidence >= confidence_threshold:
                extracted.append({
                    'text': text,
                    'confidence': confidence,
                    'position': box
                })
        
        return extracted

    def get_full_text(
        self,
        result: List[Tuple[List[List[int]], Tuple[str, float]]],
        confidence_threshold: float = 0.5,
        separator: str = '\n'
    ) -> str:
        extracted = self.extract_text(result, confidence_threshold)
        texts = [item['text'] for item in extracted]
        return separator.join(texts)

    def recognize_and_extract(
        self,
        image_path: str,
        confidence_threshold: float = 0.5,
        cls=True
    ) -> Tuple[str, List[Dict]]:
        result = self.recognize_image(image_path, cls=cls)
        extracted_data = self.extract_text(result, confidence_threshold)
        full_text = self.get_full_text(result, confidence_threshold)
        return full_text, extracted_data

    def batch_recognize(
        self,
        image_paths: List[str],
        confidence_threshold: float = 0.5,
        cls=True
    ) -> List[Dict[str, Union[str, List[Dict]]]]:
        results = []
        for image_path in image_paths:
            try:
                full_text, extracted_data = self.recognize_and_extract(
                    image_path,
                    confidence_threshold,
                    cls
                )
                results.append({
                    'file': image_path,
                    'text': full_text,
                    'details': extracted_data,
                    'success': True
                })
            except Exception as e:
                logger.error(f"Error processing {image_path}: {str(e)}")
                results.append({
                    'file': image_path,
                    'error': str(e),
                    'success': False
                })
        
        return results
