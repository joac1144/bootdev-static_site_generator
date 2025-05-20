import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_match(self):
        node = HTMLNode("tag1", "value1", None, {"key": "value"})
        node2 = HTMLNode("tag1", "value1", None, {"key": "value"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_props_to_html_neq(self):
        node = HTMLNode("tag1", "value1", None, {"key": "value"})
        node2 = HTMLNode("tag1", "value1", None, {"key": "value2"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

    def test_props_to_html_none(self):
        node = HTMLNode("tag1", "value1", None, None)
        node2 = HTMLNode("tag1", "value1", None, {})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    ### LeafNode tests
    def test_leafnode_to_html(self):
        node = LeafNode("div", "value1")
        self.assertEqual(node.to_html(), '<div>value1</div>')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a link!", {"href": "http://example.com"})
        self.assertEqual(node.to_html(), '<a href="http://example.com">This is a link!</a>')
    
    def test_leaf_to_html_value_none_raises_error(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    ### ParentNode tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )
    
    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
        

if __name__ == "__main__":
    unittest.main()