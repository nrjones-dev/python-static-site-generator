import re
from enum import Enum

from html_node import ParentNode
from inline_markdown import text_to_textnodes
from text_node import TextNode, TextType, text_node_to_html_node


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


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)
    return child_nodes


def paragraph_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = [line.strip() for line in lines]
    paragraph = " ".join(cleaned_lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    result = " ".join(new_lines)
    children = text_to_children(result)
    return ParentNode("blockquote", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    list_items = []
    for item in items:
        numbered_item = item.split(". ", 1)[1]
        children = text_to_children(numbered_item)
        text_node = ParentNode("li", children)
        list_items.append(text_node)
    return ParentNode("ol", list_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    list_items = []
    for item in items:
        children = text_to_children(item[2:])
        text_node = ParentNode("li", children)
        list_items.append(text_node)
    return ParentNode("ul", list_items)


def heading_to_html_node(block):
    heading_count = 0
    for char in block:
        if char == "#":
            heading_count += 1
        else:
            break
    if heading_count + 1 >= len(block):
        raise ValueError("Invalid heading level, no content found")
    heading_text = block[heading_count + 1 :]
    children = text_to_children(heading_text)
    return ParentNode(f"h{heading_count}", children)
