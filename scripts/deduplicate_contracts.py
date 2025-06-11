#!/usr/bin/env python3
"""
deduplicate_contracts.py

Description:
    This script deduplicates files in a given folder by calculating the MD5 hash of each file. Files that share the same hash are considered duplicates. 
    Among duplicates, the most recently modified file is kept while older copies are deleted to free up disk space.

Usage:
    Run the script with a directory path as an argument:
        $ ./deduplicate_contracts.py <directory_path>
    If no argument is provided, the default directory 'Contracts_Copy' is used.

Dependencies:
    Python Standard Library: os, sys, hashlib, datetime, pathlib
"""
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime


def calculate_file_hash(filepath):
    """Calculate the MD5 hash of a file's content."""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def format_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"


def deduplicate_folder(folder):
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"Folder not found: {folder}")
        return

    print(f"Scanning {folder_path.absolute()} for duplicate files...")
    file_hashes = {}

    # List files in the folder (non recursive since files are expected to be flat)
    for file in folder_path.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            file_hash = calculate_file_hash(file)
            if file_hash is None:
                continue
            mod_time = file.stat().st_mtime
            # Store a tuple (file, mod_time) for each hash
            file_hashes.setdefault(file_hash, []).append((file, mod_time))

    total_removed = 0
    total_space = 0

    # For each group of files with the same hash
    for file_hash, files in file_hashes.items():
        if len(files) > 1:
            # Sort by modification time descending (newest first)
            files.sort(key=lambda x: x[1], reverse=True)
            keep_file = files[0][0]
            to_delete = [f[0] for f in files[1:]]
            print(f"\nDuplicate group for hash {file_hash} (keeping: {keep_file.name}):")
            for file in to_delete:
                try:
                    size = file.stat().st_size
                    os.remove(file)
                    print(f"  Deleted duplicate: {file.name}")
                    total_removed += 1
                    total_space += size
                except Exception as e:
                    print(f"  Error deleting {file.name}: {e}")

    print(f"\nDeduplication complete. Removed {total_removed} duplicate files, freeing up {format_size(total_space)}.")


if __name__ == '__main__':
    # Default directory is 'Contracts_Copy' in the current working directory
    target_dir = sys.argv[1] if len(sys.argv) > 1 else str(Path('Contracts_Copy'))
    deduplicate_folder(target_dir) 