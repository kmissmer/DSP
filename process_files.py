import json
import sys
from collections import OrderedDict

def process_file(input_file_path, output_file_path):
    # Load the input JSON file
    with open(input_file_path, 'r') as file:
        data = json.load(file)

    # Process the data
    processed_data = []

    for item in data:
        if 'names' in item and item['names'] is not None:
            for name in item['names']:
                new_item = OrderedDict()
                new_item['filename'] = item['filename']
                new_item['organization'] = item['organization']
                new_item['docketID'] = item['docketID']
                new_item['filetype'] = item['filetype']
                new_item['filesize'] = item['filesize']
                new_item['name'] = name
                new_item['filepath'] = item['filepath']
                processed_data.append(new_item)
        else:
            new_item = OrderedDict()
            new_item['filename'] = item['filename']
            new_item['organization'] = item['organization']
            new_item['docketID'] = item['docketID']
            new_item['filetype'] = item['filetype']
            new_item['filesize'] = item['filesize']
            new_item['name'] = None
            new_item['filepath'] = item['filepath']
            processed_data.append(new_item)

    # Output the processed data to a new JSON file
    with open(output_file_path, 'w') as file:
        json.dump(processed_data, file, indent=4)

    print(f'Processed data and saved it in "{output_file_path}".')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 process_files.py InputFile OutputFile")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    process_file(input_file_path, output_file_path)
