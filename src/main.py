import os
import shutil

from src.html_node import HTMLNode, LeafNode
from src.text_node import TextNode, TextType

PUBLIC_PATH = "public"


def main():
    new_text_node = TextNode("This is a test", TextType.TEXT, "https://github.com")
    new_html_node = HTMLNode("p", "This is a paragraph")
    new_leaf_html_node = LeafNode("a", "click this link", {"href": "https://www.google.com"})
    print(new_text_node)
    print(new_html_node)
    print(new_leaf_html_node)


def clr_dir():
    if os.path.exists(PUBLIC_PATH):
        for item in os.listdir(PUBLIC_PATH):
            path = os.path.join(PUBLIC_PATH, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


def copy_content():
    pass


if __name__ == "__main__":
    main()
    clr_dir()
