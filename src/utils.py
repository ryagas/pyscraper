from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise TypeError
    if text_node.text_type is TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type is TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type is TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type is TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type is TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type is TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            # Pass through non-TEXT nodes unchanged
            new_nodes.extend([node])
            continue
        
        # Process TEXT nodes
        split_result = split_text_by_delimiter(node.text, delimiter, text_type)
        new_nodes.extend(split_result)
    return new_nodes


def split_text_by_delimiter(text, delimiter, text_type):
    """
    Split a single text string by delimiter pairs.
    
    Args:
        text: String to split
        delimiter: Delimiter to split by
        text_type: TextType to assign to text between delimiters
    
    Returns:
        List of TextNode objects
    """
    result_nodes = []
    
    # Validate delimiter pairing
    delimiter_count = text.count(delimiter)
    if delimiter_count % 2 != 0:
        raise ValueError("Invalid markdown: unclosed delimiter")
    
    # If no delimiters, return original text as-is
    if delimiter_count == 0:
        return [TextNode(text, TextType.TEXT)]
    
    # Split the text by delimiter
    sections = text.split(delimiter)
    
    # Process sections: alternating between TEXT and the new text_type
    is_inside_delimiter = False
    
    for section in sections:
        if section == "":
            # Toggle state even for empty sections
            is_inside_delimiter = not is_inside_delimiter
            continue
        
        if is_inside_delimiter:
            # Text between delimiters gets the new text_type
            result_nodes.append(TextNode(section, text_type))
        else:
            # Text outside delimiters remains TEXT
            result_nodes.append(TextNode(section, TextType.TEXT))
        
        # Toggle the state
        is_inside_delimiter = not is_inside_delimiter
    
    return result_nodes

