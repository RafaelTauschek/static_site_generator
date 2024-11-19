import unittest

from textnode import TextNode, TextType

from textnode import (
    text_node_to_html_node,
)

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


class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_tag(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")


if __name__ == "__main__":
    unittest.main()