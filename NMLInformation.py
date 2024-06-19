import os
import json
from datetime import datetime
import sys

def process_files(directory):
    # Output file
    output_file = 'NMLoutput.txt'

    # List to store full names and additional information
    full_names_info = []

    # Check if directory is empty or doesn't exist
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return
    if not os.listdir(directory):
        print(f"Error: The directory '{directory}' is empty.")
        return

    # Loop through all files in the directory
    for root, dirs, files in os.walk(directory):

        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                
                # Get the file size
                file_size = os.path.getsize(file_path)
                
                # Print file being processed and its size
                print(f"Processing file: {filename}")
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
                        full_name = f"{first_name} {last_name}"
                        
                        docket_id = data['data']['attributes']['docketId']
                        docket_type = data['data']['type']
                        
                        info = f"Docket ID: {docket_id}, Docket Type: {docket_type}, File Size: {file_size} bytes, Name: {full_name}"
                        full_names_info.append(info)
                    except KeyError as e:
                        print(f"KeyError: {e} in file {filename}")
                
                # End timer and calculate elapsed time
                end_time = datetime.now()
                elapsed_time = end_time - start_time
                
                # Print time taken to process the file
                print(f"Time taken to process: {elapsed_time}")
                print("Done with file!")

        # Write the information to the output file
        with open(output_file, 'w') as output:
            for info in full_names_info:
                output.write(info + '\n')

        print(f"Information has been written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 <script_name.py> <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    process_files(directory_path)
