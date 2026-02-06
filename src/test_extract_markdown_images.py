import unittest
from textnode import TextNode, TextType
from utils import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("second image", "https://i.imgur.com/3elNhQu.png")
            ],
            matches
        )

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_links(self):
        # Make sure images are extracted but not regular links
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev")
            ],
            matches
        )

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This is text with no links"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_images(self):
        # Make sure links are extracted but not images
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_extract_markdown_links_empty_text(self):
        matches = extract_markdown_links(
            "This is text with a [](https://boot.dev)"
        )
        self.assertListEqual([("", "https://boot.dev")], matches)

    def test_extract_markdown_mixed(self):
        # Test complex text with both images and links
        text = "Here's a ![cat](cat.jpg) and a [website](https://example.com) and another ![dog](dog.png)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        
        self.assertListEqual(
            [("cat", "cat.jpg"), ("dog", "dog.png")],
            images
        )
        self.assertListEqual(
            [("website", "https://example.com")],
            links
        )
