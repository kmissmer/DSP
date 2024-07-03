import json
import sys

if len(sys.argv) != 2:
    print("Usage: python3 script.py <path_to_json_file>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error decoding JSON from file: {file_path}")
    sys.exit(1)

total_names = 0

for entry in data:
    # Check if 'names' is a list and count its elements if it's not None
    names_list = entry.get('names')
    if names_list is not None:
        total_names += len(names_list)

    # Check if 'Name' is a non-null string
    name_string = entry.get('Name')
    if name_string and name_string.lower() != 'null':
        total_names += 1

print("Total number of names:", total_names)
