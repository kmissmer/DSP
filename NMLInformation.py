import os
import json
from datetime import datetime
import sys

def extract_organization_name(file_path):
    # Split the file_path by the directory separator '/'
    parts = file_path.split('/')
    
    # Find the index of the organization name
    data_index = parts.index('data')
    organization_name = parts[data_index + 2]  # Get the next component after 'data'
    
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
    # Check if docket_id is None or empty
    if not docket_id:
        return None
    
    # Extract the year from the docket_id, assuming the format is consistent
    try:
        return int(docket_id.split('-')[1])  # Extract the year part from the docket_id
    except (IndexError, ValueError):
        return None

def process_files(directory):
    # Output file
    output_file_name = 'NMLoutput.txt'

    # Check if directory is empty or doesn't exist
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    if not os.listdir(directory):
        print(f"Error: The directory '{directory}' is empty.")
        return

    # Set to keep track of processed file absolute paths
    processed_files = set()

    # Read existing entries from output_file (NMLoutput.txt)
    if os.path.exists(output_file_name):
        with open(output_file_name, "r") as f:
            try:
                for line in f:
                    entry = json.loads(line.strip())
                    filename = entry.get("file_path")  # Use 'file_path' instead of 'filepath'
                    if filename:
                        processed_files.add(filename.strip())  # Strip to remove any extra whitespace
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {output_file_name}")

    # Open output file in append mode
    with open(output_file_name, 'a') as output:
        # Walk through all files and subdirectories in the given directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                abs_file_path = os.path.abspath(file_path)
                
                # Skip processing if file_path is in processed_files (check absolute path)
                if abs_file_path in processed_files:
                    print(f"Skipping {file}. Already processed.")
                    continue
                
                if file.endswith('.json'):
                    # Extract the organization name from the file path
                    organization_name = extract_organization_name(file_path)
                    
                    # Get the base filename (without directories)
                    base_filename = os.path.basename(file_path)

                    # Extract docket_id from the file path
                    docket_id = extract_docket_name(file_path)

                    file_type = extract_file_type(file_path)

                    # Extract year from docket_id
                    year = extract_year_from_docket_id(docket_id)
                    
                    # Print file being processed and its size
                    file_size = os.path.getsize(file_path)
                    print(f"Processing file: {base_filename}")
                    print(f"File Size: {file_size} bytes")
                    
                    # Start timer
                    start_time = datetime.now()
                    
                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                        except json.JSONDecodeError as e:
                            print(f"Error decoding JSON in file {file}: {e}")
                            continue

                        # Extract first and last names, docket ID, and docket type
                        try:
                            first_name = data['data']['attributes'].get('firstName', None)
                            last_name = data['data']['attributes'].get('lastName', None)
                            full_name = f"{first_name} {last_name}" if (first_name and last_name) else "Null"
                                                        
                            
                            
                            info = {
                                "Organization": organization_name,
                                "FileName": base_filename,  # Use base filename here
                                "FileSize": file_size,
                                "DocketID": docket_id,
                                "FileType": file_type,
                                "Name": full_name,
                                "Year": year,  # Include extracted year
                                "FilePath": abs_file_path  # Add the full file path here
                            }
                            
                            # Write the information to the output file
                            output.write(json.dumps(info) + '\n')
                            
                        except KeyError as e:
                            print(f"KeyError: {e} in file {file}")
                    
                    # End timer and calculate elapsed time
                    end_time = datetime.now()
                    elapsed_time = end_time - start_time
                    
                    # Print time taken to process the file
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
