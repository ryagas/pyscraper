import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_br(self):
        node = LeafNode("br", "Hello, world!")
        self.assertEqual(node.to_html(), "<br>Hello, world!</br>")

    def test_leaf_to_html_a_href(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://example.com">Hello, world!</a>'
        )

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "It's a PNG", {"src": "image.png"})
        self.assertEqual(node.to_html(), '<img src="image.png">It\'s a PNG</img>')
