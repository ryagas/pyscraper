import unittest
from utils import markdown_to_html_node
from htmlnode import ParentNode, LeafNode


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_empty_markdown_document(self):
        """Empty markdown document → empty div"""
        markdown = ""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(result.children, [])

    def test_single_paragraph(self):
        """Single paragraph → div with single p tag"""
        markdown = "This is a paragraph."
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        html = result.to_html()
        self.assertEqual(html, "<div><p>This is a paragraph.</p></div>")

    def test_multiple_paragraphs(self):
        """Multiple paragraphs → div with multiple p tags"""
        markdown = """First paragraph.

Second paragraph.

Third paragraph."""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        for child in result.children:
            self.assertEqual(child.tag, "p")
        html = result.to_html()
        self.assertIn("<p>First paragraph.</p>", html)
        self.assertIn("<p>Second paragraph.</p>", html)
        self.assertIn("<p>Third paragraph.</p>", html)

    def test_heading_conversion(self):
        """Heading conversion → proper h1-h6 tags with correct level"""
        markdown = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 6)

        # Check each heading level
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "h2")
        self.assertEqual(result.children[2].tag, "h3")
        self.assertEqual(result.children[3].tag, "h4")
        self.assertEqual(result.children[4].tag, "h5")
        self.assertEqual(result.children[5].tag, "h6")

        html = result.to_html()
        self.assertIn("<h1>Heading 1</h1>", html)
        self.assertIn("<h2>Heading 2</h2>", html)
        self.assertIn("<h3>Heading 3</h3>", html)

    def test_code_block(self):
        """Code block → pre>code structure with no inline processing"""
        markdown = """```
def hello():
    print("Hello, world!")
```"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)

        pre_node = result.children[0]
        self.assertEqual(pre_node.tag, "pre")
        self.assertEqual(len(pre_node.children), 1)

        code_node = pre_node.children[0]
        self.assertEqual(code_node.tag, "code")
        self.assertIn("def hello():", code_node.value)

        html = result.to_html()
        self.assertIn("<pre><code>", html)
        self.assertIn("def hello():", html)

    def test_quote_block(self):
        """Quote block → blockquote tag"""
        markdown = """>This is a quote.
>It spans multiple lines."""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)

        blockquote = result.children[0]
        self.assertEqual(blockquote.tag, "blockquote")

        html = result.to_html()
        self.assertIn("<blockquote>", html)
        self.assertIn("This is a quote.", html)
        self.assertIn("It spans multiple lines.", html)

    def test_unordered_list(self):
        """Unordered list → ul with multiple li tags"""
        markdown = """* First item
* Second item
* Third item"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)

        ul_node = result.children[0]
        self.assertEqual(ul_node.tag, "ul")
        self.assertEqual(len(ul_node.children), 3)

        for li in ul_node.children:
            self.assertEqual(li.tag, "li")

        html = result.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>First item</li>", html)
        self.assertIn("<li>Second item</li>", html)
        self.assertIn("<li>Third item</li>", html)

    def test_ordered_list(self):
        """Ordered list → ol with multiple li tags"""
        markdown = """1. First item
2. Second item
3. Third item"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)

        ol_node = result.children[0]
        self.assertEqual(ol_node.tag, "ol")
        self.assertEqual(len(ol_node.children), 3)

        for li in ol_node.children:
            self.assertEqual(li.tag, "li")

        html = result.to_html()
        self.assertIn("<ol>", html)
        self.assertIn("<li>First item</li>", html)
        self.assertIn("<li>Second item</li>", html)
        self.assertIn("<li>Third item</li>", html)

    def test_mixed_content(self):
        """Mixed content → all block types in one document"""
        markdown = """# Main Heading

This is a paragraph with some text.

## Subheading

Another paragraph here.

```
code block
```

>A quote block

* List item 1
* List item 2

1. Ordered item 1
2. Ordered item 2"""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 8)

        # Verify the structure
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[2].tag, "h2")
        self.assertEqual(result.children[3].tag, "p")
        self.assertEqual(result.children[4].tag, "pre")
        self.assertEqual(result.children[5].tag, "blockquote")
        self.assertEqual(result.children[6].tag, "ul")
        self.assertEqual(result.children[7].tag, "ol")

    def test_inline_markdown_in_blocks(self):
        """Inline markdown in blocks → bold, italic, code, links, images work correctly"""
        markdown = """This is **bold** and *italic* and `code`.

This has a [link](https://example.com) and an ![image](https://example.com/img.png)."""
        result = markdown_to_html_node(markdown)
        html = result.to_html()

        # Check bold
        self.assertIn("<b>bold</b>", html)
        # Check italic
        self.assertIn("<i>italic</i>", html)
        # Check code
        self.assertIn("<code>code</code>", html)
        # Check link
        self.assertIn('<a href="https://example.com">link</a>', html)
        # Check image
        self.assertIn('<img src="https://example.com/img.png" alt="image"></img>', html)

    def test_multi_line_quote(self):
        """Multi-line quote → joins lines properly"""
        markdown = """>Line one
>Line two
>Line three"""
        result = markdown_to_html_node(markdown)
        blockquote = result.children[0]
        self.assertEqual(blockquote.tag, "blockquote")

        html = result.to_html()
        # Lines should be joined with spaces
        self.assertIn("Line one Line two Line three", html)

    def test_multi_line_list_items(self):
        """Multi-line list items → each item is separate li"""
        markdown = """* Item one
* Item two
* Item three"""
        result = markdown_to_html_node(markdown)
        ul_node = result.children[0]
        self.assertEqual(len(ul_node.children), 3)

        # Each line should be a separate list item
        self.assertEqual(ul_node.children[0].tag, "li")
        self.assertEqual(ul_node.children[1].tag, "li")
        self.assertEqual(ul_node.children[2].tag, "li")

    def test_heading_with_inline_markdown(self):
        """Heading with inline markdown → processes inline formatting"""
        markdown = "## This is **bold** heading"
        result = markdown_to_html_node(markdown)
        html = result.to_html()

        self.assertIn("<h2>", html)
        self.assertIn("<b>bold</b>", html)

    def test_list_with_inline_markdown(self):
        """List items with inline markdown → processes inline formatting"""
        markdown = """* Item with **bold**
* Item with *italic*
* Item with `code`"""
        result = markdown_to_html_node(markdown)
        html = result.to_html()

        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)

    def test_quote_with_inline_markdown(self):
        """Quote with inline markdown → processes inline formatting"""
        markdown = """>This is a **bold** quote with *italic* text."""
        result = markdown_to_html_node(markdown)
        html = result.to_html()

        self.assertIn("<blockquote>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)


if __name__ == "__main__":
    unittest.main()
