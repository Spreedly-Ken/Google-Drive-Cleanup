#!/usr/bin/env python3

import pandas as pd
import sys


def main():
    # The CSV file containing the inventory data
    csv_file = 'source_contracts_inventory.csv'
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
        sys.exit(1)
        
    # Ensure necessary columns exist
    required_cols = ['File Path', 'File Name', 'Extension', 'Size (bytes)', 'Creation Date', 'Modification Date']
    for col in required_cols:
        if col not in df.columns:
            print(f"Missing column in CSV: {col}")
            sys.exit(1)
            
    # Convert creation date to datetime and extract year; coerce errors in case of format issues
    df['Creation Date'] = pd.to_datetime(df['Creation Date'], errors='coerce')
    df['Year'] = df['Creation Date'].dt.year
    
    # Summary by extension
    summary_extension = df.groupby('Extension').agg(
        Count=('File Name', 'count'),
        Total_Size_bytes=('Size (bytes)', 'sum')
    ).reset_index()
    
    # Summary by creation year
    summary_year = df.groupby('Year').agg(
        Count=('File Name', 'count')
    ).reset_index()
    
    # Top 10 largest files
    # Ensure the Size (bytes) column is numeric
    df['Size (bytes)'] = pd.to_numeric(df['Size (bytes)'], errors='coerce')
    top_largest = df.sort_values(by='Size (bytes)', ascending=False).head(10)
    
    print("Summary by File Extension:")
    print(summary_extension.to_string(index=False))
    print("\nSummary by Creation Year:")
    print(summary_year.to_string(index=False))
    print("\nTop 10 Largest Files:")
    print(top_largest[['File Name', 'Size (bytes)', 'File Path']].to_string(index=False))


if __name__ == '__main__':
    main() 