#!/usr/bin/env python3
"""
inventory_contracts.py

Description:
    This script inventories all files in a specified directory by collecting details such as full file path, file name,
    file extension, size in bytes, creation date, and modification date, then writes this data to a CSV file.

Usage:
    Run the script with a directory argument:
        $ ./inventory_contracts.py <directory>
    If no argument is provided, a default directory is used.

Dependencies:
    Python Standard Library: os, csv, sys, datetime
"""
import os
import csv
import sys
import datetime


def inventory_folder(dir_path, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Path', 'File Name', 'Extension', 'Size (bytes)', 'Creation Date', 'Modification Date'])
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    stat = os.stat(full_path)
                    # Use st_birthtime if available (macOS), otherwise fallback to st_mtime
                    created_ts = getattr(stat, 'st_birthtime', stat.st_mtime)
                    created = datetime.datetime.fromtimestamp(created_ts).isoformat()
                    modified = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                    size = stat.st_size
                except Exception as e:
                    created = modified = 'N/A'
                    size = 'N/A'
                
                writer.writerow([full_path, file, os.path.splitext(file)[1], size, created, modified])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        target_directory = '/Users/ken/ai-projects/Google Drive Project/Finalized Contracts'
        print(f"No directory provided. Using default: {target_directory}")
        
    output_csv = 'contracts_inventory.csv'
    inventory_folder(target_directory, output_csv)
    print(f"Inventory complete. CSV output saved to {output_csv}") 