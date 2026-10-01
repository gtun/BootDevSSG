from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"     # text
    BOLD = "bold"       # **text**
    ITALIC = "italic"   # _text_
    CODE = "code"       # `text`
    LINK = "link"       # [text](url)
    IMAGE = "image"     # ![text](url)

class TextNode:
    def __init__(self, text: str, text_type:TextType, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other:"TextNode")->bool:
        return vars(self) == vars(other)

    def __repr__(self)->str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode)->LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url,"alt":text_node.text})
        case _:
            raise TypeError("Not a valid text type")
            