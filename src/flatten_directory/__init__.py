import os
import shutil
import argparse

def move_files_recursively(root_dir, dry_run=True):
    """
    Recursively move all files from subdirectories into the root directory.

    Args:
        root_dir: The directory to process (required)
        dry_run: If True, only print what would be moved (default: True)
    """
    if dry_run:
        print("DRY RUN MODE - No files will be moved\n")

    # Walk through all directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip the root directory itself
        if dirpath == root_dir:
            continue

        # Move each file to the root directory
        for filename in filenames:
            source_path = os.path.join(dirpath, filename)
            dest_path = os.path.join(root_dir, filename)

            try:
                if dry_run:
                    print(f"Would move: {source_path} -> {dest_path}")
                else:
                    shutil.move(source_path, dest_path)
                    print(f"Moved: {source_path} -> {dest_path}")
            except Exception as e:
                print(f"Error moving {source_path}: {e}")

    # Remove empty subdirectories
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if dirpath == root_dir:
            continue

        try:
            if not os.listdir(dirpath):  # Check if directory is empty
                if dry_run:
                    print(f"Would remove empty directory: {dirpath}")
                else:
                    os.rmdir(dirpath)
                    print(f"Removed empty directory: {dirpath}")
        except Exception as e:
            print(f"Error removing directory {dirpath}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recursively move all files from subdirectories into the target directory."
    )
    parser.add_argument(
        "target_dir",
        help="The target directory to traverse and flatten"
    )
    parser.add_argument(
        "--no-dry-run",
        action="store_true",
        help="Actually move files (default is dry-run mode)"
    )
    args = parser.parse_args()

    move_files_recursively(args.target_dir, dry_run=not args.no_dry_run)
    print("Done!")


if __name__ == "__main__":
    main()