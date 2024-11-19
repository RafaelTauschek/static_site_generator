import unittest
from markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links
)

from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is a test with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a test with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_delimiter_double_bold(self):
        node = TextNode("This is a **test** with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("test", TextType.BOLD),
                TextNode(" with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_delimiter_no_delimiter(self):
        node = TextNode("This is a node without delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a node without delimiter", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_delimiter_at_start(self):
        node = TextNode("**This** is a delimiter at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is a delimiter at the start", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_delimiter_at_end(self):
        node = TextNode("This is a delimiter at the **end**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a delimiter at the ", TextType.TEXT),
                TextNode("end", TextType.BOLD),
            ],
            new_nodes,
        )
        
    def test_delimiter_italic(self):
        node = TextNode("This is a test with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is a test with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_delimiter_mixed(self):
        node = TextNode("This is a **test** with *mixed* delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("test", TextType.BOLD),
                TextNode(" with ", TextType.TEXT),
                TextNode("mixed", TextType.ITALIC),
                TextNode(" delimiters", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_delimiter_code(self):
        node = TextNode("This is a `code block` test", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" test", TextType.TEXT),
            ],
            new_nodes,
        )
     
     
class TestExtractMarkdown(unittest.TestCase):
    def test_extract_links(self):
        text = "This is text with a link [to somewhere](https://to.somewhere.com)"
        extracted = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to somewhere", "https://to.somewhere.com")
            ],
            extracted,
        ),
        
    def test_extracted_links_multiple(self):
        text = "This is a link [to somewhere](https://to.somewhere.com) and another link [somewhere else](https://somewhere.else.com)"
        extracted = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to somewhere", "https://to.somewhere.com"),
                ("somewhere else", "https://somewhere.else.com"),
            ],
            extracted
        )
    
    
    def test_extract_images(self):
        text = "this is a image ![rick roll](https://i.imgur.com/asdqwdq.gif)"
        extracted = extract_markdown_images(text)
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/asdqwdq.gif"),
            ],
            extracted,
        )
    
    
    def test_extract_images_multiple(self):
        text = "this is a image ![rick roll](https://i.imgur.com/asdqwdq.gif) and another image ![spongebob meme](https://i.imgur.com/9a7sda9.jpeg)"
        extracted = extract_markdown_images(text)
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/asdqwdq.gif"),
                ("spongebob meme", "https://i.imgur.com/9a7sda9.jpeg"),
            ],
            extracted,
        )
    
    
       
   
        
if __name__ == '__main__':
    unittest.main()