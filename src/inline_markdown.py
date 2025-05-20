import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes: list[TextNode] = []
        split = node.text.split(delimiter)
        #print(f"Splitting \"{node.text}\" by \"{delimiter}\" into {split}")
        if len(split) % 2 == 0:
            raise Exception("Delimiter is not balanced")
        for i in range(len(split)):
            if split[i] == "":
                    continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        extracted_links = extract_markdown_links(remaining_text)
        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue
        for link_text, link_url in extracted_links:
            sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections) != 2:
                raise Exception("Delimiter is not balanced")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        extracted_images = extract_markdown_images(remaining_text)
        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue
        for alt_text, img_link in extracted_images:
            sections = remaining_text.split(f"![{alt_text}]({img_link})", 1)
            if len(sections) != 2:
                raise Exception("Delimiter is not balanced")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_link))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str):
    nodes: list[TextNode] = []
    if text == "":
        return nodes
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes