#!/usr/bin/env python3
"""
delete_draft_working_subfolders.py

Description:
    This script recursively searches a specified base directory for subfolders whose names are "Draft", "Drafts", or "Working" (case-insensitive) 
    and deletes them along with all of their contents.

Usage:
    Run the script with an optional base directory argument:
        $ ./delete_draft_working_subfolders.py <base_directory>
    If no argument is provided, the default base directory is:
        /Users/ken/ai-projects/Google Drive Cleanup/Contracts_Copy/1. Customer Contracts

Dependencies:
    Python Standard Library: os, shutil, sys
"""

import os
import shutil
import sys


def delete_target_subfolders(base_dir):
    # Define substrings (lowercase) to search for in folder names
    substrings = ["draft", "working"]
    count = 0

    # Walk the directory tree from the bottom up to safely remove directories
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for d in dirs:
            lower_d = d.lower()
            # Check if any substring is present in the folder name
            if any(sub in lower_d for sub in substrings):
                dir_path = os.path.join(root, d)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted folder: {dir_path}")
                    count += 1
                except Exception as e:
                    print(f"Error deleting folder {dir_path}: {e}")
    print(f"Deleted {count} folder(s) matching target substrings.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_directory = sys.argv[1]
    else:
        base_directory = "/Users/ken/ai-projects/Google Drive Cleanup/Contracts_Copy/1. Customer Contracts"
        print(f"No directory argument provided. Using default base directory: {base_directory}")

    if not os.path.isdir(base_directory):
        print(f"Error: Base directory {base_directory} does not exist.")
        sys.exit(1)

    delete_target_subfolders(base_directory) 