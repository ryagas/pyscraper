import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # Test that ValueError is raised when tag is None
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    # Test that ValueError is raised when children is None
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    # Test with HTML attributes (props)
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(), '<div class="container"><span>child</span></div>'
        )

    # Test with multiple props
    def test_to_html_with_multiple_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            "div", [child_node], {"class": "container", "id": "main"}
        )
        # Expected: <div class="container" id="main"><span>child</span></div>
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )
