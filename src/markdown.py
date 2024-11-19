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



