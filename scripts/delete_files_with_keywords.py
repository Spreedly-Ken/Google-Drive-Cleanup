#!/usr/bin/env python3
"""
delete_files_with_keywords.py

Description:
    This script deletes files whose names contain any of the specified keywords. 
    It reads keywords from a CSV file (default: keywords.csv) and scans a target directory recursively for files matching any keyword.
    The script supports a dry-run mode to simulate deletions and an option to auto-confirm deletions.

Usage:
    Run the script with a directory as an argument (or input it when prompted):
        $ ./delete_files_with_keywords.py <directory>
    Optional flags:
        --dry-run    Perform a dry run without deleting files.
        --yes        Automatically confirm deletion without prompt.

Dependencies:
    Python Standard Library: os, sys, argparse, csv, pathlib, time
"""

import os
import sys
import argparse
import csv
from pathlib import Path
import time

# Update the KEYWORDS_CSV constant to use the CSV file from the data directory
KEYWORDS_CSV = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data', 'keywords.csv')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Delete files whose names contain any of the specified keywords.')
    parser.add_argument('directory', type=str, nargs='?', help='Directory to search for files. If not provided, you will be prompted to enter one.')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run; list files that would be deleted.')
    parser.add_argument('--yes', action='store_true', help='Automatically confirm deletion without prompt.')
    return parser.parse_args()


def find_files(directory, keywords):
    found_files = []
    directory = Path(directory)
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if any(keyword.lower() in file_name.lower() for keyword in keywords):
                found_files.append(Path(root) / file_name)
    return found_files


def load_keywords_from_csv(filepath):
    keywords = []
    try:
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip header row
            for row in reader:
                if row and row[0]:
                    keywords.append(row[0].strip())
    except Exception as e:
        print(f"Error reading CSV file {filepath}: {e}")
    return keywords


def main():
    args = parse_arguments()
    if not args.directory:
        args.directory = input("Please enter the target directory: ")

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory.")
        sys.exit(1)

    keywords = load_keywords_from_csv(KEYWORDS_CSV)
    if not keywords:
        print(f"No keywords provided in CSV file '{KEYWORDS_CSV}'.")
        sys.exit(1)

    files_to_delete = find_files(args.directory, keywords)
    if not files_to_delete:
        print("No matching files found to delete.")
        sys.exit(0)

    print("The following files will be deleted:")
    for file in files_to_delete:
        print(file)

    if args.dry_run:
        print("Dry run enabled: no files have been deleted.")
        sys.exit(0)

    if not args.yes:
        confirm = input("Are you sure you want to delete these files? (y/N): ")
        if confirm.lower() not in ['y', 'yes']:
            print("Operation canceled.")
            sys.exit(0)

    print("Starting deletion...")
    start_time = time.time()
    success_count = 0
    fail_count = 0
    failed_files = []
    total_files = len(files_to_delete)

    for idx, file in enumerate(files_to_delete, start=1):
        print(f"Processing file {idx} of {total_files}: {file}")
        try:
            file.unlink()
            print(f"Deleted: {file}\n")
            success_count += 1
        except Exception as e:
            print(f"Failed to delete {file}: {e}\n")
            fail_count += 1
            failed_files.append((str(file), str(e)))

    end_time = time.time()
    elapsed_time = end_time - start_time

    summary = (f"# Deletion Summary\n\n"
               f"**Total files matched:** {total_files}\n\n"
               f"**Files successfully deleted:** {success_count}\n\n"
               f"**Files failed to delete:** {fail_count}\n\n"
               f"**Elapsed time:** {elapsed_time:.2f} seconds\n\n")

    if failed_files:
        summary += "## Failed Files Details\n\n"
        for file, error in failed_files:
            summary += f"- **File:** {file} - **Error:** {error}\n"

    print(summary)
    with open("deletion_summary.md", "w") as summary_file:
        summary_file.write(summary)
    print("Summary saved to deletion_summary.md")


if __name__ == '__main__':
    main() 