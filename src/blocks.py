import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")

    filtered_blocks: list[str] = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_blocktype(block: str):
    lines = block.strip().split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"^```.*```", block, flags=re.S):
        return BlockType.CODE
    elif all(re.match(r"^>", line) for line in lines):
        return BlockType.QUOTE
    elif all(re.match(r"^- ", line) for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(re.match(rf"^{i + 1}\. ", line) for i, line in enumerate(block.strip().split("\n"))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)

    block_nodes: list[HTMLNode] = []

    for block in blocks:
        block_node = block_to_html_node(block)
        block_nodes.append(block_node)

    return ParentNode("div", block_nodes)
        

def block_to_html_node(block: str):
    blocktype = block_to_blocktype(block)
    if blocktype == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif blocktype == BlockType.HEADING:
        return heading_to_html_node(block)
    elif blocktype == BlockType.CODE:
        return code_to_html_node(block)
    elif blocktype == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif blocktype == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif blocktype == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise Exception("Invalid block type")

def text_to_children(text: str):
    html_nodes: list[HTMLNode] = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def paragraph_to_html_node(block: str):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))

def heading_to_html_node(block: str):
    level = len(block)-len(block.lstrip('#'))
    text = block[level+1:]
    return ParentNode(f"h{level}", text_to_children(text))

def code_to_html_node(block: str):
    text = block.strip("```")
    text_node = TextNode(text, TextType.TEXT)
    as_html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [as_html_node])])

def quote_to_html_node(block: str):
    lines = block.split("\n")
    new_lines: list[str] = []
    for line in lines:
        if not line.startswith("> "):
            raise Exception("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = "\n".join(new_lines)
    return ParentNode("blockquote", text_to_children(text))

def unordered_list_to_html_node(block: str):
    lines = block.split("\n")
    html_items: list[HTMLNode] = []
    for line in lines:
        text = line.lstrip("- ")
        html_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", html_items)

def ordered_list_to_html_node(block: str):
    lines = block.split("\n")
    html_items: list[HTMLNode] = []
    for line in lines:
        text = line[3:]
        html_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", html_items)