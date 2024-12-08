import unittest
from tbe_header_parser import parse_tbe_file

class TestTBEParser(unittest.TestCase):
    def test_parse_tbe_file_valid(self):
        test_file = 'test_valid_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIsNotNone(metadata)  # Ensure metadata is not None
        self.assertIn('TBL', metadata)
        self.assertIn('Title', metadata['TBL'])

    def test_parse_tbe_file_missing_title(self):
        test_file = 'test_missing_title_tbe.csv'
        
        # Capture log output using assertLogs
        with self.assertLogs(level='WARNING') as cm:
            metadata = parse_tbe_file(test_file)
        
        log_output = cm.output
        # Now check for the missing title warning
        self.assertIn("WARNING:root:Missing required metadata field: 'Title'", log_output)
        self.assertIsNotNone(metadata)  # Ensure metadata is returned even if incomplete

    def test_parse_tbe_file_invalid_format(self):
        test_file = 'test_invalid_format_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIsNone(metadata)

    def test_parse_tbe_file_empty(self):
        test_file = 'test_empty_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIsNone(metadata)  # Expect None for empty files
