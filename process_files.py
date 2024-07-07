import json
import os
import sys

def process_file(input_file_path, output_dir):
    # Load the input JSON file
    with open(input_file_path, 'r') as file:
        data = json.load(file)

    # Process the data
    processed_data = []

    for item in data:
        if item['names'] is not None and len(item['names']) > 1:
            for name in item['names']:
                new_item = item.copy()
                new_item['name'] = name
                del new_item['names']
                processed_data.append(new_item)
        else:
            if item['names']:
                item['name'] = item['names'][0]
            del item['names']
            processed_data.append(item)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Output each processed item to a new JSON file
    for i, item in enumerate(processed_data):
        output_file_path = os.path.join(output_dir, f'output_{i+1}.json')
        with open(output_file_path, 'w') as file:
            json.dump(item, file, indent=4)

    print(f'Processed {len(processed_data)} items and saved them in the "{output_dir}" directory.')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 process_files.py InputFile OutputDir")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_dir = sys.argv[2]

    process_file(input_file_path, output_dir)
