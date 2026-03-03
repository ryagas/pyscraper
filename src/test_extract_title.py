import unittest
from utils import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        """Test extracting a simple h1 title"""
        markdown = "# Hello World"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

    def test_extract_title_with_multiple_blocks(self):
        """Test extracting h1 when there are multiple blocks"""
        markdown = """# My Title

This is a paragraph.

## This is h2

Another paragraph."""
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")

    def test_extract_title_with_leading_whitespace(self):
        """Test extracting h1 with leading/trailing whitespace in markdown"""
        markdown = """

# Title with Spaces

Some content here."""
        result = extract_title(markdown)
        self.assertEqual(result, "Title with Spaces")

    def test_extract_title_with_inline_formatting(self):
        """Test extracting h1 that contains inline markdown"""
        markdown = "# Title with **bold** and *italic*"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with **bold** and *italic*")

    def test_extract_title_first_h1_only(self):
        """Test that only the first h1 is extracted when multiple exist"""
        markdown = """# First Title

Some content.

# Second Title

More content."""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

    def test_extract_title_ignores_h2(self):
        """Test that h2 headers are ignored"""
        markdown = """## This is h2

# This is h1"""
        result = extract_title(markdown)
        self.assertEqual(result, "This is h1")

    def test_extract_title_ignores_h3_to_h6(self):
        """Test that h3-h6 headers are ignored"""
        markdown = """### This is h3

#### This is h4

# This is h1"""
        result = extract_title(markdown)
        self.assertEqual(result, "This is h1")

    def test_extract_title_no_h1_raises_exception(self):
        """Test that missing h1 raises an exception"""
        markdown = """## This is h2

This is a paragraph.

### This is h3"""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")

    def test_extract_title_empty_markdown_raises_exception(self):
        """Test that empty markdown raises an exception"""
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")

    def test_extract_title_only_whitespace_raises_exception(self):
        """Test that markdown with only whitespace raises an exception"""
        markdown = "   \n\n   "
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")

    def test_extract_title_hash_without_space_not_h1(self):
        """Test that # without space is not recognized as h1"""
        markdown = """#NoSpace

# Proper H1"""
        result = extract_title(markdown)
        self.assertEqual(result, "Proper H1")

    def test_extract_title_with_special_characters(self):
        """Test extracting h1 with special characters"""
        markdown = "# Title with $pecial Ch@racters & Symbols!"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with $pecial Ch@racters & Symbols!")

    def test_extract_title_with_numbers(self):
        """Test extracting h1 with numbers"""
        markdown = "# Chapter 1: Introduction to Python 3.11"
        result = extract_title(markdown)
        self.assertEqual(result, "Chapter 1: Introduction to Python 3.11")

    def test_extract_title_multiline_block(self):
        """Test that h1 in a multiline block is extracted correctly"""
        markdown = """# Title
on multiple
lines

Paragraph here."""
        result = extract_title(markdown)
        # The title should include everything after "# " in that block
        self.assertEqual(result, "Title\non multiple\nlines")


if __name__ == "__main__":
    unittest.main()
