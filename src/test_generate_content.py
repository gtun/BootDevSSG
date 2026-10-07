import unittest
from generate_content import extract_title, generate_page

class TestExtractTitle(unittest.TestCase):
    def test_good_heading(self):
        test = """
# My heading
"""
        self.assertEqual(extract_title(test),"My heading")
    
    def test_correct_heading(self):
        test = """
## Not my heading
# My heading
"""
        self.assertEqual(extract_title(test),"My heading")
    
    def test_no_heading(self):
        test = """
### Also not my heading
"""
        with self.assertRaises(ValueError):
            extract_title(test)
    
    def test_whitespaces_heading(self):
        test = """
#    My wide whitespaced heading    
"""
        self.assertEqual(extract_title(test),"My wide whitespaced heading")

if __name__ == "__main__":
    unittest.main()