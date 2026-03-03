import sys
from utils import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
