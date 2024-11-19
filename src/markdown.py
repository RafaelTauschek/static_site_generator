from textnode import TextNode, TextType
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