import os
import shutil


def copy_directory_recursive(source_dir, dest_dir):
    """
    Recursively copy contents from source directory to destination directory.
    The destination directory is emptied first, then all files are copied.

    Args:
        source_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    # Validate source directory exists
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

    # Empty destination directory if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # Create destination directory
    os.makedirs(dest_dir)

    # Recursively copy files
    for root, dirs, files in os.walk(source_dir):
        # Calculate relative path from source
        rel_path = os.path.relpath(root, source_dir)

        # Handle root directory case (when rel_path is ".")
        if rel_path == ".":
            dest_root = dest_dir
        else:
            dest_root = os.path.join(dest_dir, rel_path)

        # Create subdirectories in destination
        os.makedirs(dest_root, exist_ok=True)

        # Copy each file
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)

            shutil.copy2(src_file, dest_file)
            print(f"Copied: {dest_file}")


def main():
    copy_directory_recursive("static", "public")


main()
