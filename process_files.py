import json
import sys
from collections import OrderedDict

def process_file(input_file_path, output_file_path):
    try:
        # Load the input JSON file
        with open(input_file_path, 'r') as file:
            data = json.load(file)

        # Process the data
        processed_data = []

        for item in data:
            # Check if the required fields exist, if not, skip this item
            if not all(key in item for key in ['filename', 'organization', 'docketID', 'filetype', 'filesize', 'year', 'filepath']):
                continue
            
            if 'names' in item and item['names'] is not None:
                for name in item['names']:
                    new_item = OrderedDict()
                    new_item['Organization'] = item['organization']
                    new_item['Filename'] = item['filename']
                    new_item['DocketID'] = item['docketID']
                    new_item['Filetype'] = item['filetype']
                    new_item['Filesize'] = item['filesize']
                    new_item['Name'] = name
                    new_item['Year'] = item['year']
                    new_item['Filepath'] = item['filepath']
                    processed_data.append(new_item)
            else:
                new_item = OrderedDict()
                new_item['filename'] = item['filename']
                new_item['organization'] = item['organization']
                new_item['docketID'] = item['docketID']
                new_item['filetype'] = item['filetype']
                new_item['filesize'] = item['filesize']
                new_item['name'] = None
                new_item['year'] = item['year']
                new_item['filepath'] = item['filepath']
                processed_data.append(new_item)

        # Output the processed data to a new JSON file
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
    if len(sys.argv) != 3:
        print("Usage: python3 process_files.py InputFile OutputFile")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_file(input_file_path, output_file_path)
