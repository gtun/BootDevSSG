import unittest
from markdown_to_html import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
        # Headings
    def test_heading_h1(self):
        node = markdown_to_html_node("# Title")
        self.assertEqual(node.to_html(), "<div><h1>Title</h1></div>")

    def test_heading_h3_with_inline(self):
        node = markdown_to_html_node("### Sub **bold**")
        self.assertEqual(node.to_html(), "<div><h3>Sub <b>bold</b></h3></div>")

    def test_heading_h6(self):
        node = markdown_to_html_node("###### Tiny")
        self.assertEqual(node.to_html(), "<div><h6>Tiny</h6></div>")

    # Quotes
    def test_quote_multiline(self):
        node = markdown_to_html_node("> line one\n> line two")
        self.assertEqual(
            node.to_html(), "<div><blockquote>line one line two</blockquote></div>"
        )

    def test_quote_no_space_after_marker(self):
        node = markdown_to_html_node(">line one\n>line two")
        self.assertEqual(
            node.to_html(), "<div><blockquote>line one line two</blockquote></div>"
        )

    def test_quote_with_inline(self):
        node = markdown_to_html_node("> a _quote_ here")
        self.assertEqual(
            node.to_html(), "<div><blockquote>a <i>quote</i> here</blockquote></div>"
        )

    # Unordered lists
    def test_unordered_list(self):
        node = markdown_to_html_node("- one\n- two\n- three")
        self.assertEqual(
            node.to_html(), "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>"
        )

    def test_unordered_list_with_inline(self):
        node = markdown_to_html_node("- plain\n- **bold** item\n- `code` item")
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>plain</li><li><b>bold</b> item</li><li><code>code</code> item</li></ul></div>",
        )

    # Ordered lists
    def test_ordered_list(self):
        node = markdown_to_html_node("1. first\n2. second\n3. third")
        self.assertEqual(
            node.to_html(), "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>"
        )

    def test_ordered_list_with_inline(self):
        node = markdown_to_html_node("1. plain\n2. _italic_ item")
        self.assertEqual(
            node.to_html(), "<div><ol><li>plain</li><li><i>italic</i> item</li></ol></div>"
        )

    # Whole document, all block types together
    def test_full_document(self):
        md = (
            "# Heading\n\n"
            "A paragraph with **bold**.\n\n"
            "- item one\n- item two\n\n"
            "1. first\n2. second\n\n"
            "> a quote\n\n"
            "```\ncode here\n```"
        )
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Heading</h1>"
            "<p>A paragraph with <b>bold</b>.</p>"
            "<ul><li>item one</li><li>item two</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<blockquote>a quote</blockquote>"
            "<pre><code>code here\n</code></pre>"
            "</div>",
        )

if __name__ == "__main__":
    unittest.main()