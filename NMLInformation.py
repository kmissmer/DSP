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
                    filename = entry.get("filename")
                    file_path = entry.get("file_path")  # Read stored file paths
                    if filename and file_path:
                        processed_files.add(file_path)  # Add stored file paths to processed_files
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
                                "Name": full_name,
                                "file_path": abs_file_path  # Add the full file path here
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
