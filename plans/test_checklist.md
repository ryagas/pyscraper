# Test Checklist for text_node_to_html_node

## High Priority - Basic Coverage

- [x] `test_bold()` - TextType.BOLD creates `<b>` tag
- [x] `test_italic()` - TextType.ITALIC creates `<i>` tag  
- [x] `test_code()` - TextType.CODE creates `<code>` tag
- [x] `test_link()` - TextType.LINK creates `<a>` tag with href prop
- [x] `test_image()` - TextType.IMAGE creates `<img>` tag with src/alt props
- [x] `test_invalid_text_type()` - Invalid type raises TypeError

## Medium Priority - Edge Cases

- [x] `test_empty_text()` - Empty string with TEXT type
- [x] `test_empty_bold()` - Empty string with BOLD type
- [x] `test_link_missing_url()` - LINK with None URL
- [x] `test_image_missing_url()` - IMAGE with None URL
- [x] `test_link_empty_text()` - LINK with empty text but valid URL

## Low Priority - Special Cases

- [x] `test_html_special_chars()` - Text with `<`, `>`, `&` characters
- [x] `test_special_chars_in_code()` - CODE with special characters
- [x] `test_unicode_text()` - Unicode/emoji support
- [x] `test_text_with_whitespace()` - Whitespace preservation
- [x] `test_text_with_newlines()` - Newline preservation
- [x] `test_image_empty_alt()` - IMAGE with empty alt but valid src
- [x] `test_long_text()` - Very long text (10,000+ chars)
