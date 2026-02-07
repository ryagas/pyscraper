import re
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


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.extend([node])
            continue
        image_list = extract_markdown_images(node.text)
        if len(image_list) == 0:
            new_nodes.extend([node])
            continue
        first_image = image_list[0]
        image_markdown = f"![{first_image[0]}]({first_image[1]})"

        parts = node.text.split(image_markdown, 1)

        if parts[0]:
            new_nodes.extend([TextNode(parts[0], TextType.TEXT)])

        new_nodes.extend([TextNode(first_image[0], TextType.IMAGE, first_image[1])])

        if parts[1]:
            results = split_nodes_image([TextNode(parts[1], TextType.TEXT)])
            new_nodes.extend(results)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.extend([node])
            continue
        link_list = extract_markdown_links(node.text)
        if len(link_list) == 0:
            new_nodes.extend([node])
            continue
        first_link = link_list[0]
        link_markdown = f"[{first_link[0]}]({first_link[1]})"
        parts = node.text.split(link_markdown, 1)

        if parts[0]:
            new_nodes.extend([TextNode(parts[0], TextType.TEXT)])

        new_nodes.extend([TextNode(first_link[0], TextType.LINK, first_link[1])])

        if parts[1]:
            results = split_nodes_link([TextNode(parts[1], TextType.TEXT)])
            new_nodes.extend(results)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # inline code first
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # bold
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # italic
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    # images
    nodes = split_nodes_image(nodes)
    # lastly, links
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    if not markdown:
        return []

    # blocks = SPLIT markdown by "\n\n"
    blocks = markdown.split("\n\n")

    # remove leading/trailing whitespace
    cleaned_blocks = []
    for block in blocks:
        trimmed_block = block.strip()

        if trimmed_block:
            cleaned_blocks.extend([trimmed_block])

    return cleaned_blocks
