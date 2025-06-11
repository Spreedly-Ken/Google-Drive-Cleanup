#!/usr/bin/env python3
"""
duplicate_scanner.py

Description:
    This script scans the 'Contracts_Copy' directory for duplicate files by normalizing filenames and comparing file contents using MD5 hashes. 
    It groups potential duplicates based on similar naming patterns and content similarity, displaying details such as file size and modification date.
    Additionally, the script provides a summary of Zendesk ticket files found in the "Data Files (json, md, yaml)" directory.

Usage:
    Simply run the script without arguments:
         $ ./duplicate_scanner.py

Dependencies:
    Python Standard Library: os, hashlib, re, pathlib, collections, datetime

Notes:
    Ensure that the 'Contracts_Copy' directory and 'Data Files (json, md, yaml)' directory are properly set up before running.
"""

import os
import hashlib
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def calculate_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (OSError, IOError) as e:
        print(f"⚠️  Error reading {filepath}: {e}")
        return None

def format_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def normalize_filename(filename):
    """Remove copy indicators to find base name"""
    base_name = Path(filename).stem
    
    # Remove common copy/version patterns
    patterns_to_remove = [
        r'\s+copy\s*\d*$',  # " copy", " copy 2", etc.
        r'\s+\(\d+\)$',     # " (1)", " (2)", etc.
    ]
    
    normalized = base_name
    for pattern in patterns_to_remove:
        normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
    
    return normalized.strip()

def scan_data_files_directory():
    """Scan the Data Files directory for duplicates"""
    directory = "Contracts_Copy"
    
    if not Path(directory).exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    print(f"🔍 Scanning: {Path(directory).absolute()}")
    print("=" * 60)
    
    # Get all files
    all_files = []
    for file_path in Path(directory).iterdir():
        if file_path.is_file() and not file_path.name.startswith('.'):
            try:
                stat = file_path.stat()
                all_files.append({
                    'path': file_path,
                    'name': file_path.name,
                    'size': stat.st_size,
                    'modified': stat.st_mtime,
                    'normalized_name': normalize_filename(file_path.name)
                })
            except OSError:
                continue
    
    print(f"📊 Found {len(all_files)} files")
    
    # Group by normalized name to find potential duplicates
    name_groups = defaultdict(list)
    for file_info in all_files:
        name_groups[file_info['normalized_name']].append(file_info)
    
    # Find groups with multiple files
    duplicate_groups = []
    for normalized_name, files in name_groups.items():
        if len(files) > 1:
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x['modified'], reverse=True)
            duplicate_groups.append((normalized_name, files))
    
    if not duplicate_groups:
        print("\n✅ No potential duplicates found based on naming patterns!")
        return
    
    print(f"\n🔄 Found {len(duplicate_groups)} groups of potential duplicates:")
    print("=" * 60)
    
    total_potential_savings = 0
    
    for i, (base_name, files) in enumerate(duplicate_groups, 1):
        print(f"\n📂 GROUP {i}: '{base_name}'")
        print(f"   {len(files)} files:")
        
        for j, file_info in enumerate(files):
            age_indicator = "🆕" if j == 0 else "🗓️ "
            modified_str = datetime.fromtimestamp(file_info['modified']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"     {age_indicator} {file_info['name']}")
            print(f"        Size: {format_size(file_info['size'])}")
            print(f"        Modified: {modified_str}")
            
            # Add to potential savings (all but newest)
            if j > 0:
                total_potential_savings += file_info['size']
        
        # Check if files have identical content
        if len(files) > 1:
            print(f"     🔍 Checking content similarity...")
            hashes = []
            for file_info in files:
                file_hash = calculate_file_hash(file_info['path'])
                hashes.append(file_hash)
            
            if len(set(hashes)) == 1:
                print(f"     ✅ All files have IDENTICAL content!")
            else:
                print(f"     📝 Files have DIFFERENT content (legitimate versions)")
    
    print(f"\n📈 SUMMARY:")
    print(f"   • Found {len(duplicate_groups)} groups of similar files")
    print(f"   • Potential space to review: {format_size(total_potential_savings)}")
    print(f"   • 🆕 = Newest file, 🗓️ = Older versions")
    
    # Show the biggest space wasters
    print(f"\n🎯 BIGGEST SPACE OPPORTUNITIES:")
    sorted_groups = sorted(duplicate_groups, key=lambda x: sum(f['size'] for f in x[1][1:]), reverse=True)
    
    for i, (base_name, files) in enumerate(sorted_groups[:3], 1):
        group_savings = sum(f['size'] for f in files[1:])
        print(f"   {i}. '{base_name}' - could save {format_size(group_savings)}")

def show_zendesk_files():
    """Show summary of zendesk ticket files"""
    data_dir = Path("Data Files (json, md, yaml)")
    zendesk_files = list(data_dir.glob("zendesk_ticket_*.json"))
    
    if zendesk_files:
        total_size = sum(f.stat().st_size for f in zendesk_files)
        print(f"\n📋 ZENDESK TICKETS:")
        print(f"   • {len(zendesk_files)} individual ticket files")
        print(f"   • Total size: {format_size(total_size)}")
        print(f"   • These appear to be individual tickets (not duplicates)")

if __name__ == "__main__":
    scan_data_files_directory()
    show_zendesk_files() 