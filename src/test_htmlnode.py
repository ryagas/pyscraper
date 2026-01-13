import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("h1", "Hello World!\n")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "Apple's homepage", None, {"href": "https://apple.com"})
        self.assertEqual(node.props_to_html(), f' href="https://apple.com"')

    def test_repr(self):
        node = HTMLNode(
            "img", "This is an image", None, {"src": "image.png", "alt": "an image"}
        )
        self.assertEqual(
            "HTMLNode(\"img\", \"This is an image\", {'src': 'image.png', 'alt': 'an image'})",
            f"{node}",
        )
