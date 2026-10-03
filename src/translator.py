from textnode import TextNode, TextType

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