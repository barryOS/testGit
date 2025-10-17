import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    @staticmethod
    def remove_duplicates(text: str) -> str:
        lines = text.split('\n')
        seen = set()
        unique_lines = []
        
        for line in lines:
            line_clean = line.strip()
            if line_clean and line_clean not in seen:
                seen.add(line_clean)
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)

    @staticmethod
    def fix_common_errors(text: str, lang: str = 'ch') -> str:
        if lang == 'en':
            text = re.sub(r'(\w),(\w)', r'\1, \2', text)
            text = re.sub(r'(\w)\.(\w)', r'\1. \2', text)
        
        return text

    @staticmethod
    def sort_by_position(
        extracted_data: List[Dict],
        sort_direction: str = 'vertical'
    ) -> List[Dict]:
        if not extracted_data:
            return []
        
        if sort_direction == 'vertical':
            return sorted(
                extracted_data,
                key=lambda x: (x['position'][0][1], x['position'][0][0])
            )
        else:
            return sorted(
                extracted_data,
                key=lambda x: (x['position'][0][0], x['position'][0][1])
            )

    @staticmethod
    def group_by_lines(
        extracted_data: List[Dict],
        threshold: int = 10
    ) -> List[List[Dict]]:
        if not extracted_data:
            return []
        
        sorted_data = TextProcessor.sort_by_position(extracted_data, 'vertical')
        
        lines = []
        current_line = [sorted_data[0]]
        current_y = sorted_data[0]['position'][0][1]
        
        for item in sorted_data[1:]:
            item_y = item['position'][0][1]
            
            if abs(item_y - current_y) <= threshold:
                current_line.append(item)
            else:
                current_line.sort(key=lambda x: x['position'][0][0])
                lines.append(current_line)
                current_line = [item]
                current_y = item_y
        
        if current_line:
            current_line.sort(key=lambda x: x['position'][0][0])
            lines.append(current_line)
        
        return lines

    @staticmethod
    def reconstruct_text_from_lines(lines: List[List[Dict]]) -> str:
        reconstructed_lines = []
        
        for line in lines:
            line_text = ' '.join([item['text'] for item in line])
            reconstructed_lines.append(line_text)
        
        return '\n'.join(reconstructed_lines)

    @staticmethod
    def filter_by_confidence(
        extracted_data: List[Dict],
        min_confidence: float = 0.7
    ) -> List[Dict]:
        return [
            item for item in extracted_data
            if item['confidence'] >= min_confidence
        ]

    @staticmethod
    def get_statistics(extracted_data: List[Dict]) -> Dict:
        if not extracted_data:
            return {
                'total_items': 0,
                'average_confidence': 0,
                'min_confidence': 0,
                'max_confidence': 0
            }
        
        confidences = [item['confidence'] for item in extracted_data]
        
        return {
            'total_items': len(extracted_data),
            'average_confidence': sum(confidences) / len(confidences),
            'min_confidence': min(confidences),
            'max_confidence': max(confidences),
            'total_characters': sum(len(item['text']) for item in extracted_data)
        }
