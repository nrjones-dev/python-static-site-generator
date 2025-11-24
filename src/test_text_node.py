import unittest

from text_node import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_texttype_eq_false(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_eq_false(self):
        node = TextNode("This is not a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.nrjones.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.nrjones.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("Test node", TextType.LINK, "https://www.nrjones.dev")
        self.assertEqual("TextNode(Test node, link, https://www.nrjones.dev)", repr(node))


if __name__ == "__main__":
    unittest.main()
