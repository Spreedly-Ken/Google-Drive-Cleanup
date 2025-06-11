# inventory_customer_contracts.py
#
# This script inventories customer contract directories.
# It scans a given root directory for immediate subdirectories (each representing a customer) and their subfolders.
# The inventory is written to a CSV file with columns 'Customer' and 'Subfolder'.
# When run with the --merge flag, the script performs fuzzy merging of similar customer names using the rapidfuzz library,
# grouping variations together and outputting the merged results to a separate CSV file.

import os
import csv
import argparse


def inventory_customer_contracts(root_directory):
    """Inventory immediate subfolders (customers) and their subfolders from the given root directory."""
    customers = {}
    # List immediate subfolders as customer names
    for customer in os.listdir(root_directory):
        customer_path = os.path.join(root_directory, customer)
        if os.path.isdir(customer_path):
            # List subfolders within each customer folder
            sub_folders = [name for name in os.listdir(customer_path) if os.path.isdir(os.path.join(customer_path, name))]
            customers[customer] = sub_folders
    return customers


def write_inventory_csv(data, output_path):
    """Write the inventory dictionary to a CSV file with columns 'Customer' and 'Subfolder'."""
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Customer", "Subfolder"])
        for customer, subfolders in sorted(data.items()):
            if subfolders:
                for sub in sorted(subfolders):
                    writer.writerow([customer, sub])
            else:
                writer.writerow([customer, ""])
    print("Inventory CSV saved to:", output_path)


def merge_similar_names(names, threshold=80):
    """Merge similar names based on fuzzy matching with a given threshold.
       Returns groups where each group is a list of similar names.
    """
    try:
        from rapidfuzz import fuzz
    except ImportError:
        print("[ERROR] The module 'rapidfuzz' is required for fuzzy merging. Install it via: pip install rapidfuzz")
        exit(1)

    groups = []
    for name in names:
        added = False
        for group in groups:
            # Compare with the first name in each group
            if fuzz.ratio(name, group[0]) >= threshold:
                group.append(name)
                added = True
                break
        if not added:
            groups.append([name])
    return groups


def write_merge_csv(groups, output_path):
    """Write the merged groups to a CSV file with columns 'Group Representative' and 'Customer Variations'."""
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Group Representative", "Customer Variations"])
        for group in sorted(groups, key=lambda g: g[0]):
            writer.writerow([group[0], ", ".join(sorted(group))])
    print("Merged inventory CSV saved to:", output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inventory and optionally merge customer contracts folder names")
    parser.add_argument("--root", default=None, help="Path to the '1. Customer Contracts' folder")
    parser.add_argument("--output", default="data/customer_inventory.csv", help="CSV output file for inventory")
    parser.add_argument("--merge", action="store_true", help="Also perform fuzzy merging of similar customer names")
    parser.add_argument("--merge_output", default="data/customer_merged_inventory.csv", help="CSV output file for merged groups")
    args = parser.parse_args()

    if not args.root:
        mode = input("Do you want to run the base or merge version? (Enter 'base' or 'merge'): ").strip().lower()
        if mode == 'merge':
            args.merge = True
        args.root = input("Enter the path to the folder to analyze: ").strip()

    # Generate inventory
    inventory = inventory_customer_contracts(args.root)
    write_inventory_csv(inventory, args.output)

    # If requested, perform fuzzy merging on the customer names (top-level folders)
    if args.merge:
        customer_names = list(inventory.keys())
        groups = merge_similar_names(customer_names)
        write_merge_csv(groups, args.merge_output) 