import unittest

from textnode import TextNode, TextType
from utils import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        input = "plain text"
        result = text_to_textnodes(input)
        expected = [TextNode("plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_bold(self):
        input = "text with **bold** section"
        result = text_to_textnodes(input)
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" section", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_italic(self):
        input = "text with *italic* section"
        result = text_to_textnodes(input)
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" section", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_code(self):
        input = "text with `code` section"
        result = text_to_textnodes(input)
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" section", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_link(self):
        input = "text with [link text](https://url.com) section"
        result = text_to_textnodes(input)
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "https://url.com"),
            TextNode(" section", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_single_image(self):
        input = "text with ![alt text](https://image.png) section"
        result = text_to_textnodes(input)
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://image.png"),
            TextNode(" section", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
