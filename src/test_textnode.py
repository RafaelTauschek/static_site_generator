import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        self.assertEqual(node.text, node2.text)
        self.assertEqual(node.url, node2.url)
        self.assertEqual(node.text_type, node2.text_type)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is not a text node", "italic", 'test.de')
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node.text, node2.text)
        self.assertNotEqual(node.url, node2.url)
        
    def test_default_url(self):
        node = TextNode('This is a text node', "italic")
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()