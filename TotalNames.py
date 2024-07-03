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
    if entry['names'] or entry['Name'] is not None:
        total_names += len(entry['names'] or entry['Name'])

print("Total number of names:", total_names)
