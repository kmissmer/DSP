import json
import sys
from collections import Counter

def main(filename):
    # Load the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Extract names from each entry and flatten the list
    all_names = [name for entry in data for name in entry.get('names', [])]

    # Count occurrences of each name
    name_counts = Counter(all_names)

    # Get the top 100 names
    top_100_names = name_counts.most_common(100)

    # Print the top 100 names
    for name, count in top_100_names:
        print(f'{name}: {count}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 top_names.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)