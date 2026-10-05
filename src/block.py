

def markdown_to_blocks(markdown:str) -> list[str]:
    new_blocks = markdown.split("\n\n")
    new_blocks = [block.strip() for block in new_blocks if block.strip()]
    return new_blocks