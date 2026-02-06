import unittest
from textnode import TextNode, TextType
from utils import split_nodes_delimiter, split_nodes_image


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


class TestSplitNodesImage(unittest.TestCase):
    def test_case_image_middle_of_text(self):
        # Arrange
        input_node = TextNode(
            "Text before ![example image](https://example.com/example.gif) text after",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)  # or split_nodes_link

        # Assert
        expected_length = 3
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode(
                "example image", TextType.IMAGE, "https://example.com/example.gif"
            ),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), expected_length)

        # Optionally verify specific node properties
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/example.gif")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_case_image_beginning_of_text(self):
        # Arrange
        input_node = TextNode(
            "![example image](https://example.com/example.gif) text after",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected_length = 2
        expected = [
            TextNode(
                "example image", TextType.IMAGE, "https://example.com/example.gif"
            ),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), expected_length)

        # Optionally verify specific node properties
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "https://example.com/example.gif")
        self.assertEqual(result[1].text_type, TextType.TEXT)


if __name__ == "__main__":
    unittest.main()
