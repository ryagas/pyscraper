import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            str(node), 'TextNode("This is a text node", TextType.BOLD, None)'
        )

    def test_none_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, TextNode("This is a text node", TextType.BOLD, None))

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://localhost")
        node2 = TextNode(
            "This is a different text node", TextType.BOLD, "https://localhost"
        )
        node3 = TextNode(
            "This is a different text node", TextType.ITALIC, "https://localhost"
        )
        node4 = TextNode(
            "This is a different text node", TextType.ITALIC, "https://apple.com"
        )
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node4)


if __name__ == "__main__":
    unittest.main()
