#!/usr/bin/env python3
"""
merge_customer_folders.py

This script applies fuzzy merge suggestions to actual customer directories.
It scans a given root directory for customer folders, uses fuzzy matching (via rapidfuzz)
to group similar folder names, and then, after prompting for confirmation, merges the folders.
Merging involves moving all contents from duplicate folders into a representative folder,
then removing the now-empty duplicate folders.

Usage:
    python merge_customer_folders.py --root <path_to_customer_folders>
"""

import os
import shutil
import argparse

try:
    from rapidfuzz import fuzz
except ImportError:
    print("[ERROR] The module 'rapidfuzz' is required for fuzzy merging. Install it via: pip install rapidfuzz")
    exit(1)


def fuzzy_group(names, threshold=80):
    """
    Group similar names using fuzzy matching.
    Returns a list of groups, where each group is a list of similar names.
    """
    groups = []
    for name in names:
        added = False
        for group in groups:
            if fuzz.ratio(name, group[0]) >= threshold:
                group.append(name)
                added = True
                break
        if not added:
            groups.append([name])
    return groups


def merge_directories(root_directory, groups):
    """
    For each group with multiple similar folder names, use the first (alphabetically) as the representative.
    Move all contents from the other folders into the representative folder and remove the empty folder.
    """
    for group in groups:
        if len(group) > 1:
            group_sorted = sorted(group)
            rep = group_sorted[0]
            rep_path = os.path.join(root_directory, rep)
            if not os.path.exists(rep_path):
                print(f"Representative folder '{rep}' does not exist, skipping group {group}")
                continue
            print(f"Merging group: {group_sorted} into '{rep}'")
            for folder in group_sorted:
                if folder == rep:
                    continue
                folder_path = os.path.join(root_directory, folder)
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    for item in os.listdir(folder_path):
                        src = os.path.join(folder_path, item)
                        dst = os.path.join(rep_path, item)
                        if os.path.exists(dst):
                            print(f"  Warning: {dst} already exists. Skipping {src}.")
                        else:
                            shutil.move(src, dst)
                    try:
                        os.rmdir(folder_path)
                        print(f"  Merged and removed folder '{folder}'.")
                    except OSError as e:
                        print(f"  Could not remove folder '{folder}': {e}")
                else:
                    print(f"Folder '{folder}' does not exist, skipping.")


def main():
    parser = argparse.ArgumentParser(description="Merge similar customer folders based on fuzzy merge suggestions")
    parser.add_argument("--root", default=None, help="Path to the folder containing customer directories")
    args = parser.parse_args()
    if not args.root:
        args.root = input("Enter the path to the folder containing customer directories: ").strip()
    root = args.root

    # List all directories in the root directory
    customers = [name for name in os.listdir(root) if os.path.isdir(os.path.join(root, name))]
    print(f"Found {len(customers)} customer directories.")

    groups = fuzzy_group(customers)

    # Print merge suggestions
    print("Merge Suggestions:")
    for group in groups:
        if len(group) > 1:
            group_sorted = sorted(group)
            print(f"  {group_sorted[0]}: {', '.join(group_sorted)}")

    confirm = input("Proceed with merging? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Merge cancelled.")
        return

    merge_directories(root, groups)
    print("Merge process completed.")


if __name__ == "__main__":
    main() 