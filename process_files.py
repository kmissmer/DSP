import json
import sys
from collections import OrderedDict, defaultdict

def process_file(input_file_path, output_file_path):
    try:
        # Load the input JSON file
        with open(input_file_path, 'r') as file:
            data = json.load(file)

        # Group data by DocketID and aggregate names
        dockets = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'organization': '', 'year': 0}))

        for item in data:
            # Check if the required fields exist, if not, skip this item
            if not all(key in item for key in ['Filename', 'Organization', 'DocketID', 'Filetype', 'Filesize', 'Year', 'Filepath']):
                continue

            docket_id = item['DocketID']
            name = item.get('Name', 'Null')
            dockets[docket_id][name]['count'] += 1
            dockets[docket_id][name]['organization'] = item['Organization']
            dockets[docket_id][name]['year'] = item['Year']

        processed_data = []

        for docket_id, names in dockets.items():
            for name, details in names.items():
                # Create a new item with aggregated count
                new_item = OrderedDict()
                new_item['Organization'] = details['organization']
                new_item['DocketID'] = docket_id
                new_item['Name'] = name
                new_item['Count'] = details['count']
                new_item['Year'] = details['year']
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
