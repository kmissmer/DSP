import json
import sys

def combine_json_files(input_file1, input_file2, output_file):
    try:
        # Load data from the first input JSON file
        with open(input_file1, 'r') as file1:
            data1 = json.load(file1)

        # Load data from the second input JSON file
        with open(input_file2, 'r') as file2:
            data2 = json.load(file2)

        # Combine data from both files
        combined_data = data1 + data2

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
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python3 combine_json.py InputFile1 InputFile2 OutputFile [OutputFileName]")
        sys.exit(1)

    input_file1 = sys.argv[1]
    input_file2 = sys.argv[2]
    output_file = sys.argv[3]

    if len(sys.argv) == 5:
        output_file = sys.argv[4]

    combine_json_files(input_file1, input_file2, output_file)