import unittest
from utils import (
    text_to_child_nodes,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
)
from htmlnode import LeafNode, ParentNode


class TestTextToChildNodes(unittest.TestCase):
    def test_plain_text(self):
        """text_to_child_nodes converts plain text correctly"""
        text = "Just plain text"
        result = text_to_child_nodes(text)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], LeafNode)
        self.assertEqual(result[0].value, "Just plain text")

    def test_bold_text(self):
        """text_to_child_nodes converts bold text correctly"""
        text = "This is **bold** text"
        result = text_to_child_nodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, "This is ")
        self.assertEqual(result[1].tag, "b")
        self.assertEqual(result[1].value, "bold")
        self.assertEqual(result[2].value, " text")

    def test_italic_text(self):
        """text_to_child_nodes converts italic text correctly"""
        text = "This is *italic* text"
        result = text_to_child_nodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].tag, "i")
        self.assertEqual(result[1].value, "italic")

    def test_code_text(self):
        """text_to_child_nodes converts inline code correctly"""
        text = "This is `code` text"
        result = text_to_child_nodes(text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].tag, "code")
        self.assertEqual(result[1].value, "code")

    def test_link(self):
        """text_to_child_nodes converts links correctly"""
        text = "This is a [link](https://example.com)"
        result = text_to_child_nodes(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].tag, "a")
        self.assertEqual(result[1].value, "link")
        self.assertEqual(result[1].props["href"], "https://example.com")

    def test_image(self):
        """text_to_child_nodes converts images correctly"""
        text = "This is an ![image](https://example.com/img.png)"
        result = text_to_child_nodes(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].tag, "img")
        self.assertEqual(result[1].props["src"], "https://example.com/img.png")
        self.assertEqual(result[1].props["alt"], "image")

    def test_mixed_inline_markdown(self):
        """text_to_child_nodes converts mixed inline markdown correctly"""
        text = "**bold** and *italic* and `code`"
        result = text_to_child_nodes(text)
        # Should have: bold, " and ", italic, " and ", code
        self.assertGreater(len(result), 3)
        # Check that we have bold, italic, and code tags
        tags = [node.tag for node in result]
        self.assertIn("b", tags)
        self.assertIn("i", tags)
        self.assertIn("code", tags)


class TestParagraphToHTMLNode(unittest.TestCase):
    def test_simple_paragraph(self):
        """paragraph_to_html_node creates p tag with plain text"""
        block = "This is a simple paragraph."
        result = paragraph_to_html_node(block)
        self.assertEqual(result.tag, "p")
        self.assertIsNotNone(result.children)
        html = result.to_html()
        self.assertEqual(html, "<p>This is a simple paragraph.</p>")

    def test_paragraph_with_inline_markdown(self):
        """paragraph_to_html_node creates p tag with inline content"""
        block = "This has **bold** text."
        result = paragraph_to_html_node(block)
        self.assertEqual(result.tag, "p")
        html = result.to_html()
        self.assertIn("<b>bold</b>", html)


class TestHeadingToHTMLNode(unittest.TestCase):
    def test_h1_heading(self):
        """heading_to_html_node extracts level 1 correctly"""
        block = "# Heading 1"
        result = heading_to_html_node(block)
        self.assertEqual(result.tag, "h1")
        html = result.to_html()
        self.assertIn("Heading 1", html)

    def test_h2_heading(self):
        """heading_to_html_node extracts level 2 correctly"""
        block = "## Heading 2"
        result = heading_to_html_node(block)
        self.assertEqual(result.tag, "h2")
        html = result.to_html()
        self.assertIn("Heading 2", html)

    def test_h3_heading(self):
        """heading_to_html_node extracts level 3 correctly"""
        block = "### Heading 3"
        result = heading_to_html_node(block)
        self.assertEqual(result.tag, "h3")
        html = result.to_html()
        self.assertIn("Heading 3", html)

    def test_h6_heading(self):
        """heading_to_html_node extracts level 6 correctly"""
        block = "###### Heading 6"
        result = heading_to_html_node(block)
        self.assertEqual(result.tag, "h6")
        html = result.to_html()
        self.assertIn("Heading 6", html)

    def test_heading_with_inline_markdown(self):
        """heading_to_html_node processes inline markdown in heading text"""
        block = "## This is **bold** heading"
        result = heading_to_html_node(block)
        self.assertEqual(result.tag, "h2")
        html = result.to_html()
        self.assertIn("<b>bold</b>", html)


