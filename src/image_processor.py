import cv2
import numpy as np
from PIL import Image, ImageEnhance
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    @staticmethod
    def load_image(image_path: str) -> np.ndarray:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
        return image

    @staticmethod
    def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    @staticmethod
    def denoise(image: np.ndarray, strength: int = 10) -> np.ndarray:
        return cv2.fastNlMeansDenoising(image, None, strength, 7, 21)

    @staticmethod
    def binarize(
        image: np.ndarray,
        method: str = 'adaptive',
        threshold: int = 127
    ) -> np.ndarray:
        gray = ImageProcessor.convert_to_grayscale(image)
        
        if method == 'adaptive':
            binary = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )
        elif method == 'otsu':
            _, binary = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        else:
            _, binary = cv2.threshold(
                gray,
                threshold,
                255,
                cv2.THRESH_BINARY
            )
        
        return binary

    @staticmethod
    def deskew(image: np.ndarray) -> np.ndarray:
        gray = ImageProcessor.convert_to_grayscale(image)
        
        coords = np.column_stack(np.where(gray > 0))
        if len(coords) == 0:
            return image
        
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        if abs(angle) < 0.5:
            return image
        
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated

    @staticmethod
    def enhance_contrast(image: np.ndarray, alpha: float = 1.5) -> np.ndarray:
        return cv2.convertScaleAbs(image, alpha=alpha, beta=0)

    @staticmethod
    def resize_image(
        image: np.ndarray,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        scale: Optional[float] = None
    ) -> np.ndarray:
        height, width = image.shape[:2]
        
        if scale:
            new_width = int(width * scale)
            new_height = int(height * scale)
        else:
            new_width = width
            new_height = height
            
            if max_width and width > max_width:
                ratio = max_width / width
                new_width = max_width
                new_height = int(height * ratio)
            
            if max_height and new_height > max_height:
                ratio = max_height / new_height
                new_height = max_height
                new_width = int(new_width * ratio)
        
        if new_width != width or new_height != height:
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return image

    @staticmethod
    def enhance_sharpness(image: np.ndarray) -> np.ndarray:
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        return cv2.filter2D(image, -1, kernel)

    @staticmethod
    def preprocess_for_ocr(
        image_path: str,
        apply_denoise: bool = True,
        apply_deskew: bool = True,
        apply_binarize: bool = False,
        enhance_contrast: bool = True,
        max_size: Optional[int] = 2048
    ) -> np.ndarray:
        logger.info(f"Preprocessing image: {image_path}")
        image = ImageProcessor.load_image(image_path)
        
        if max_size:
            image = ImageProcessor.resize_image(
                image,
                max_width=max_size,
                max_height=max_size
            )
        
        if apply_deskew:
            image = ImageProcessor.deskew(image)
        
        if apply_denoise:
            gray = ImageProcessor.convert_to_grayscale(image)
            gray = ImageProcessor.denoise(gray)
            if len(image.shape) == 3:
                image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            else:
                image = gray
        
        if enhance_contrast:
            image = ImageProcessor.enhance_contrast(image)
        
        if apply_binarize:
            image = ImageProcessor.binarize(image)
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        return image

    @staticmethod
    def save_image(image: np.ndarray, output_path: str) -> None:
        cv2.imwrite(output_path, image)
        logger.info(f"Saved preprocessed image to: {output_path}")
