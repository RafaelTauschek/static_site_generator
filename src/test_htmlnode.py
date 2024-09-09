import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_is_none(self):
        node1 = HTMLNode("p", "This is a test parapraph")
        node2 = HTMLNode("p", "This is a test parapraph")
        
        self.assertIsNone(node1.children)
        self.assertIsNone(node1.props)
        self.assertIsNone(node2.children)
        self.assertIsNone(node2.props)
        
    def test_not_eq(self):
        node1 = HTMLNode("p", "This is a test parapraph")
        node2 = HTMLNode("h1", "This is a header")
        
        self.assertNotEqual(node1, node2)
        
        
        
class TestParentNode(unittest.TestCase):
    
    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        
        string = node.to_html()
        print(string)

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        
        
if __name__ == "__main__":
    unittest.main()
    