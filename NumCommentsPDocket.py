import os
import sys
from datetime import datetime

def extract_year_from_docket_id(docket_id):
    try:
        return int(docket_id.split('-')[1])  # Extract the year part from the docket_id
    except (IndexError, ValueError):
        return None

def count_files_per_docket(directory_path, output_file):
    file_counts = {}

    # Open the output file for appending
    with open(output_file, 'a') as f:
        # Walk through the directory and subdirectories
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Get the relative path from directory_path
                rel_path = os.path.relpath(file_path, directory_path)
                path_components = rel_path.split(os.sep)
                if len(path_components) > 1:
                    # Adjust index to get the correct docket name
                    docket_name = path_components[1]  # This assumes the docket name is the second directory after /data/data
                    year = extract_year_from_docket_id(docket_name)
                    if year == 2024:
                        if docket_name not in file_counts:
                            file_counts[docket_name] = 0
                        if file.endswith(".json"):
                            file_counts[docket_name] += 1
                            # Write the current total count to the output file
                            f.write(f"{docket_name} - {file_counts[docket_name]} files\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 NumFilesPerDocket.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        print(f"Starting processing at {datetime.now()}...")

        # Output file
        output_file = "dockets.txt"

        # Ensure the output file is empty before starting
        open(output_file, 'w').close()

        # Process the files and write counts as they are processed
        count_files_per_docket(directory_path, output_file)

        print(f"Results written to {output_file}")
