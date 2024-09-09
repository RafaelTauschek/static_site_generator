import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a text node", "bold")
        node2 = LeafNode("p", "This is a text node", "bold")
        self.assertEqual(node.to_html(), node2.to_html())
        
    def test_to_html_no_value(self):
        node = LeafNode("h1", None, "italic")
        with self.assertRaises(ValueError): node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a text node", "italic")
        value = "This is a text node"
        self.assertEqual(node.to_html(), value)


if __name__ == "__main__":
    unittest.main()