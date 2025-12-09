import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_media,
    text_to_textnodes,
)
from text_node import TextNode, TextType


class TestSplitDelimiter(unittest.TestCase):
    def test_string_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_string_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_string_image(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_single_word_delimiter(self):
        node = TextNode("**Bold Word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [TextNode("Bold Word", TextType.BOLD)],
            new_nodes,
        )

    def test_missing_closing_delimiter(self):
        node = TextNode("This is text with a **bold word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_nodes(self):
        node_1 = TextNode("This is a text block", TextType.TEXT)
        node_2 = TextNode("This is text with a **bold word**", TextType.TEXT)
        node_3 = TextNode("`Code`", TextType.CODE)
        node_4 = TextNode("This is text block again", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_1, node_2, node_3, node_4], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("This is a text block", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode("`Code`", TextType.CODE),
                TextNode("This is text block again", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_empty_markdown_links(self):
        text = ""
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_empty_markdown_images(self):
        text = ""
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_empty_url_image(self):
        text = "![alt]()"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alt", "")], matches)

    def test_missing_alt_text_image(self):
        text = "![](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_split_nodes_media_images(self):
        node = TextNode(
            "This is text with an image ![to python](https://quantumzeitgeist.com/wp-content/uploads/pythoned.png) and ![to boot.dev](https://blog.boot.dev/img/800/bootsstandinggold.png.webp)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_media([node], extract_markdown_images, TextType.IMAGE)
        self.assertEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to python", TextType.IMAGE, "https://quantumzeitgeist.com/wp-content/uploads/pythoned.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to boot.dev", TextType.IMAGE, "https://blog.boot.dev/img/800/bootsstandinggold.png.webp"),
            ],
            new_nodes,
        )

    def test_split_nodes_media_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_media([node], extract_markdown_links, TextType.LINK)
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_nodes_media_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_media([node], extract_markdown_links, TextType.IMAGE)
        self.assertEqual([TextNode("", TextType.TEXT)], new_nodes)

    def test_split_nodes_media_no_links(self):
        node = TextNode("This is text with a link ", TextType.TEXT)
        new_nodes = split_nodes_media([node], extract_markdown_links, TextType.IMAGE)
        self.assertEqual([TextNode("This is text with a link ", TextType.TEXT)], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
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
            new_nodes,
        )

    def test_text_to_textnodes_empty(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertEqual([], new_nodes)

    def test_text_to_textnodes_links(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)" * 5
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
