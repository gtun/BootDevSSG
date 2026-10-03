import unittest

from textnode import TextNode, TextType
from translator import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_code_blocks(self):
        node = TextNode("BThis is `CODE` and so is this `CODE` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("BThis is ", TextType.TEXT),
                TextNode("CODE", TextType.CODE),
                TextNode(" and so is this ", TextType.TEXT),
                TextNode("CODE", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_delimiters_at_start_and_end(self):
        node = TextNode("`CTHIS` `IS` a code `BLOCK`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("CTHIS", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("IS", TextType.CODE),
                TextNode(" a code ", TextType.TEXT),
                TextNode("BLOCK", TextType.CODE),
            ],
        )

    def test_no_delimiter(self):
        node = TextNode("This has no code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This has no code", TextType.TEXT)])

    def test_multiple_input_nodes(self):
        node_list = [
            TextNode("AThis is text with a `CODE BLOCK` word", TextType.TEXT),
            TextNode("This has no code", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("AThis is text with a ", TextType.TEXT),
                TextNode("CODE BLOCK", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This has no code", TextType.TEXT),
            ],
        )

    def test_unclosed_delimiter_raises(self):
        node = TextNode("This has no `closing backtick", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_node_unchanged(self):
        node = TextNode("Emboldened!", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Emboldened!", TextType.BOLD)])

    def test_bold_delimiter(self):
        node = TextNode("This is **bolded** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_chained_delimiters(self):
        node = TextNode("A **bold** and `code` mix", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" mix", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()