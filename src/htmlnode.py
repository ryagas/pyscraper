class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or self.props == {}:
            return ""
        result = ""
        for prop in self.props.keys():
            result += f' {prop}="{self.props[prop]}"'
        return result

    def __repr__(self):
        result = ""
        result += "HTMLNode("
        result += f'"{self.tag if self.tag else ""}", '
        result += f'"{self.value if self.value else ""}", '
        if self.value is None or self.value == "":
            if self.children:
                result += "["
                for child in self.children:
                    result += f"{str(child)},\n"
                result += "], "
            else:
                result += "None, "
        result += f"{self.props})"
        return result


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        result = f"<{self.tag}"
        if self.props is not None:
            for prop in self.props.keys():
                result += f' {prop}="{self.props[prop]}"'
        result += f">{self.value}</{self.tag}>"
        return result

    def __repr__(self):
        result = ""
        result += "LeafNode("
        result += f'"{self.tag if self.tag else ""}", '
        result += f'"{self.value if self.value else ""}", '
        result += f"{self.props})"
        return result


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required")
        if self.children is None:
            raise ValueError("Parent must have children")
        result = ""
        result += f"<{self.tag}"
        if self.props is not None:
            for prop in self.props.keys():
                result += f' {prop}="{self.props[prop]}"'
        result += ">"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result
