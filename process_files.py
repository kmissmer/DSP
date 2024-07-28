import json
import sys
import os
from collections import OrderedDict, defaultdict

def process_file(input_file_path):
    try:
        # Load the input JSON file
        with open(input_file_path, 'r') as file:
            data = json.load(file)

        # Group data by DocketID
        dockets = defaultdict(list)
        for item in data:
            docket_id = item['DocketID']
            dockets[docket_id].append(item)

        processed_data = []

        for docket_id, items in dockets.items():
            name_counts = defaultdict(int)

            for item in items:
                # Check if the required fields exist, if not, skip this item
                if not all(key in item for key in ['Organization', 'FileName', 'DocketID', 'FileType', 'Year', 'FilePath']):
                    continue

                # Handle both Filesize and FileSize keys
                filesize = item.get('Filesize') or item.get('FileSize')

                names = item.get('Name', 'Null')
                if isinstance(names, list):
                    for name in names:
                        name_counts[name] += 1
                else:
                    name_counts[names] += 1

            # To ensure each name within the same docket is output only once
            seen_names = set()

            for item in items:
                names = item.get('Name', 'Null')
                if isinstance(names, list):
                    for name in names:
                        count = name_counts[name]

                        if name not in seen_names:
                            seen_names.add(name)

                            new_item = OrderedDict()
                            new_item['Organization'] = item['Organization']
                            new_item['Filename'] = item['FileName']
                            new_item['Filesize'] = filesize
                            new_item['DocketID'] = item['DocketID']
                            new_item['Filetype'] = item['FileType']
                            new_item['Name'] = name
                            new_item['Count'] = count
                            new_item['Year'] = item['Year']
                            new_item['Filepath'] = item['FilePath']
                            processed_data.append(new_item)
                else:
                    count = name_counts[names]

                    if names not in seen_names:
                        seen_names.add(names)

                        new_item = OrderedDict()
                        new_item['Organization'] = item['Organization']
                        new_item['Filename'] = item['FileName']
                        new_item['Filesize'] = filesize
                        new_item['DocketID'] = item['DocketID']
                        new_item['Filetype'] = item['FileType']
                        new_item['Name'] = names
                        new_item['Count'] = count
                        new_item['Year'] = item['Year']
                        new_item['Filepath'] = item['FilePath']
                        processed_data.append(new_item)

        # Define the output file path by changing the extension to .processed.json
        base_name = os.path.splitext(input_file_path)[0]
        output_file_path = f"{base_name}_processed.json"

        # Output the processed data to the new JSON file
        with open(output_file_path, 'w') as file:
            json.dump(processed_data, file, indent=4)

        print(f'Processed data and saved it in "{output_file_path}".')
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{input_file_path}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 process_files.py InputFile")
        sys.exit(1)

    input_file_path = sys.argv[1]

    process_file(input_file_path)
