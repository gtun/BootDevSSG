from enum import Enum


class TextType(Enum):
    PLAIN = "plain"     # text
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