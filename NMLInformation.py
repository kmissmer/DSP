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


def process_files(directory):
    # Output file
    output_file = 'NMLoutput.txt'

    # Check if directory is empty or doesn't exist
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    if not os.listdir(directory):
        print(f"Error: The directory '{directory}' is empty.")
        return

    # Set to keep track of processed filenames
    processed_files = set()

    # Read existing entries from output_file (NMLoutput.txt)
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    filename = entry.get("filename")
                    if filename:
                        processed_files.add(filename)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in {output_file}")

    # Walk through all files and subdirectories in the given directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                
                # Skip processing if file_path is in processed_files
                if file_path in processed_files:
                    print(f"Skipping {filename}. Already processed.")
                    continue
                
                # Get the file size
                file_size = os.path.getsize(file_path)
                
                # Extract the organization name from the file path
                organization_name = extract_organization_name(file_path)
                
                # Get the base filename (without directories)
                base_filename = os.path.basename(file_path)
                
                # Print file being processed and its size
                print(f"Processing file: {base_filename}")
                print(f"File Size: {file_size} bytes")
                
                # Start timer
                start_time = datetime.now()
                
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {filename}: {e}")
                        continue

                    # Extract first and last names, docket ID, and docket type
                    try:
                        first_name = data['data']['attributes']['firstName']
                        last_name = data['data']['attributes']['lastName']
                        full_name = f"{first_name} {last_name}" if (first_name and last_name) else "null"
                        
                        docket_id = data['data']['attributes']['docketId']
                        docket_type = data['data']['type']
                        
                        info = {
                            "organization": organization_name,
                            "filename": base_filename,  # Use base filename here
                            "filesize": file_size,
                            "Docket ID": docket_id,
                            "Docket Type": docket_type,
                            "Name": full_name
                        }
                        
                        # Write the information to the output file immediately
                        with open(output_file, 'a') as output:
                            output.write(json.dumps(info) + '\n')
                        
                    except KeyError as e:
                        print(f"KeyError: {e} in file {filename}")
                
                # End timer and calculate elapsed time
                end_time = datetime.now()
                elapsed_time = end_time - start_time
                
                # Print time taken to process the file
                print(f"Time taken to process: {elapsed_time}")
                print("Done with file!")

    print(f"Information has been added to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 <script_name.py> <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    process_files(directory_path)
