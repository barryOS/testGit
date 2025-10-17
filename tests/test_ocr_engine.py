import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.text_processor import TextProcessor


class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.sample_data = [
            {
                'text': 'Hello World',
                'confidence': 0.95,
                'position': [[10, 10], [100, 10], [100, 30], [10, 30]]
            },
            {
                'text': '你好世界',
                'confidence': 0.88,
                'position': [[10, 40], [100, 40], [100, 60], [10, 60]]
            },
            {
                'text': 'Low confidence',
                'confidence': 0.45,
                'position': [[10, 70], [100, 70], [100, 90], [10, 90]]
            }
        ]

    def test_filter_by_confidence(self):
        filtered = TextProcessor.filter_by_confidence(
            self.sample_data,
            min_confidence=0.7
        )
        self.assertEqual(len(filtered), 2)
        for item in filtered:
            self.assertGreaterEqual(item['confidence'], 0.7)

    def test_get_statistics(self):
        stats = TextProcessor.get_statistics(self.sample_data)
        
        self.assertEqual(stats['total_items'], 3)
        self.assertAlmostEqual(stats['average_confidence'], 0.76, places=2)
        self.assertEqual(stats['min_confidence'], 0.45)
        self.assertEqual(stats['max_confidence'], 0.95)

    def test_clean_text(self):
        messy_text = "  Hello    World  \n  "
        cleaned = TextProcessor.clean_text(messy_text)
        self.assertEqual(cleaned, "Hello World")

    def test_sort_by_position(self):
        sorted_data = TextProcessor.sort_by_position(
            self.sample_data,
            sort_direction='vertical'
        )
        
        self.assertEqual(len(sorted_data), 3)
        for i in range(len(sorted_data) - 1):
            y1 = sorted_data[i]['position'][0][1]
            y2 = sorted_data[i + 1]['position'][0][1]
            self.assertLessEqual(y1, y2)


class TestImageProcessor(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


class TestPDFProcessor(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
