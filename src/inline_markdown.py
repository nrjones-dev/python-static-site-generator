import re

from text_node import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        new_text = node.text.split(delimiter)
        if len(new_text) % 2 == 0:
            raise ValueError("Invalid markdown, formating not closed.")

        for i in range(len(new_text)):
            if new_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(new_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(new_text[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    alt_text = r"!\[([^]]*)\]"
    url_links = r"\(([^)]*)\)"
    matches = re.findall(alt_text + url_links, text)
    return matches


def extract_markdown_links(text):
    alt_text = r"(?<!!)\[([^]]*)\]"
    url_links = r"\(([^)]*)\)"
    matches = re.findall(alt_text + url_links, text)
    return matches


def split_nodes_media(old_nodes, extract_func, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text_links = extract_func(node.text)
        if not text_links:
            new_nodes.append(node)
            continue

        original_text = node.text
        for alt, url in text_links:
            if text_type == TextType.IMAGE:
                text_sections = original_text.split(f"![{alt}]({url})", 1)
            else:
                text_sections = original_text.split(f"[{alt}]({url})", 1)

            if len(text_sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if text_sections[0]:
                new_nodes.append(TextNode(text_sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, text_type, url))
            original_text = text_sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes
