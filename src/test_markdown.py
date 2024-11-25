import unittest
from markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnode,
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
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

    
class TestSplitNodes(unittest.TestCase):
    def test_split_node_images(self):
        node1 = TextNode("This is a image ![rick roll](https://i.imgur.com/asdqwdq.gif)", TextType.TEXT)
        new_nodes1 = split_nodes_image([node1])
        self.assertListEqual(
            [
                TextNode("This is a image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/asdqwdq.gif"),
            ],
            new_nodes1,
        )
        
        node2 = TextNode("This is a image ![rick roll](https://i.imgur.com/asdqwdq.gif) with text at the end", TextType.TEXT)
        new_node2 = split_nodes_image([node2])
        self.assertListEqual(
            [
                TextNode("This is a image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/asdqwdq.gif"),
                TextNode(" with text at the end", TextType.TEXT),
            ],
            new_node2,
        )
        

    def test_split_node_images_multiple(self):
        node = TextNode("This is a image ![rick roll](https://i.imgur.com/asdqwdq.gif) and another image ![spongebob meme](https://i.imgur.com/9a7sda9.jpeg)", TextType.TEXT)
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a image ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/asdqwdq.gif"),
                TextNode(" and another image ", TextType.TEXT),
                TextNode("spongebob meme", TextType.IMAGE, "https://i.imgur.com/9a7sda9.jpeg"),
            ],
            new_node,
        )
    

    def test_split_node_links(self):
        node1 = TextNode("This is text with a link [to somewhere](https://to.somewhere.com)", TextType.TEXT)
        new_nodes1 = split_nodes_link([node1])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to somewhere", TextType.LINK, "https://to.somewhere.com"),
            ],
            new_nodes1
        )
        
        node2 = TextNode("This is text with a link [to somewhere](https://to.somewhere.com) with text at the end", TextType.TEXT)
        new_nodes2 = split_nodes_link([node2])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to somewhere", TextType.LINK, "https://to.somewhere.com"),
                TextNode(" with text at the end", TextType.TEXT),
            ],
            new_nodes2
        )
    
    def test_split_node_links_multiple(self):
        node = TextNode("This is text with a link [to somewhere](https://to.somewhere.com) and [to elsewhere](https://to.elsewhere.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to somewhere", TextType.LINK, "https://to.somewhere.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to elsewhere", TextType.LINK, "https://to.elsewhere.com"),
            ],
            new_nodes,
        )
    
class TestTextToNodes(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
    
 
class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        raw_md = """## Wizard's Guide
        
        A wizzard is never late, nor early.
        
        * Bring your staff
        * Pack some lembas bread
        * Don't forget your hat"""

        blocks = markdown_to_blocks(raw_md)
        self.assertListEqual(
            [
                "## Wizard's Guide",
                "A wizzard is never late, nor early.",
                "* Bring your staff\n* Pack some lembas bread\n* Don't forget your hat"
            ],
            blocks,
        )    
        

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_paragraph_type(self):
        text = "This is just 1. Paragraph without any special type"
        paragraph = block_to_block_type(text)
        self.assertEqual("paragraph", paragraph)
        
    def test_block_to_heading_type(self):
        text = "### This is a heading"
        heading = block_to_block_type(text)
        self.assertEqual("heading", heading)
        
    def test_block_to_code_type(self):
        text = "```This is a code block```"
        code = block_to_block_type(text)
        self.assertEqual("code", code)
        
    def test_block_to_quote_type(self):
        text = ">This is a quote\n>even with\n>newlines"
        quote = block_to_block_type(text)
        self.assertEqual("quote", quote)
        
    def test_block_to_unordered_list_type(self):
        text = "* This is an\n- unordered list with\n* or - as character"
        unordered_list = block_to_block_type(text)
        self.assertEqual("unordered_list", unordered_list)
        
    def test_block_to_ordered_list_type(self):
        text = "1. This is and ordered\n2. List that increment\n3. The number every time"
        ordered_list = block_to_block_type(text)
        self.assertEqual("ordered_list", ordered_list)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_paragraph(self):
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

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
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

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
    
    
    
    
    
if __name__ == '__main__':
    unittest.main()