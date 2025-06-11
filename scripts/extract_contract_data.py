#!/usr/bin/env python3
"""
extract_contract_data.py

Description:
    This script processes contract files in PDF and DOCX formats from a source directory. It copies each file to a destination directory (avoiding name clashes by renaming if necessary), extracts text using PyPDF2 (for PDFs) or python-docx (for DOCX files), extracts key data points (such as Contract Date, Effective Date, Expiration Date, and involved parties) using regex patterns, and writes the extracted information to a CSV file.

Usage:
    Run the script with source and destination directory arguments:
        $ ./extract_contract_data.py <source_directory> <destination_directory>
    If no arguments are provided, default paths are used.

Dependencies:
    Python Standard Library: os, sys, re, csv, shutil
    External Libraries: PyPDF2, python-docx
"""

import os
import sys
import re
import csv
import shutil
from PyPDF2 import PdfReader
from docx import Document


def copy_file(src_path, dest_dir):
    '''Copies a file to the destination directory, avoiding overwrites by renaming if necessary.'''
    if not os.path.exists(src_path):
        print(f"File not found: {src_path}, skipping.")
        return None
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    base_name = os.path.basename(src_path)
    dest_path = os.path.join(dest_dir, base_name)
    counter = 1
    while os.path.exists(dest_path):
        name, ext = os.path.splitext(base_name)
        dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
        counter += 1
    try:
        shutil.copy2(src_path, dest_path)
        return dest_path
    except Exception as e:
        print(f"Error copying {src_path} to {dest_path}: {e}")
        return None


def extract_text_from_pdf(pdf_path):
    '''Extracts text from a PDF file using PyPDF2. Returns the extracted text as a string.'''
    text = ''
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text


def extract_text_from_docx(docx_path):
    '''Extracts text from a DOCX file using python-docx. Returns the extracted text as a string.'''
    text = ''
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + '\n'
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
    return text


def extract_key_data(text):
    '''Extracts key data points from the given text using regex patterns. Returns a dictionary of data points.'''
    data = {}
    # Example pattern for Contract Date
    m = re.search(r"Contract Date[:\s]*([\d/\.-]+)", text, re.IGNORECASE)
    data['Contract Date'] = m.group(1) if m else ""

    # Example pattern for Effective Date
    m = re.search(r"Effective Date[:\s]*([\d/\.-]+)", text, re.IGNORECASE)
    data['Effective Date'] = m.group(1) if m else ""

    # Example pattern for Expiration Date
    m = re.search(r"Expiration Date[:\s]*([\d/\.-]+)", text, re.IGNORECASE)
    data['Expiration Date'] = m.group(1) if m else ""

    # Example pattern for Parties: trying to find text like "between X and Y"
    m = re.search(r"between\s+(.*?)\s+and\s+(.*?)([\.,\n]|$)", text, re.IGNORECASE)
    if m:
        data['Party 1'] = m.group(1).strip()
        data['Party 2'] = m.group(2).strip()
    else:
        data['Party 1'] = ""
        data['Party 2'] = ""

    return data


def process_contracts(source_dir, dest_dir, output_csv):
    '''Processes all PDF and DOCX files from the read-only source directory, copies them to the destination folder, extracts text and key data, and writes results to output CSV.'''
    rows = []
    # Walk through the source directory recursively
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.pdf') or file.lower().endswith('.docx'):
                src_path = os.path.join(root, file)
                print(f"Processing: {src_path}")
                # Copy the file to the destination directory
                copied_path = copy_file(src_path, dest_dir)
                if not copied_path:
                    continue

                # Extract text based on file type
                if file.lower().endswith('.pdf'):
                    text = extract_text_from_pdf(copied_path)
                else:
                    text = extract_text_from_docx(copied_path)

                # Extract key data using regex
                key_data = extract_key_data(text)
                # Prepare the row for CSV
                row = {
                    'Original File Path': src_path,
                    'Copied File Path': copied_path,
                    'File Name': file,
                    'Contract Date': key_data.get('Contract Date', ''),
                    'Effective Date': key_data.get('Effective Date', ''),
                    'Expiration Date': key_data.get('Expiration Date', ''),
                    'Party 1': key_data.get('Party 1', ''),
                    'Party 2': key_data.get('Party 2', '')
                }
                rows.append(row)

    # Write the extracted data into a CSV file
    fieldnames = ['Original File Path', 'Copied File Path', 'File Name', 'Contract Date', 'Effective Date', 'Expiration Date', 'Party 1', 'Party 2']
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"Extraction complete. Data saved to {output_csv}")
    except Exception as e:
        print(f"Error writing CSV: {e}")


def main():
    # Default directories
    default_source = "/Users/ken/Library/CloudStorage/GoogleDrive-ken@spreedly.com/Shared drives/LEGAL/COMMERCIAL & BUSINESS SUPPORT/1. Customer Contracts"
    default_dest = "/Users/ken/ai-projects/Google Drive Project/Contracts_Copy"

    if len(sys.argv) >= 3:
        source_dir = sys.argv[1]
        dest_dir = sys.argv[2]
    else:
        source_dir = default_source
        dest_dir = default_dest
        print(f"No command line arguments provided. Using default source: {source_dir}\nDefault destination: {dest_dir}")

    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    output_csv = os.path.join(dest_dir, 'extracted_contract_data.csv')
    process_contracts(source_dir, dest_dir, output_csv)


if __name__ == '__main__':
    main() 