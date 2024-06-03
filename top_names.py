import json
import sys
from collections import Counter

def main(filename):
    # Load the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Extract full names from each entry
    all_full_names = [name for entry in data for name in entry.get('names', [])]

    # Count occurrences of each full name
    full_name_counts = Counter(all_full_names)

    # Get the top 100 full names
    top_100_full_names = full_name_counts.most_common(100)

    # Print the top 100 full names
    for name, count in top_100_full_names:
        print(f'{name}: {count}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 top_names.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)