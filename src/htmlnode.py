

class HTMLNode:
    def __init__(self, tag:str=None, value:str=None, children:list=None, props:dict=None):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props
        
    def to_html(self):
        raise NotImplementedError("To be overridden by children classes")
    
    def props_to_html(self):
        props_str = ""
        if self.props:
            for key in self.props:
                props_str +=  f' {key}="{self.props[key]}"'
        return props_str
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag:str | None, value:str, props:dict=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self)->str:
        if self.value is None:
            raise ValueError("LeafNode requires a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    
class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list, props:dict=None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self)->str:
        if not self.tag:
            raise ValueError("ParentNode must have tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        html = f'<{self.tag}{self.props_to_html()}>'
        
        for child in self.children:
            html += child.to_html()
            
        html += f'</{self.tag}>'
        
        return html