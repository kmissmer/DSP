import json
import sys
import os

def extract_organization_name(file_path):
    # Assuming organization name can be found in the file path
    parts = file_path.split('/')
    data_index = parts.index('data')
    organization_name = parts[data_index + 2]
    return organization_name

def combine_json_files(input_file1, input_file2):
    try:
        # Load data from the first input JSON file
        with open(input_file1, 'r') as file1:
            data1 = json.load(file1)

        # Load data from the second input JSON file
        with open(input_file2, 'r') as file2:
            data2 = json.load(file2)

        # Combine data from both files
        combined_data = data1 + data2

        # Extract organization name from the input files
        organization_name = extract_organization_name(input_file1)
        output_file = f"{organization_name}.json"

        # Write the combined data to the output JSON file
        with open(output_file, 'w') as outfile:
            json.dump(combined_data, outfile, indent=4)

        print(f"Combined data from '{input_file1}' and '{input_file2}' saved to '{output_file}'.")
    
    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file paths.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}. Please ensure the input files are valid JSON.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 combine_json.py InputFile1 InputFile2")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]

    combine_json_files(input_file1, input_file2)
