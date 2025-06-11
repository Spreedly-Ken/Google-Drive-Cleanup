#!/usr/bin/env python3
"""
organize_by_year.py

Description:
    This script organizes files in a specified directory by moving them into subdirectories based on the year they were created.
    It inspects each file in the given directory, determines its creation year using st_birthtime (on macOS) or modification time as a fallback,
    and then moves the file into a folder named after that year. If a file with the same name already exists in the target directory,
    the script appends an incremental counter to the filename to prevent overwriting.

Usage:
    Run the script with an optional directory argument:
        $ ./organize_by_year.py <directory>
    If no argument is provided, it defaults to:
        /Users/ken/ai-projects/Google Drive Project/Finalized Contracts

Dependencies:
    Python Standard Library: os, shutil, sys, datetime

Notes:
    - This script is designed for use on macOS, though it will work on other systems with the modification time fallback.
    - Ensure you have proper permissions for moving files in the target directory.
"""
import os
import shutil
import sys
import datetime


def organize_files_by_year(directory):
    # Iterate over all entries in the provided directory
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        # Process only files (skip directories)
        if os.path.isfile(full_path):
            try:
                stat = os.stat(full_path)
                # Use st_birthtime if available (macOS), fallback to modification time
                creation_time = getattr(stat, 'st_birthtime', stat.st_mtime)
                year = datetime.datetime.fromtimestamp(creation_time).strftime('%Y')
            except Exception as e:
                print(f"Could not get time for {full_path}: {e}")
                continue
            
            target_dir = os.path.join(directory, year)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # Build target path; if file exists, rename to avoid overwrite
            target_path = os.path.join(target_dir, entry)
            base, ext = os.path.splitext(entry)
            counter = 1
            while os.path.exists(target_path):
                target_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
                counter += 1
            
            shutil.move(full_path, target_path)
            print(f"Moved {full_path} to {target_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "/Users/ken/ai-projects/Google Drive Project/Finalized Contracts"
        print(f"No arguments provided. Using default directory: {directory}")

    organize_files_by_year(directory) 