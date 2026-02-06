import unittest
from textnode import TextNode, TextType
from utils import split_nodes_delimiter, split_nodes_image, split_nodes_link


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
    def test_single_image_middle_of_text(self):
        # Arrange
        input_node = TextNode(
            "Text before ![alt](url) text after",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_image_at_start(self):
        # Arrange
        input_node = TextNode(
            "![alt](url) text after",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)

    def test_image_at_end(self):
        # Arrange
        input_node = TextNode(
            "Text before ![alt](url)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)

    def test_only_image(self):
        # Arrange
        input_node = TextNode(
            "![alt](url)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)

    def test_multiple_images(self):
        # Arrange
        input_node = TextNode(
            "![alt1](url1) middle ![alt2](url2)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_no_images(self):
        # Arrange
        input_node = TextNode(
            "Plain text with no images",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("Plain text with no images", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)

    def test_empty_alt_text(self):
        # Arrange
        input_node = TextNode(
            "Text ![](url) more",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "url"),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_empty_url(self):
        # Arrange
        input_node = TextNode(
            "Text ![alt]() more",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, ""),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_non_text_node_input(self):
        # Arrange
        input_node = TextNode("bold text", TextType.BOLD)
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)

    def test_empty_list(self):
        # Arrange
        old_nodes = []

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = []
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 0)

    def test_mixed_node_types(self):
        # Arrange
        old_nodes = [
            TextNode("plain text with ![image](url)", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("another ![img](url2) text", TextType.TEXT),
        ]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("plain text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode("bold text", TextType.BOLD),
            TextNode("another ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url2"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_adjacent_images(self):
        # Arrange
        input_node = TextNode(
            "![alt1](url1)![alt2](url2)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_image(old_nodes)

        # Assert
        expected = [
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode("alt2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link_middle_of_text(self):
        # Arrange
        input_node = TextNode(
            "Text before [link text](url) text after",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "url"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_link_at_start(self):
        # Arrange
        input_node = TextNode(
            "[link text](url) text after",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("link text", TextType.LINK, "url"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)

    def test_link_at_end(self):
        # Arrange
        input_node = TextNode(
            "Text before [link text](url)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "url"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)

    def test_only_link(self):
        # Arrange
        input_node = TextNode(
            "[link text](url)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("link text", TextType.LINK, "url"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)

    def test_multiple_links(self):
        # Arrange
        input_node = TextNode(
            "[link1](url1) middle [link2](url2)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_no_links(self):
        # Arrange
        input_node = TextNode(
            "Plain text with no links",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("Plain text with no links", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)

    def test_empty_link_text(self):
        # Arrange
        input_node = TextNode(
            "Text [](url) more",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("", TextType.LINK, "url"),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_empty_url(self):
        # Arrange
        input_node = TextNode(
            "Text [link text]() more",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("link text", TextType.LINK, ""),
            TextNode(" more", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_non_text_node_input(self):
        # Arrange
        input_node = TextNode("bold text", TextType.BOLD)
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)

    def test_empty_list(self):
        # Arrange
        old_nodes = []

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = []
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 0)

    def test_mixed_node_types(self):
        # Arrange
        old_nodes = [
            TextNode("plain text with [link](url)", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("another [link2](url2) text", TextType.TEXT),
        ]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("plain text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("bold text", TextType.BOLD),
            TextNode("another ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_adjacent_links(self):
        # Arrange
        input_node = TextNode(
            "[link1](url1)[link2](url2)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)

    def test_link_next_to_image(self):
        # Arrange
        input_node = TextNode(
            "[link](url) and ![image](url)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert - split_nodes_link should only process the link
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and ![image](url)", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_image_markdown_not_matched(self):
        # Arrange
        input_node = TextNode(
            "This is an ![image](url) not a link",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act
        result = split_nodes_link(old_nodes)

        # Assert - image syntax should be ignored by split_nodes_link
        expected = [
            TextNode("This is an ![image](url) not a link", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 1)


class TestIntegration(unittest.TestCase):
    def test_links_and_images_together(self):
        # Arrange
        input_node = TextNode(
            "Check [this link](url1) and ![this image](url2) out",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act - process with split_nodes_link first, then split_nodes_image
        result_after_links = split_nodes_link(old_nodes)
        result = split_nodes_image(result_after_links)

        # Assert
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("this link", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("this image", TextType.IMAGE, "url2"),
            TextNode(" out", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 5)

    def test_complex_mixed_content(self):
        # Arrange
        input_node = TextNode(
            "[link1](url1) text ![img1](url2) more [link2](url3)",
            TextType.TEXT,
        )
        old_nodes = [input_node]

        # Act - process with split_nodes_link first, then split_nodes_image
        result_after_links = split_nodes_link(old_nodes)
        result = split_nodes_image(result_after_links)

        # Assert
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" text ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url2"),
            TextNode(" more ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url3"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
