import unittest
from block import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_multiple_newlines_in_middle(self):
        md="""
Just a line.





That was many blanks lines."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         [
                             "Just a line.",
                             "That was many blanks lines."
                         ])
        
    def test_line_in_beginning(self):
        md = """








Hello"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         ["Hello"])
    
    
    def test_line_in_end(self):
        md="""
That's it.







"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,["That's it."])
        
    def test_lines_with_whitespace(self):
        md="""
There are whitespace characters on the next line.

       

Promise."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,["There are whitespace characters on the next line.","Promise."])