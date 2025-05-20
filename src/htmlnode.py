from __future__ import annotations

type Props = dict[str, str|None]|None

class HTMLNode:
    def __init__(self, tag: str|None = None, value: str|None = None, children: list[HTMLNode]|None = None, props: Props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        dict_to_list = self.props.items()
        return " ".join([f'{key}="{value}"' for key, value in dict_to_list])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str|None, props: Props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return self.value
        return f"<{self.tag}{"" if self.props is None else " "}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str|None, children: list[HTMLNode], props: Props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("a tag is required")
        if self.children is None:
            raise ValueError("children are required")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}{"" if self.props is None else " "}{self.props_to_html()}>{child_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
