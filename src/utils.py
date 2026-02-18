from enum import Enum
import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("```\n") and block.rstrip().endswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    all_lines_start_with_quote = True
    for line in lines:
        if not (line.startswith(">")):
            all_lines_start_with_quote = False
            break
    if all_lines_start_with_quote:
        return BlockType.QUOTE

    all_lines_are_unordered = True
    for line in lines:
        if not (line.startswith("* ") or line.startswith("- ")):
            all_lines_are_unordered = False
            break
    if all_lines_are_unordered:
        return BlockType.UNORDERED_LIST

    all_lines_are_ordered = True
    expected_number = 1
    for line in lines:
        expected_prefix = str(expected_number) + ". "
        if not (line.startswith(expected_prefix)):
            all_lines_are_ordered = False
            break
        expected_number += 1
    if all_lines_are_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


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


def strip_numbered_prefix(block):
    return re.sub(r"^\d+\.\s*", "", block)


def strip_list_prefix(line):
    if line.startswith("* "):
        return line[2:]
    elif line.startswith("- "):
        return line[2:]
    return line


def join_lines_without_prefix(lines, prefix):
    stripped_lines = []
    for line in lines:
        if line.startswith(prefix):
            # Remove the prefix and any immediately following whitespace
            stripped_lines.append(line[len(prefix) :].lstrip())
        else:
            # If line doesn't have the prefix, keep it as is
            stripped_lines.append(line)

    return " ".join(stripped_lines)


def split_into_lines(block):
    return block.splitlines()


def strip_code_delimiters(block):
    result = block
    # Remove leading ```
    if result.startswith("```"):
        result = result[3:]

    # Remove trailing ```
    if result.endswith("```"):
        result = result[:-3]

    return result


def strip_heading_prefix(block):
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    # Skip the space after the hashes
    if i < len(block) and block[i] == " ":
        i += 1
    return block[i:]


def count_leading_hashes(block):
    count = 0
    for ch in block:
        if ch == "#":
            count += 1
        else:
            break
    return count


def text_to_child_nodes(text):
    # Convert text with inline markdown to list of HTMLNodes
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    # Process inline markdown in paragraph
    children = text_to_child_nodes(block)
    return ParentNode("p", children)


def heading_to_html_node(block):
    # Extract heading level (count # chars)
    level = count_leading_hashes(block)

    # Remove "### " prefix to get text
    text = strip_heading_prefix(block)

    # Process inline markdown
    children = text_to_child_nodes(text)

    # Return h1-h6 tag
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    # Remove ``` delimiters
    code_text = strip_code_delimiters(block)

    # Code blocks should not process inline markdown
    # Just wrap text in code tag, then in pre tag
    code_node = LeafNode("code", code_text)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    # Split into lines
    lines = split_into_lines(block)

    # Strip '>' from each line and join
    text = join_lines_without_prefix(lines, ">")

    # Process inline markdown in quote
    children = text_to_child_nodes(text)

    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    # Split into lines
    lines = split_into_lines(block)

    # Create list items
    list_items = []
    for line in lines:
        # Strip "* " or "- " prefix
        text = strip_list_prefix(line)

        # Process inline markdown in list item
        children = text_to_child_nodes(text)

        li_node = ParentNode("li", children)
        list_items.append(li_node)

    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    # Split into lines
    lines = split_into_lines(block)

    # Create list items
    list_items = []
    for line in lines:
        # Strip "1. ", "2. ", etc. prefix
        text = strip_numbered_prefix(line)

        # Process inline markdown in list item
        children = text_to_child_nodes(text)

        li_node = ParentNode("li", children)
        list_items.append(li_node)

    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """
    Converts a markdown document into a single parent HTMLNode.

    Args:
        markdown: String containing markdown document

    Returns:
        ParentNode with tag='div' containing child nodes for each block
    """
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Create list to hold child nodes for each block
    block_children = []

    # Process each block
    for block in blocks:
        # Determine block type
        block_type = block_to_block_type(block)

        # Convert block to HTMLNode based on type
        if block_type == BlockType.PARAGRAPH:
            child_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            child_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            child_node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            child_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            child_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            child_node = ordered_list_to_html_node(block)

        block_children.append(child_node)

    # Return parent div containing all blocks
    return ParentNode("div", block_children)
