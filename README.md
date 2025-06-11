# Google Drive Cleanup

## Overview

This repository contains a suite of Python scripts designed to automate the management and processing of contract files from Google Drive. The tools handle tasks such as organizing files by year, copying final PDFs, deduplicating files, deleting files matching specified keywords, inventory management, merging customer folders, and cleaning up unwanted subfolders.

## Project Structure

- **Contracts_Copy/** - Contains customer contract folders.
- **data/** - Contains input CSV files (e.g., keywords) used by some scripts. *(Ignored - not shared)*
- **docs/** - Documentation related to the project.
- **scripts/** - Python scripts for various tasks:
  - `organize_by_year.py`: Organize files by creation year.
  - `copy_final_pdfs.py`: Copy PDF files from final(s) folders.
  - `deduplicate_contracts.py`: Deduplicate files based on file hash.
  - `delete_files_with_keywords.py`: Delete files whose names contain specified keywords.
  - `duplicate_scanner.py`: Scan for duplicate files and summarize potential savings.
  - `extract_contract_data.py`: Extract key contract data from PDF/DOCX files.
  - `inventory_contracts.py`: Inventory files by collecting metadata (file path, size, dates, etc.).
  - `inventory_customer_contracts.py`: Inventory customer contract subdirectories.
  - `inventory_source_contracts.py`: Inventory source contract files.
  - `inventory_summary.py`: Generate a summary report of the inventory.
  - `merge_customer_folders.py`: Merge customer folders using fuzzy matching.
  - `delete_draft_working_subfolders.py`: Delete all subfolders with names containing "draft" or "working".
- **deletion_summary.md** - Output file summarizing deletion operations. *(Ignored)*

## Dependencies

The scripts rely on Python 3 and primarily use standard libraries. Additional libraries for specific functionality include:

- PyPDF2
- python-docx
- rapidfuzz
- pandas (for inventory summary)

Install dependencies using:

```
pip install -r requirements.txt
```

## Git Ignore

Sensitive data, CSV files, outputs, and input files (e.g., in the data directory) are intentionally not shared. See the `.gitignore` file for details.

## How to Use

Run individual scripts with their respective arguments. For example:

```
./organize_by_year.py /path/to/target/directory
```

If no arguments are provided, the scripts often use default directories configured within the code.

## License

[Specify your license here] 