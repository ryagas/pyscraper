import unittest
from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_single_bold(self):
        input_node = TextNode("This is **bold** text", TextType.TEXT)
        old_nodes = [input_node]
        delimiter = "**"
        text_type = TextType.BOLD

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_split_single_italic(self):
        input_node = TextNode("This is *italic* text", TextType.TEXT)
        old_nodes = [input_node]
        delimiter = "*"
        text_type = TextType.ITALIC

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_single_code(self):
        input_node = TextNode("This is `code` text", TextType.TEXT)
        old_nodes = [input_node]
        delimiter = "`"
        text_type = TextType.CODE

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_delimiter_at_start(self):
        input_node = TextNode("**bold** text", TextType.TEXT)
        old_nodes = [input_node]
        delimiter = "**"
        text_type = TextType.BOLD

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected = [TextNode("bold", TextType.BOLD), TextNode(" text", TextType.TEXT)]

        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        input_node = TextNode("This is **bold**", TextType.TEXT)
        old_nodes = [input_node]
        delimiter = "**"
        text_type = TextType.BOLD

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]

        self.assertEqual(result, expected)

    def test_only_delimited_text(self):
        input_node = TextNode("**bold**", TextType.TEXT)
        old_nodes = [input_node]
        delimiter = "**"
        text_type = TextType.BOLD

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)

        # Start and end sections are empty, only middle section remains
        expected = [TextNode("bold", TextType.BOLD)]

    def test_no_delimiters(self):
        input_node = TextNode("This is plain text", TextType.TEXT)
        old_nodes = [input_node]
        delimiter = "**"
        text_type = TextType.BOLD

        result = split_nodes_delimiter(old_nodes, delimiter, text_type)

        # No delimiters, so return original node
        expected = [TextNode("This is plain text", TextType.TEXT)]

        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
