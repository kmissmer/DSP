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
                    file_counts[docket_id] = {"txt": 0, "htm": 0, "json": 0}
                if file.endswith(".txt"):
                    file_counts[docket_id]["txt"] += 1
                elif file.endswith(".htm") or file.endswith(".html"):
                    file_counts[docket_id]["htm"] += 1
                elif file.endswith(".json"):
                    file_counts[docket_id]["json"] += 1
    
    # Convert to the required output format
    output_list = []
    for docket_id, counts in file_counts.items():
        txt_count = counts.get("txt", 0)
        htm_count = counts.get("htm", 0)
        json_count = counts.get("json", 0)
        output_list.append(f"{docket_id} - {txt_count} txt, {htm_count} htm, {json_count} json")

    return output_list

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
