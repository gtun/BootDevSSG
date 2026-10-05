import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list" 

def markdown_to_blocks(markdown:str) -> list[str]:
    new_blocks = markdown.split("\n\n")
    new_blocks = [block.strip() for block in new_blocks if block.strip()]
    return new_blocks

def block_to_block_type(markdown) -> BlockType:
    if re.match(r"^#{1,6} .+", markdown):
        return BlockType.HEADING
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    
    lines = str.split(markdown,"\n")
    
    
    if lines[0].startswith(">"):
        for i in range(1, len(lines)):
            if not lines[i].startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if lines[0].startswith("- "):
        for i in range(1, len(lines)):
            if not lines[i].startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if lines[0].startswith("1. "):
        for i in range(1, len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH