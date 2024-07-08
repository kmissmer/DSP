import json
import csv
import sys

def json_to_csv(input_file):
    try:
        # Load JSON data
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Extract headers from the keys of the first item
        headers = list(data[0].keys())

        # Prepare CSV output file
        output_file = input_file.replace('.json', '.csv')

        # Write to CSV file with escapechar set to handle special characters
        with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers, escapechar='\\')
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        print(f"CSV file '{output_file}' successfully created.")

    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the file path.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}. Please ensure the input file is valid JSON.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 json_to_csv.py InputFile.json")
        sys.exit(1)

    input_file = sys.argv[1]
    json_to_csv(input_file)
