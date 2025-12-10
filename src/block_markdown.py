import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    md_blocks = markdown.split("\n\n")
    filtered_blocks = list(filter(None, map(str.strip, md_blocks)))
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all_lines_start_with(lines, ">"):
        return BlockType.QUOTE
    if all_lines_start_with(lines, "- "):
        return BlockType.ULIST

    if is_ordered_list(lines):
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def is_ordered_list(lines):
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            return False
    return True


def all_lines_start_with(lines, prefix):
    for line in lines:
        if not line.startswith(prefix):
            return False
    return True
