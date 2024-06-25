import os
import sys
from datetime import datetime

def extract_year_from_docket_id(docket_id):
    try:
        return int(docket_id.split('-')[1])  # Extract the year part from the docket_id
    except (IndexError, ValueError):
        return None

def count_files_per_docket(directory_path):
    file_counts = {}

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            docket_id = os.path.basename(root)
            year = extract_year_from_docket_id(docket_id)
            if year == 2024:
                if docket_id not in file_counts:
                    file_counts[docket_id] = 0
                file_counts[docket_id] += 1
    
    # Sort dockets by the number of files in descending order
    sorted_dockets = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_dockets[:50]

def write_to_file(top_50_dockets, output_file):
    with open(output_file, 'w') as f:
        for i, (docket_id, count) in enumerate(top_50_dockets, start=1):
            f.write(f"{docket_id} - {count} files\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 NumFilesPerDocket.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        print(f"Starting processing at {datetime.now()}...")

        top_50_dockets = count_files_per_docket(directory_path)

        # Write the top 50 dockets with their file counts to a file
        output_file = "dockets.txt"
        write_to_file(top_50_dockets, output_file)

        print(f"Results written to {output_file}")
