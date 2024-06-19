import json
import sys

def convert_output_to_json(input_file):
    # Determine the output file name based on input file name
    output_file = input_file.split('.')[0] + '.json'

    with open(input_file, 'r') as f:
        data = f.readlines()

    output_data = []
    for line in data:
        try:
            entry = json.loads(line.strip())  # Convert JSON string to dictionary
            output_data.append(entry)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in line: {line.strip()}\nError message: {e}")

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)

    print(f"Conversion completed. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 program.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_output_to_json(input_file)
