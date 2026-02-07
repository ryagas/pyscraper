import unittest

from utils import markdown_to_blocks


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks_empty(self):
        md = ""

        blocks = markdown_to_blocks(md)
        expected = []

        self.assertEqual(blocks, expected)

        md = None
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_single(self):
        md = "This is a single block"

        blocks = markdown_to_blocks(md)
        expected = [md]
        self.assertEqual(blocks, expected)

        md = "Line 1\nLine 2\nLine 3"

        blocks = markdown_to_blocks(md)
        expected = [md]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_3(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(
            blocks,
            expected,
        )

    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        ]
        self.assertEqual(
            blocks,
            expected,
        )
