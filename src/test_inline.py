import unittest
from textnode import TextNode, TextType
from src.inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
    
class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"),("obi wan","https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_at_beginning(self):
        node = TextNode("![cat](https://i.imgur.com/cat.png) starts the text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" starts the text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_in_middle(self):
        node = TextNode("Before ![cat](https://i.imgur.com/cat.png) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode("The text ends with ![cat](https://i.imgur.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("The text ends with ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
            ],
            new_nodes,
        )

    def test_two_images_in_middle(self):
        node = TextNode(
            "Start ![cat](https://i.imgur.com/cat.png) middle ![dog](https://i.imgur.com/dog.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "https://i.imgur.com/dog.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_beginning_and_middle(self):
        node = TextNode(
            "![cat](https://i.imgur.com/cat.png) then ![dog](https://i.imgur.com/dog.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "https://i.imgur.com/dog.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_malformed_image_unchanged(self):
        # missing the closing ] -- shouldn't be recognized as an image
        node = TextNode("This is ![broken image(https://i.imgur.com/cat.png) text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is ![broken image(https://i.imgur.com/cat.png) text", TextType.TEXT)],
            new_nodes,
        )

    def test_malformed_then_valid_image(self):
        node = TextNode(
            "A ![broken(https://i.imgur.com/bad.png) then ![dog](https://i.imgur.com/dog.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A ![broken(https://i.imgur.com/bad.png) then ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "https://i.imgur.com/dog.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_same_image_twice(self):
        # the case maxsplit=1 exists for
        node = TextNode(
            "![cat](https://i.imgur.com/cat.png) and ![cat](https://i.imgur.com/cat.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
            ],
            new_nodes,
        )

    def test_only_image(self):
        node = TextNode("![cat](https://i.imgur.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png")],
            new_nodes,
        )

    def test_adjacent_images(self):
        node = TextNode(
            "![cat](https://i.imgur.com/cat.png)![dog](https://i.imgur.com/dog.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode("dog", TextType.IMAGE, "https://i.imgur.com/dog.png"),
            ],
            new_nodes,
        )

    def test_links_left_alone(self):
        node = TextNode(
            "[boot dev](https://www.boot.dev) and ![cat](https://i.imgur.com/cat.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("[boot dev](https://www.boot.dev) and ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
            ],
            new_nodes,
        )

    def test_non_text_node_unchanged(self):
        node = TextNode("bold ![cat](https://i.imgur.com/cat.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("bold ![cat](https://i.imgur.com/cat.png)", TextType.BOLD)],
            new_nodes,
        )

    def test_multiple_input_nodes(self):
        node_list = [
            TextNode("A ![cat](https://i.imgur.com/cat.png) B", TextType.TEXT),
            TextNode("no images here", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(node_list)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" B", TextType.TEXT),
                TextNode("no images here", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_empty_input_list(self):
        self.assertListEqual([], split_nodes_image([]))

    def test_empty_alt_text(self):
        # empty alt text is valid (decorative images) -- locks in that behavior
        node = TextNode("Decorative ![](https://i.imgur.com/cat.png) image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Decorative ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" image", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitLinks(unittest.TestCase):
    def test_link_at_beginning(self):
        node = TextNode("[boot dev](https://www.boot.dev) starts the text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" starts the text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_in_middle(self):
        node = TextNode("Before [boot dev](https://www.boot.dev) after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode("The text ends with [boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("The text ends with ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_two_links_in_middle(self):
        node = TextNode(
            "Start [boot dev](https://www.boot.dev) middle [youtube](https://www.youtube.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_beginning_and_middle(self):
        node = TextNode(
            "[boot dev](https://www.boot.dev) then [youtube](https://www.youtube.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" then ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_malformed_link_unchanged(self):
        # missing the closing ] -- shouldn't be recognized as a link
        node = TextNode("This is [broken link(https://www.boot.dev) text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is [broken link(https://www.boot.dev) text", TextType.TEXT)],
            new_nodes,
        )

    def test_malformed_then_valid_link(self):
        node = TextNode(
            "A [broken(https://bad.example.com) then [youtube](https://www.youtube.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("A [broken(https://bad.example.com) then ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_same_link_twice(self):
        # the case maxsplit=1 exists for
        node = TextNode(
            "[boot dev](https://www.boot.dev) and [boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_only_link(self):
        node = TextNode("[boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("boot dev", TextType.LINK, "https://www.boot.dev")],
            new_nodes,
        )

    def test_adjacent_links(self):
        node = TextNode(
            "[boot dev](https://www.boot.dev)[youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_images_left_alone(self):
        # tests the (?<!!) lookbehind
        node = TextNode(
            "![cat](https://i.imgur.com/cat.png) and [boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![cat](https://i.imgur.com/cat.png) and ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_non_text_node_unchanged(self):
        node = TextNode("bold [boot dev](https://www.boot.dev)", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("bold [boot dev](https://www.boot.dev)", TextType.BOLD)],
            new_nodes,
        )

    def test_multiple_input_nodes(self):
        node_list = [
            TextNode("A [boot dev](https://www.boot.dev) B", TextType.TEXT),
            TextNode("no links here", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_link(node_list)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" B", TextType.TEXT),
                TextNode("no links here", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_empty_input_list(self):
        self.assertListEqual([], split_nodes_link([]))

    def test_empty_link_text(self):
        # the regex allows empty link text -- locks in that behavior
        node = TextNode("Click [](https://www.boot.dev) here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://www.boot.dev"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_course_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            text_to_textnodes("Just plain text"),
        )

    def test_empty_string(self):
        # empty TEXT nodes get dropped, so nothing is left
        self.assertListEqual([], text_to_textnodes(""))

    def test_only_bold(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    def test_image_url_with_underscores(self):
        # images must be split before the _ italic delimiter runs
        self.assertListEqual(
            [
                TextNode("See ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/my_cool_image.png"),
                TextNode(" now", TextType.TEXT),
            ],
            text_to_textnodes("See ![pic](https://example.com/my_cool_image.png) now"),
        )

    def test_link_url_with_underscores(self):
        # links must be split before the _ italic delimiter runs
        self.assertListEqual(
            [
                TextNode("Read ", TextType.TEXT),
                TextNode("the docs", TextType.LINK, "https://example.com/some_page_here"),
                TextNode(" first", TextType.TEXT),
            ],
            text_to_textnodes("Read [the docs](https://example.com/some_page_here) first"),
        )

    def test_multiple_of_each_delimiter(self):
        self.assertListEqual(
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("c", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("d", TextType.ITALIC),
            ],
            text_to_textnodes("**a** and **b** with _c_ and _d_"),
        )

    def test_starts_with_image_ends_with_code(self):
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://i.imgur.com/cat.png"),
                TextNode(" then ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            text_to_textnodes("![img](https://i.imgur.com/cat.png) then `code`"),
        )

    def test_unclosed_delimiter_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("This **never closes")

    def test_known_limitation_link_syntax_inside_code(self):
        # KNOWN LIMITATION: links are split before code, so link syntax shown
        # inside backticks becomes a real link, leaving each backtick stranded
        # in its own TEXT node -- the code splitter then sees an unmatched
        # delimiter and raises. Locks in current behavior, not ideal behavior.
        with self.assertRaises(ValueError):
            text_to_textnodes("Write it like `[text](url)` in markdown")


if __name__ == "__main__":
    unittest.main()