from html_node import HTMLNode, LeafNode
from text_node import TextNode, TextType


def main():
    new_text_node = TextNode("This is a test", TextType.TEXT, "https://github.com")
    new_html_node = HTMLNode("p", "This is a paragraph")
    new_leaf_html_node = LeafNode("a", "click this link", {"href": "https://www.google.com"})
    print(new_text_node)
    print(new_html_node)
    print(new_leaf_html_node)




if __name__ == "__main__":
    main()
