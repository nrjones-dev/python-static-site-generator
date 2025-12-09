def markdown_to_blocks(markdown):
    md_blocks = markdown.split("\n\n")
    filtered_blocks = list(filter(None, map(str.strip, md_blocks)))

    return filtered_blocks
