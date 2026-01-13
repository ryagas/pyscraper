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
