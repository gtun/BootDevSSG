
from htmlnode import ParentNode
from block import markdown_to_blocks, block_to_block_type, BlockType
from inline import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_children.append(block_markdown_to_node(block, block_type))
    return ParentNode("div",html_children)

def block_markdown_to_node(markdown: str, block_type: BlockType) -> ParentNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_node(markdown)
        case BlockType.HEADING:
            heading = markdown.split(" ", 1)
            return ParentNode(f"h{len(heading[0])}", text_to_children(heading[1]))
        case BlockType.CODE:
            text = markdown.removeprefix("```\n").removesuffix("```")
            return ParentNode("pre", [text_node_to_html_node(TextNode(text, TextType.CODE))])    
        case BlockType.QUOTE:
            lines = [line.removeprefix(">").strip() for line in markdown.split("\n")]
            quote = " ".join(lines) 
            return ParentNode("blockquote", text_to_children(quote))
        case BlockType.UNORDERED_LIST:
            lines = [line.removeprefix("- ").strip() for line in markdown.split("\n")]
            return ParentNode("ul", [ParentNode("li", text_to_children(line)) for line in lines])
        case BlockType.ORDERED_LIST:
            lines = [line.split(". ", 1)[1] for line in markdown.split("\n")]
            return ParentNode("ol", [ParentNode("li", text_to_children(line)) for line in lines])
        case _:
            raise Exception("BlockType is missing for some reason even though at this point it shouldn't be")

def text_to_children(text: str) -> list:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def paragraph_to_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))