class TestCodeToHTMLNode(unittest.TestCase):
    def test_simple_code_block(self):
        """code_to_html_node preserves raw text without inline processing"""
        block = """```
def hello():
    print("Hello")
```"""
        result = code_to_html_node(block)
        self.assertEqual(result.tag, "pre")
        self.assertEqual(len(result.children), 1)

        code_node = result.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertIn("def hello():", code_node.value)
        self.assertIn('print("Hello")', code_node.value)

    def test_code_block_no_inline_processing(self):
        """code_to_html_node does not process markdown in code"""
        block = """```
This has **bold** but it should not be processed
```"""
        result = code_to_html_node(block)
        code_node = result.children[0]
        # Should contain the raw ** characters, not <b> tags
        self.assertIn("**bold**", code_node.value)
        html = result.to_html()
        self.assertNotIn("<b>", html)


class TestQuoteToHTMLNode(unittest.TestCase):
    def test_single_line_quote(self):
        """quote_to_html_node strips > prefix"""
        block = ">This is a quote."
        result = quote_to_html_node(block)
        self.assertEqual(result.tag, "blockquote")
        html = result.to_html()
        self.assertIn("This is a quote.", html)
        # Check that the markdown > prefix is not in the content (not counting HTML tags)
        self.assertEqual(html, "<blockquote>This is a quote.</blockquote>")

    def test_multi_line_quote(self):
        """quote_to_html_node strips > prefix and joins lines"""
        block = """>Line one
>Line two
>Line three"""
        result = quote_to_html_node(block)
        self.assertEqual(result.tag, "blockquote")
        html = result.to_html()
        # Lines should be joined with spaces
        self.assertIn("Line one", html)
        self.assertIn("Line two", html)
        self.assertIn("Line three", html)

    def test_quote_with_inline_markdown(self):
        """quote_to_html_node processes inline markdown"""
        block = ">This is **bold** quote."
        result = quote_to_html_node(block)
        html = result.to_html()
        self.assertIn("<b>bold</b>", html)


class TestUnorderedListToHTMLNode(unittest.TestCase):
    def test_asterisk_list(self):
        """unordered_list_to_html_node strips * prefix"""
        block = """* Item 1
* Item 2
* Item 3"""
        result = unordered_list_to_html_node(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 3)

        for li in result.children:
            self.assertEqual(li.tag, "li")

        html = result.to_html()
        self.assertIn("<li>Item 1</li>", html)
        self.assertIn("<li>Item 2</li>", html)
        self.assertIn("<li>Item 3</li>", html)

    def test_dash_list(self):
        """unordered_list_to_html_node strips - prefix"""
        block = """- Item 1
- Item 2"""
        result = unordered_list_to_html_node(block)
        self.assertEqual(result.tag, "ul")
        self.assertEqual(len(result.children), 2)
        html = result.to_html()
        self.assertIn("<li>Item 1</li>", html)

    def test_list_with_inline_markdown(self):
        """unordered_list_to_html_node processes inline markdown in items"""
        block = """* Item with **bold**
* Item with *italic*"""
        result = unordered_list_to_html_node(block)
        html = result.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)


class TestOrderedListToHTMLNode(unittest.TestCase):
    def test_simple_ordered_list(self):
        """ordered_list_to_html_node strips numbered prefix"""
        block = """1. First item
2. Second item
3. Third item"""
        result = ordered_list_to_html_node(block)
        self.assertEqual(result.tag, "ol")
        self.assertEqual(len(result.children), 3)

        for li in result.children:
            self.assertEqual(li.tag, "li")

        html = result.to_html()
        self.assertIn("<li>First item</li>", html)
        self.assertIn("<li>Second item</li>", html)
        self.assertIn("<li>Third item</li>", html)

    def test_ordered_list_with_inline_markdown(self):
        """ordered_list_to_html_node processes inline markdown in items"""
        block = """1. Item with **bold**
2. Item with `code`"""
        result = ordered_list_to_html_node(block)
        html = result.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<code>code</code>", html)


if __name__ == "__main__":
    unittest.main()
