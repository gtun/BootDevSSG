import unittest
import enum
from block import markdown_to_blocks, block_to_block_type, BlockType



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
        
class TestBlockToBlockType(unittest.TestCase):
    # Headings
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_seven_hashes(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # Code
    def test_code(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')\n```"), BlockType.CODE)

    def test_code_no_newline_after_opening(self):
        self.assertEqual(block_to_block_type("```print('hi')```"), BlockType.PARAGRAPH)

    def test_code_no_closing(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')"), BlockType.PARAGRAPH)

    # Quotes
    def test_quote(self):
        self.assertEqual(block_to_block_type("> line one\n> line two"), BlockType.QUOTE)

    def test_quote_no_space_after_marker(self):
        self.assertEqual(block_to_block_type(">line one\n>line two"), BlockType.QUOTE)

    def test_quote_second_line_missing_marker(self):
        self.assertEqual(block_to_block_type("> line one\nline two"), BlockType.PARAGRAPH)

    # Unordered lists
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- one\n- two\n- three"), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        self.assertEqual(block_to_block_type("-one\n-two"), BlockType.PARAGRAPH)

    def test_unordered_list_broken_line(self):
        self.assertEqual(block_to_block_type("- one\ntwo"), BlockType.PARAGRAPH)

    # Ordered lists
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. one\n2. two\n3. three"), BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. only"), BlockType.ORDERED_LIST)

    def test_ordered_list_starts_at_two(self):
        self.assertEqual(block_to_block_type("2. one\n3. two"), BlockType.PARAGRAPH)

    def test_ordered_list_skips_number(self):
        self.assertEqual(block_to_block_type("1. one\n3. two"), BlockType.PARAGRAPH)

    # Paragraphs
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text."), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("Line one\nline two"), BlockType.PARAGRAPH)