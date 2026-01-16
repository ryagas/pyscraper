# Test Checklist for text_node_to_html_node

## High Priority - Basic Coverage

- [ ] `test_bold()` - TextType.BOLD creates `<b>` tag
- [ ] `test_italic()` - TextType.ITALIC creates `<i>` tag  
- [ ] `test_code()` - TextType.CODE creates `<code>` tag
- [ ] `test_link()` - TextType.LINK creates `<a>` tag with href prop
- [ ] `test_image()` - TextType.IMAGE creates `<img>` tag with src/alt props
- [ ] `test_invalid_text_type()` - Invalid type raises TypeError

## Medium Priority - Edge Cases

- [ ] `test_empty_text()` - Empty string with TEXT type
- [ ] `test_empty_bold()` - Empty string with BOLD type
- [ ] `test_link_missing_url()` - LINK with None URL
- [ ] `test_image_missing_url()` - IMAGE with None URL
- [ ] `test_link_empty_text()` - LINK with empty text but valid URL

## Low Priority - Special Cases

- [ ] `test_html_special_chars()` - Text with `<`, `>`, `&` characters
- [ ] `test_special_chars_in_code()` - CODE with special characters
- [ ] `test_unicode_text()` - Unicode/emoji support
- [ ] `test_text_with_whitespace()` - Whitespace preservation
- [ ] `test_text_with_newlines()` - Newline preservation
- [ ] `test_image_empty_alt()` - IMAGE with empty alt but valid src
- [ ] `test_long_text()` - Very long text (10,000+ chars)
