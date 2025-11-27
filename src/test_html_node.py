import unittest

from html_node import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", None, None, {"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode("div", None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            "HTMLNode(div, None, None, {'href': 'https://www.google.com', 'target': '_blank'})", repr(node)
        )

    def test_values(self):
        node = HTMLNode("p", "Hello there")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello there")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_parent_node_repr(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            "ParentNode(div, children: [ParentNode(span, children: [LeafNode(b, grandchild, None)], None)], None)",
            repr(parent_node),
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "some normal text, followed by "),
                LeafNode("b", "some BOLD text "),
                LeafNode("i", "and then some italic text "),
                LeafNode(None, "and then some raw text again."),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p>some normal text, followed by <b>some BOLD text </b><i>and then some italic text </i>and then some raw text again.</p>",
        )

    def test_parent_without_tag_raises(self):
        child = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_parent_without_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()


if __name__ == "__main__":
    unittest.main()
