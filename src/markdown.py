from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        if delimiter in node.text:
            sections = node.text.split(delimiter)
            
            if len(sections) % 2 == 0:
                raise Exception("Invalid node, delimiter wasn't closed")

            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.extend([TextNode(sections[i], TextType.TEXT)])
                else:
                    new_nodes.extend([TextNode(sections[i], text_type)])
        else:
            new_nodes.append(TextNode(node.text, TextType.TEXT))
            
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches



def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches




def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text == "":
            continue
        
        image_nodes = extract_markdown_images(node.text)
        
        if len(image_nodes) == 0:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        for i in range(len(image_nodes)):
            splitted_text = original_text.split(f"![{image_nodes[i][0]}]({image_nodes[i][1]})", 1)
            if splitted_text[0] != "":
                new_nodes.extend([TextNode(splitted_text[0], TextType.TEXT)])
                new_nodes.extend([TextNode(image_nodes[i][0], TextType.IMAGE, image_nodes[i][1])])
                original_text = splitted_text[1]
            else:
                new_nodes.extend([TextNode(image_nodes[i][0], TextType.IMAGE, image_nodes[i][1])])
                original_text = splitted_text[0]
                
        if original_text:
            new_nodes.extend([TextNode(original_text, TextType.TEXT)])
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text == "":
            continue
        
        link_nodes = extract_markdown_links(node.text)
        
        if len(link_nodes) == 0:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        for i in range(len(link_nodes)):
            splitted_text = original_text.split(f"[{link_nodes[i][0]}]({link_nodes[i][1]})", 1)
            if splitted_text[0] != "":
                new_nodes.extend([TextNode(splitted_text[0], TextType.TEXT)])
                new_nodes.extend([TextNode(link_nodes[i][0], TextType.LINK, link_nodes[i][1])])
                original_text = splitted_text[1]
            else:
                new_nodes.extend([TextNode(link_nodes[i][0], TextType.LINK, link_nodes[i][1])])
                original_text = splitted_text[0]
                
        if original_text:
            new_nodes.extend([TextNode(original_text , TextType.TEXT)])
    return new_nodes


def text_to_textnode(text):
    node = TextNode(text, TextType.TEXT)
    bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "*", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    links = split_nodes_link(code)
    images = split_nodes_image(links)
    return images

def markdown_to_blocks(markdown):
    blocks = []
    splitted_by_whitespace = markdown.split('\n')
    block = ""
    
    for i in range(len(splitted_by_whitespace)):
        cleaned_block = splitted_by_whitespace[i].strip()
        if cleaned_block != "":
            if block:
                block += "\n"
            block += cleaned_block
        else:
            if block != "":
                blocks.append(block)
            block = ""
    if block != "":
        blocks.append(block)
    return blocks


def block_to_block_type(block):
    if block.startswith("#"):
        count = 0
        for character in block:
            if character == "#":
                count += 1
            else: 
                break
        if count <= 6 and block[count] == " ":
            return "heading"
        
    if block.startswith("```") and block[3] != "`" and block.endswith("```") and block[-4] != "`":
            return "code"
        
    if block.startswith(">"):
        splitted = block.split("\n")
        for line in splitted:
            if not line.startswith(">"):
                break
        else: return "quote"
    
    if block.startswith("*") or block.startswith("-"):
        splitted = block.split("\n")
        for line in splitted:
            if not line.startswith("* ") and not line.startswith("- "):
                break
        else: return "unordered_list"
        
    if block.startswith("1"):
        splitted = block.split("\n")
        for i, line in enumerate(splitted):
            if not line.startswith(f"{i + 1}. "):
                break
        else: return "ordered_list"
        
    return "paragraph"


def text_to_children(text):
    nodes = text_to_textnode(text)
    children = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "quote":
            html_nodes.append(quote_to_node(block))
        elif block_type == "unordered_list":
            html_nodes.append(unordered_list_to_node(block))
        elif block_type == "ordered_list":
            html_nodes.append(ordered_list_to_node(block))
        elif block_type == "code":
            html_nodes.append(code_to_node(block))
        elif block_type == "heading":
            html_nodes.append(heading_to_node(block))
        else:
            html_nodes.append(paragraph_to_node(block))

    return ParentNode("div", html_nodes)

def quote_to_node(text):
    quote_lines = []
    for line in text.split('\n'):
        if line.startswith('>'):
            clean_line = line[1:].strip()
            if clean_line:
                quote_lines.append(clean_line)
    quote_text = ' '.join(quote_lines)
    return ParentNode("blockquote", text_to_children(quote_text))

def code_to_node(text):
    text = text[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])
    

def paragraph_to_node(text):
    splitted_nodes = text.split("\n")
    paragraph = " ".join(splitted_nodes)
    return ParentNode("p", text_to_children(paragraph))


def heading_to_node(text):
    count = 0
    
    for character in text:
        if character == "#":
            count += 1
        else: break
        
    clean_text = text[count + 1:].strip()
    return ParentNode(f"h{count}", text_to_children(clean_text))


def ordered_list_to_node(text):
    splitted_nodes = text.split("\n")
    list_nodes = []
    for item_text in splitted_nodes:
        list_content = item_text[2:].strip()
        list_nodes.append(ParentNode("li", text_to_children(list_content)))
    return ParentNode("ol", list_nodes)


def unordered_list_to_node(text):
    splitted_nodes = text.split("\n")
    list_nodes = []
    for item_text in splitted_nodes:
        if item_text.startswith("* ") or item_text.startswith("- "):
            list_content = item_text[2:].strip()
            list_nodes.append(ParentNode("li", text_to_children(list_content)))
    return ParentNode("ul", list_nodes)