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
            # Get the docket name from the path relative to directory_path
            rel_path = os.path.relpath(file_path, directory_path)
            path_components = rel_path.split(os.sep)
            if len(path_components) > 1:
                docket_name = path_components[0]
                year = extract_year_from_docket_id(docket_name)
                if year == 2024:
                    if docket_name not in file_counts:
                        file_counts[docket_name] = 0
                    if file.endswith(".txt") or file.endswith(".htm") or file.endswith(".html") or file.endswith(".json"):
                        file_counts[docket_name] += 1
    
    # Convert to the required output format
    output_list = []
    for docket_name, count in file_counts.items():
        output_list.append(f"{docket_name} - {count} files")

    # Sort by file count in descending order
    output_list.sort(key=lambda x: int(x.split(" - ")[1].split()[0]), reverse=True)  # Adjusted key function here

    return output_list[:50]


def write_to_file(output_list, output_file):
    with open(output_file, 'w') as f:
        for line in output_list:
            f.write(f"{line}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 NumFilesPerDocket.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        print(f"Starting processing at {datetime.now()}...")

        output_list = count_files_per_docket(directory_path)

        # Write the dockets with their file counts to a file
        output_file = "dockets.txt"
        write_to_file(output_list, output_file)

        print(f"Results written to {output_file}")
