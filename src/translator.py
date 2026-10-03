from textnode import TextNode, TextType
import re

INLINE_DELIMITERS = [
    ("**", TextType.BOLD),
    ("_", TextType.ITALIC),
    ("`", TextType.CODE),
]

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text_strings = node.text.split(delimiter)
            if len(text_strings) % 2 == 0:
                raise ValueError(f"Matching closing delimiter '{delimiter}' not found!")
            for i in range(0, len(text_strings)):
                if not text_strings[i]:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(text_strings[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text_strings[i], text_type))
    
    return new_nodes

def extract_markdown_images(text)->list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    

def extract_markdown_links(text)->list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:    
            new_nodes.append(node)
            continue
        image_tuples_list = extract_markdown_images(node.text)
        if not image_tuples_list:
            new_nodes.append(node)
            continue
        
        leftover = node.text
        for alt_text, image_url in image_tuples_list:
            sections = leftover.split(f"![{alt_text}]({image_url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            leftover = sections[1]
        if leftover:
            new_nodes.append(TextNode(leftover, TextType.TEXT))
        
    return new_nodes
            
            
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:    
            new_nodes.append(node)
            continue
        link_tuples_list = extract_markdown_links(node.text)
        if not link_tuples_list:
            new_nodes.append(node)
            continue
        
        leftover = node.text
        for link_text, url in link_tuples_list:
            sections = leftover.split(f"[{link_text}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            leftover = sections[1]
        if leftover:
            new_nodes.append(TextNode(leftover, TextType.TEXT))
        
    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    nodes = split_nodes_image(split_nodes_link([TextNode(text, TextType.TEXT)]))

    for delimiter, text_type in INLINE_DELIMITERS:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    
    return nodes