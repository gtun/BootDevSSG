import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)
        
        node4 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node4)
    
    # text_node_to_html_node() tests
    def test_text_plain(self):
        node = TextNode("This is a plain text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a plain text node")
    
    def test_text_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
            
    def test_text_italic(self):
        node = TextNode("This is an italicized text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italicized text node")
    
    def test_text_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
            
    def test_text_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "https://garytunak.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")

    def test_text_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "https://garytunak.com/img/logo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["alt"], "This is an image text node")
            
    def test_text_error(self):
        node = TextNode("This is not a valid text node", "wingding")
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()