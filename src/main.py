from text_node import TextNode, TextType


def main():
    new_node = TextNode("This is a test", TextType.LINK, "https://github.com")
    print(new_node)


if __name__ == "__main__":
    main()
