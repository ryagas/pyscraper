from utils import copy_directory_recursive, generate_page


def main():
    copy_directory_recursive("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()
