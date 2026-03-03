import sys
from utils import copy_directory_recursive, generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_directory_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
