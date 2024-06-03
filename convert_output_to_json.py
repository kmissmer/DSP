import json

def convert_output_to_json(input_file, output_file):
    with open(input_file, 'r') as f:
        data = f.readlines()

    output_data = []
    for line in data:
        entry = eval(line.strip())  # Convert string to dictionary
        output_data.append(entry)

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=4)

if __name__ == "__main__":
    input_file = "output.txt"
    output_file = "output.json"
    convert_output_to_json(input_file, output_file)
