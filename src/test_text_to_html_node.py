import unittest

from textnode import TextNode, TextType
from utils import text_node_to_html_node


class TestTextNodeToHTML(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    # ── High Priority - Basic Coverage ──

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/img.png", "alt": "alt text"},
        )

    def test_invalid_text_type(self):
        node = TextNode("bad", TextType.TEXT)
        node.text_type = "not_a_real_type"
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

    # ── Medium Priority - Edge Cases ──

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")

    def test_empty_bold(self):
        node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "")

    def test_link_missing_url(self):
        node = TextNode("click here", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": None})

    def test_image_missing_url(self):
        node = TextNode("alt text", TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": None, "alt": "alt text"})

    def test_link_empty_text(self):
        node = TextNode("", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    # ── Low Priority - Special Cases ──

    def test_html_special_chars(self):
        node = TextNode("<div>hello</div> & 'world'", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "<div>hello</div> & 'world'")

    def test_special_chars_in_code(self):
        node = TextNode("if x < 10 && y > 5", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "if x < 10 && y > 5")

    def test_unicode_text(self):
        node = TextNode("Hello 🌍 café naïve", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "Hello 🌍 café naïve")

    def test_text_with_whitespace(self):
        node = TextNode("  hello   world  ", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "  hello   world  ")

    def test_text_with_newlines(self):
        node = TextNode("line one\nline two\nline three", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "line one\nline two\nline three")

    def test_image_empty_alt(self):
        node = TextNode("", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/img.png", "alt": ""},
        )

    def test_long_text(self):
        long_string = "a" * 10000
        node = TextNode(long_string, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, long_string)
        self.assertEqual(len(html_node.value), 10000)


if __name__ == "__main__":
    unittest.main()
