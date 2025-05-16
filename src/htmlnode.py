from blocks import BlockType, markdown_to_blocks, block_to_blocktype

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
    
def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in blocks:
        block_node = block_to_html_node(block)
        block_nodes.append(block_node)

    return ParentNode("div", block_nodes)
        

def block_to_html_node(block: str):
    blocktype = block_to_blocktype(block)
    if blocktype == BlockType.PARAGRAPH:
        return ParentNode("p", text_to_children(block))
    elif blocktype == BlockType.HEADING:
        level = block.count("#")
        return ParentNode(f"h{level}", text_to_children(block))
    elif blocktype == BlockType.CODE:
        return ParentNode("pre", [LeafNode("code", block)])
    elif blocktype == BlockType.QUOTE:
        return ParentNode("blockquote", text_to_children(block))
    elif blocktype == BlockType.UNORDERED_LIST:
        return ParentNode("ul", text_to_children(block))
    elif blocktype == BlockType.ORDERED_LIST:
        return ParentNode("ol", text_to_children(block))
    else:
        raise Exception("Invalid block type")

def text_to_children(text: str):
    from helpers import text_to_textnodes
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node.to_html_node())
    return html_nodes