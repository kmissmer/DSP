import json
import sys
from collections import OrderedDict, defaultdict

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
            
            name_counts = defaultdict(int)
            if 'names' in item and item['names'] is not None:
                for name in item['names']:
                    name_counts[name] += 1

                for name, count in name_counts.items():
                    new_item = OrderedDict()
                    new_item['Organization'] = item['organization']
                    new_item['Filename'] = item['filename']
                    new_item['Filesize'] = item['filesize']
                    new_item['DocketID'] = item['docketID']
                    new_item['Filetype'] = item['filetype']
                    new_item['Name'] = name
                    new_item['Count'] = count
                    new_item['Year'] = item['year']
                    new_item['Filepath'] = item['filepath']
                    processed_data.append(new_item)
            else:
                new_item = OrderedDict()
                new_item['Organization'] = item['organization']
                new_item['Filename'] = item['filename']
                new_item['Filesize'] = item['filesize']
                new_item['DocketID'] = item['docketID']
                new_item['Filetype'] = item['filetype']
                new_item['Name'] = None
                new_item['Count'] = 0
                new_item['Year'] = item['year']
                new_item['Filepath'] = item['filepath']
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
