import unittest

from block_markdown import BlockType, all_lines_start_with, block_to_block_type, is_ordered_list, markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        markdown = """
This is the 1st line



this is the 5th line
this is the 6th line
"""
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is the 1st line",
                "this is the 5th line\nthis is the 6th line",
            ],
        )

    def test_block_to_block_type_general(self):
        cases = [
            ("# This is a heading", BlockType.HEADING),
            ("###### This is a heading", BlockType.HEADING),
            ("```\nThis is a\ncode block\n```", BlockType.CODE),
            ("```This is a code block```", BlockType.CODE),
            (">This is a quoted\n>block of\n>text", BlockType.QUOTE),
            ("- This is an unordered list\n- with items\n- in it", BlockType.ULIST),
            ("1. This is an ordered list\n2. with items\n3. in it", BlockType.OLIST),
            ("This is a normal paragraph\nHow do you do?", BlockType.PARAGRAPH),
        ]
        for block, expected in cases:
            with self.subTest(block):
                self.assertEqual(expected, block_to_block_type(block))

    def test_is_ordered_list(self):
        block = "1. foo\n2. bar\n3. sushi\n4. eggs"
        lines = block.split("\n")
        self.assertTrue(is_ordered_list(lines))

    def test_is_ordered_list_false(self):
        block = "1. foo\n3. bar"
        lines = block.split("\n")
        self.assertFalse(is_ordered_list(lines))

    def test_all_lines_start_with_quote(self):
        block = ">foo\n>bar\n>sushi\n>eggs"
        lines = block.split("\n")
        prefix = ">"
        self.assertTrue(all_lines_start_with(lines, prefix))

    def test_all_lines_start_with_ulist(self):
        block = "- foo\n- bar\n- sushi\n- eggs"
        lines = block.split("\n")
        prefix = "- "
        self.assertTrue(all_lines_start_with(lines, prefix))
