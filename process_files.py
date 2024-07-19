import os
import json
import spacy

# Load Spacy model
nlp = spacy.load("en_core_web_sm")

# Directory containing the files
directory = 'path_to_directory'

# Function to process a single JSON file
def process_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return extract_names(data, count=1)  # Count is set to 1 for JSON files

# Function to extract names from text
def extract_names(text, count=1):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return {name: count for name in names}

# Function to process files and aggregate counts
def process_files(directory):
    aggregated_counts = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith('.json'):
            names_counts = process_json_file(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
            names_counts = extract_names(text)
        
        for name, count in names_counts.items():
            if name in aggregated_counts:
                aggregated_counts[name] += count
            else:
                aggregated_counts[name] = count

    return aggregated_counts

# Main function to run the processing
def main():
    aggregated_counts = process_files(directory)
    for name, count in aggregated_counts.items():
        print(f'{name}: {count}')

if __name__ == "__main__":
    main()
