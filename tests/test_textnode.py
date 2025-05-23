import unittest
from src.textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    #region Comparing text nodes
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "testurl.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "testurl.com")
        self.assertEqual(node, node2)
    
    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_texttype_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "url1")
        node2 = TextNode("This is a text node", TextType.CODE, "url2")
        self.assertNotEqual(node, node2)
    #endregion

    #region text_node_to_html_node
    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
    
    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "http://example.com"})
    #endregion
    

if __name__ == "__main__":
    unittest.main()