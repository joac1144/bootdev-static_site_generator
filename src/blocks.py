from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    stripped = [block.strip() for block in blocks]
    return stripped

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