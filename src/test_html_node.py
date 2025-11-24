import unittest

from html_node import HTMLNode, LeafNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')


if __name__ == "__main__":
    unittest.main()
