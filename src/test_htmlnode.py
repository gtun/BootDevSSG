import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node_none = HTMLNode()
        node_none_expected = ""
        self.assertEqual(node_none.props_to_html(), node_none_expected)

    def test_props_to_html_a(self):
        node_a = HTMLNode("a","Click me",props={"href":"https://garytunak.com","target":"_blank"})
        node_a_expected = ' href="https://garytunak.com" target="_blank"'
        self.assertEqual(node_a.props_to_html(), node_a_expected)

    def test_props_to_html_img(self):
        node_img = HTMLNode("img",props={"src":"https://garytunak.com/img/logo.png","alt":"garytunak logo"})
        node_img_expected = ' src="https://garytunak.com/img/logo.png" alt="garytunak logo"'
        self.assertEqual(node_img.props_to_html(), node_img_expected)

class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node_p = LeafNode("p", "Hello, world!")
        self.assertEqual(node_p.to_html(), "<p>Hello, world!</p>")

    def test_to_html_props(self):
        node_b = LeafNode("b", "Hello, world!", props={"fake_prop_1":"1","fake_prop_2":"2"})
        self.assertEqual(node_b.to_html(), '<b fake_prop_1="1" fake_prop_2="2">Hello, world!</b>')

    def test_to_html_code(self):
        node_code = LeafNode("code", "Hello, world!")
        self.assertEqual(node_code.to_html(), "<code>Hello, world!</code>")

    def test_to_html_empty_value(self):
        node_empty_cell = LeafNode("td", "")
        self.assertEqual(node_empty_cell.to_html(), "<td></td>")
        

class TestParentNode(unittest.TestCase):
    # --- Happy paths ---

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_leaf_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_multiple_parent_children(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "one")]),
                ParentNode("li", [LeafNode(None, "two")]),
            ],
        )
        self.assertEqual(node.to_html(), "<ul><li>one</li><li>two</li></ul>")

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [ParentNode("section", [ParentNode("p", [LeafNode("i", "deep")])])],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p><i>deep</i></p></section></div>",
        )

    def test_to_html_mixed_siblings(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode("p", [LeafNode(None, "Hello "), LeafNode("b", "world")]),
                LeafNode(None, "tail"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>Hello <b>world</b></p>tail</div>",
        )

    # --- Props ---

    def test_to_html_parent_props(self):
        node = ParentNode("div", [LeafNode("span", "child")], {"class": "box"})
        self.assertEqual(
            node.to_html(), '<div class="box"><span>child</span></div>'
        )

    def test_to_html_props_at_multiple_levels(self):
        node = ParentNode(
            "div",
            [ParentNode("a", [LeafNode("b", "link")], {"href": "https://garytunak.com"})],
            {"id": "nav"},
        )
        self.assertEqual(
            node.to_html(),
            '<div id="nav"><a href="https://garytunak.com"><b>link</b></a></div>',
        )

    # --- Errors ---

    def test_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "child")])
        with self.assertRaisesRegex(ValueError, "tag"):
            node.to_html()

    def test_empty_tag_raises(self):
        node = ParentNode("", [LeafNode("b", "child")])
        with self.assertRaisesRegex(ValueError, "tag"):
            node.to_html()

    def test_none_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaisesRegex(ValueError, "children"):
            node.to_html()

    def test_empty_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaisesRegex(ValueError, "children"):
            node.to_html()

    def test_invalid_leaf_deep_in_tree_raises(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("b", None)])])
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()