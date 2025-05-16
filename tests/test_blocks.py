import unittest
from src.blocks import BlockType, block_to_blocktype, markdown_to_blocks

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
    
    def test_block_to_blocktype_paragraph(self):
        paragraph = "This is a paragraph."
        self.assertEqual(block_to_blocktype(paragraph), BlockType.PARAGRAPH)

    def test_block_to_blocktype_1_hash_returns_heading(self):
        heading = "# This is a heading"
        self.assertEqual(block_to_blocktype(heading), BlockType.HEADING)

    def test_block_to_blocktype_6_hashes_returns_heading(self):
        heading = "###### This is a heading"
        self.assertEqual(block_to_blocktype(heading), BlockType.HEADING)

    def test_block_to_blocktype_7_hashes_returns_paragrapg(self):
        heading = "####### This is a fake heading"
        self.assertEqual(block_to_blocktype(heading), BlockType.PARAGRAPH)

    def test_block_to_blocktype_triplebackticks_returns_code(self):
        code = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_blocktype(code), BlockType.CODE)

    def test_block_to_blocktype_triplebackticks_no_newlines_returns_code(self):
        code = "```print('Hello, World!')```"
        self.assertEqual(block_to_blocktype(code), BlockType.CODE)

    def test_block_to_blocktype_quote_returns_quote(self):
        quote = "> This is a quote"
        self.assertEqual(block_to_blocktype(quote), BlockType.QUOTE)
    
    def test_block_to_blocktype_quote_no_space_returns_quote(self):
        quote = ">This is a quote"
        self.assertEqual(block_to_blocktype(quote), BlockType.QUOTE)
    
    def test_block_to_blocktype_quote_multilines_returns_quote(self):
        quote = """
> This is a quote
> This is another quote
"""
        self.assertEqual(block_to_blocktype(quote), BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list_returns_unordered_list(self):
        unordered_list = """
- Item 1
- Item 2
- Item 3
"""
        self.assertEqual(block_to_blocktype(unordered_list), BlockType.UNORDERED_LIST)
    
    def test_block_to_blocktype_unordered_list_fake_line_returns_paragraph(self):
        unordered_list = """
- Item 1
- Item 2
This is not a list item
"""
        self.assertEqual(block_to_blocktype(unordered_list), BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list_returns_ordered_list(self):
        ordered_list = """
1. Item 1
2. Item 2
3. Item 3
"""
        self.assertEqual(block_to_blocktype(ordered_list), BlockType.ORDERED_LIST)

    def test_block_to_blocktype_ordered_list_fake_line_returns_paragraph(self):
        ordered_list = """
1. Item 1
2. Item 2
This is not a list item
"""
        self.assertEqual(block_to_blocktype(ordered_list), BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list_not_incrementing_returns_paragrapg(self):
        ordered_list = """
1. Item 1
2. Item 2
4. Item 3
"""
        self.assertEqual(block_to_blocktype(ordered_list), BlockType.PARAGRAPH)