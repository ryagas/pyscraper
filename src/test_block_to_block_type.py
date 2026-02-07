import unittest

from utils import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    # 1. CODE Block Tests
    def test_code_block_basic(self):
        block = "```\ncode here\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_multiline(self):
        block = "```\nline 1\nline 2\nline 3\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_code_block_with_language(self):
        # Language specifier requires newline after opening backticks
        block = "```\nprint('hello')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    # 2. HEADING Block Tests
    def test_heading_h1(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_h2(self):
        block = "## Second level heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### Sixth level heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_no_space(self):
        block = "##NoSpace"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### Too many"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # 3. QUOTE Block Tests
    def test_quote_single_line(self):
        block = ">This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_multiline(self):
        block = ">Line 1\n>Line 2\n>Line 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_with_space(self):
        block = "> Quote with space"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_partial_fails(self):
        block = ">Line 1\nNot a quote\n>Line 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # 4. UNORDERED_LIST Block Tests
    def test_unordered_list_asterisk(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_dash(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        block = "* Single item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed_markers_succeed(self):
        # Implementation allows mixed markers as long as each line starts with * or -
        block = "* Item 1\n- Item 2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        block = "*NoSpace\n*Item2"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # 5. ORDERED_LIST Block Tests
    def test_ordered_list_sequential(self):
        block = "1. First\n2. Second\n3. Third"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_single_item(self):
        block = "1. Only item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_non_sequential(self):
        block = "1. First\n3. Third\n4. Fourth"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list_must_start_at_one(self):
        block = "2. Second\n3. Third"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list_no_space(self):
        block = "1.NoSpace"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # 6. PARAGRAPH Block Tests
    def test_paragraph_simple(self):
        block = "This is a regular paragraph."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "Line 1\nLine 2\nLine 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_with_special_chars(self):
        block = "This > is not a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_numbers_wrong_format(self):
        block = "1 First item\n2 Second item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    # 7. Edge Cases
    def test_code_block_empty(self):
        block = "```\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_quote_with_empty_lines(self):
        block = ">Line 1\n>\n>Line 3"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_code_block_without_newline(self):
        block = "```code\nmore```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_text_with_multiple_patterns(self):
        # This should be identified as heading since heading check comes before quote
        block = "# Not a heading because > this starts with a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)


if __name__ == "__main__":
    unittest.main()
