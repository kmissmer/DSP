import json
from collections import Counter

# Load the JSON file
with open('output.json', 'r') as file:
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
