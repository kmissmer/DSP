import json
import sys

def convert_output_to_json(input_file):
    # Determine the output file name based on input file name
    output_file = input_file.split('.')[0] + '.json'

    with open(input_file, 'r') as f:
        data = f.readlines()

    output_data = []
    for line in data:
        entry = eval(line.strip())  # Convert string to dictionary
        output_data.append(entry)

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)

    print(f"Conversion completed. Output saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 program.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_output_to_json(input_file)
