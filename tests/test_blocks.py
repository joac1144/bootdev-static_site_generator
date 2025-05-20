import unittest
from src.blocks import BlockType, block_to_blocktype, markdown_to_blocks, markdown_to_html_node

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
    
    #region block_to_blocktype
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
    #endregion

    #region markdown_to_html_node
    def test_markdown_to_html_node_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_markdown_to_html_node_unordered_lists(self):
        md = """
- Normal Item 1
- Normal Item 2
- Italic _Item 3_

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Normal Item 1</li><li>Normal Item 2</li><li>Italic <i>Item 3</i></li></ul></div>",
        )

    def test_markdown_to_html_node_ordered_lists(self):
        md = """
1. Normal Item 1
2. Normal Item 2
3. Bolded _Item 3_

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Normal Item 1</li><li>Normal Item 2</li><li>Bolded <i>Item 3</i></li></ol></div>",
        )
    #endregion