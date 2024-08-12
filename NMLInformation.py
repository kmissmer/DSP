import os
import json
from datetime import datetime
import sys
import re

def extract_organization_name(file_path):
    parts = file_path.split('/')
    data_index = parts.index('data')
    organization_name = parts[data_index + 2]
    return organization_name

def extract_docket_name(file_path):
    parts = file_path.split('/')
    data_index = parts.index('data')
    docket_name = parts[data_index + 3]
    return docket_name

def extract_file_type(file_path):
    parts = file_path.split('/')
    file_type = parts.index('data')
    file_type = parts[file_type + 5]
    return file_type


def extract_year_from_docket_id(docket_id):
    if not docket_id:
        return None
    try:
        # Search for the first occurrence of a 4-digit number in the docket ID
        match = re.search(r'\b\d{4}\b', docket_id)
        if match:
            return int(match.group(0))
        else:
            return None
    except (IndexError, ValueError):
        return None
    
def process_files(directory):
    processed_files = set()

    # Determine output file name based on organization name
    output_file_name = None
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                organization_name = extract_organization_name(file_path)
                output_file_name = f'NMLoutput{organization_name}.txt'
                break
        if output_file_name:
            break

    if not output_file_name:
        print(f"Error: No JSON files found in '{directory}' to determine organization name.")
        return

    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    if not os.listdir(directory):
        print(f"Error: The directory '{directory}' is empty.")
        return

    if os.path.exists(output_file_name):
        with open(output_file_name, "r") as f:
            try:
                for line in f:
                    entry = json.loads(line.strip())
                    filename = entry.get("FileName")
                    if filename:
                        processed_files.add(filename.strip())
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {output_file_name}")

    with open(output_file_name, 'a') as output:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                base_filename = os.path.basename(file_path)

                if base_filename in processed_files:
                    print(f"Skipping {file}. Already processed.")
                    continue

                if file.endswith('.json'):
                    organization_name = extract_organization_name(file_path)
                    docket_id = extract_docket_name(file_path)
                    file_type = extract_file_type(file_path)
                    year = extract_year_from_docket_id(docket_id)
                    file_size = os.path.getsize(file_path)

                    print(f"Processing file: {base_filename}")
                    print(f"File Size: {file_size} bytes")

                    start_time = datetime.now()

                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON in file {file}: {e}")
                            continue

                        try:
                            first_name = data['data']['attributes'].get('firstName', None)
                            last_name = data['data']['attributes'].get('lastName', None)
                            full_name = f"{first_name} {last_name}" if (first_name and last_name) else "Null"

                            info = {
                                "Organization": organization_name,
                                "FileName": base_filename,
                                "FileSize": file_size,
                                "DocketID": docket_id,
                                "FileType": file_type,
                                "Name": full_name,
                                "Count": 1,
                                "Year": year,
                                "FilePath": os.path.abspath(file_path)
                            }

                            output.write(json.dumps(info) + '\n')
                        except KeyError as e:
                            print(f"KeyError: {e} in file {file}")

                    end_time = datetime.now()
                    elapsed_time = end_time - start_time

                    print(f"Time taken to process: {elapsed_time}")
                    print("Done with file!")

    print(f"Information has been written to {output_file_name}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 <script_name.py> <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    process_files(directory_path)
