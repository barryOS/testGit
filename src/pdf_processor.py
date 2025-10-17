import os
import logging
from typing import List, Dict, Optional
from pdf2image import convert_from_path
from PIL import Image
import tempfile

logger = logging.getLogger(__name__)


class PDFProcessor:
    def __init__(self, dpi: int = 300):
        self.dpi = dpi

    def pdf_to_images(
        self,
        pdf_path: str,
        output_folder: Optional[str] = None,
        first_page: Optional[int] = None,
        last_page: Optional[int] = None
    ) -> List[str]:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Converting PDF to images: {pdf_path}")
        
        if output_folder is None:
            output_folder = tempfile.mkdtemp()
        else:
            os.makedirs(output_folder, exist_ok=True)
        
        images = convert_from_path(
            pdf_path,
            dpi=self.dpi,
            first_page=first_page,
            last_page=last_page
        )
        
        image_paths = []
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        for i, image in enumerate(images, start=1):
            image_path = os.path.join(output_folder, f"{pdf_name}_page_{i}.jpg")
            image.save(image_path, 'JPEG')
            image_paths.append(image_path)
            logger.info(f"Saved page {i} to {image_path}")
        
        return image_paths

    def process_pdf_with_ocr(
        self,
        pdf_path: str,
        ocr_engine,
        confidence_threshold: float = 0.5,
        output_folder: Optional[str] = None
    ) -> Dict[str, any]:
        image_paths = self.pdf_to_images(pdf_path, output_folder)
        
        results = {
            'pdf_file': pdf_path,
            'total_pages': len(image_paths),
            'pages': []
        }
        
        for i, image_path in enumerate(image_paths, start=1):
            try:
                logger.info(f"Processing page {i}/{len(image_paths)}")
                full_text, extracted_data = ocr_engine.recognize_and_extract(
                    image_path,
                    confidence_threshold
                )
                
                results['pages'].append({
                    'page_number': i,
                    'image_path': image_path,
                    'text': full_text,
                    'details': extracted_data,
                    'success': True
                })
            except Exception as e:
                logger.error(f"Error processing page {i}: {str(e)}")
                results['pages'].append({
                    'page_number': i,
                    'image_path': image_path,
                    'error': str(e),
                    'success': False
                })
        
        return results

    def get_full_pdf_text(self, pdf_results: Dict) -> str:
        texts = []
        for page in pdf_results['pages']:
            if page.get('success') and page.get('text'):
                texts.append(f"--- Page {page['page_number']} ---\n{page['text']}")
        
        return '\n\n'.join(texts)
