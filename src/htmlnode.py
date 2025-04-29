class HTMLNode:
    def __init__(self, tag=None, value= None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        dict_to_list = self.props.items()
        return " ".join([f'{key}="{value}"' for key, value in dict_to_list])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return self.value
        return f"<{self.tag}{"" if self.props is None else " "}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
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