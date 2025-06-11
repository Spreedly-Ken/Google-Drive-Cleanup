#!/usr/bin/env python3
"""
copy_final_pdfs.py

Description:
    This script scans the provided source directory recursively for subdirectories named "final" or "finals" (case-insensitive) 
    and copies any PDF files found into a designated destination directory. It avoids overwriting files at the destination by renaming files with an incremental counter if needed.

Usage:
    Run the script with source and destination directories as command line arguments:
        $ ./copy_final_pdfs.py <source_directory> <destination_directory>
    If no arguments are provided, default paths are used.

Dependencies:
    Python Standard Library: os, shutil, sys
"""
import os
import shutil
import sys


def copy_pdfs_from_finals(source_dir, dest_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(source_dir):
        # Check if the current directory's name is 'final' or 'finals' (case-insensitive)
        if os.path.basename(root).lower() in ["final", "finals"]:
            for file in files:
                if file.lower().endswith(".pdf"):
                    source_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_dir, file)
                    
                    # If destination file exists, modify the filename to avoid overwriting
                    base, ext = os.path.splitext(file)
                    counter = 1
                    while os.path.exists(dest_file):
                        dest_file = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                        counter += 1
                    
                    shutil.copy2(source_file, dest_file)
                    print(f"Copied {source_file} to {dest_file}")


if __name__ == "__main__":
    # Accept command line arguments for source and destination directories
    if len(sys.argv) == 3:
        src = sys.argv[1]
        dst = sys.argv[2]
    else:
        src = "/Users/ken/Library/CloudStorage/GoogleDrive-ken@spreedly.com/Shared drives/LEGAL/COMMERCIAL & BUSINESS SUPPORT/1. Customer Contracts"
        dst = "/Users/ken/ai-projects/Google Drive Project/Finalized Contracts"
        print(f"No arguments provided. Using default source: {src}\nDestination: {dst}")
    
    copy_pdfs_from_finals(src, dst) 