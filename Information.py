import spacy
import os
import json
from datetime import datetime
import sys


def chunk_reader(file_path, chunk_size=1000000):
    with open(file_path, 'r', errors='ignore') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk


def extract_names(nlp, chunk):
    doc = nlp(chunk)
    names = []
    if doc.ents:
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                cleaned_name = " ".join(ent.text.split())
                names.append(cleaned_name)
    return names


def process_files(file_path, nlp):
    NamesExtracted = []
    try:
        print(f"Processing file: {file_path}")  # Display the file being processed
        start_time = datetime.now()
        file_size = os.path.getsize(file_path)
        print("File Size:", file_size, "bytes")  # Display file size
        for chunk in chunk_reader(file_path):
            names = extract_names(nlp, chunk)
            NamesExtracted.extend(names)

        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("Time taken to process:", elapsed_time)  # Display the time taken
        print("Done!")
        return NamesExtracted

    except (json.JSONDecodeError, OSError) as error:
        print(f"Error processing file {file_path}: {str(error)}")
        return []


def find_names_in_everything(directory_path):
    output_filename = "output.txt"
    processed_files = set()

    # Load spaCy model with increased max_length limit
    nlp = spacy.load("en_core_web_lg")
    nlp.max_length = 1000000  # Set max_length to 1 million characters

    if os.path.exists(output_filename):
        with open(output_filename, "r") as output_file:
            try:
                data = output_file.readlines()

                for line in data:
                    entry = json.loads(line)
                    filename = entry.get("filename")
                    if filename:
                        processed_files.add(filename)
            except json.JSONDecodeError:
                pass

    results = []
    errors = []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)


            if file_path in processed_files:
                print(f"Skipping {file_path}. Already processed.")
                continue

            if file.endswith(('.htm', '.txt')):
                names = process_files(file_path, nlp)
                if names:
                    result = {"filename": file_path, "filesize": file_size, "names": names}
                else:
                    result = {"filename": file_path, "filesize": file_size}
                processed_files.add(file_path)
                results.append(result)

                with open(output_filename, "a") as text_file:
                    text_file.write(json.dumps(result))
                    text_file.write("\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 <script_name.py> <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    find_names_in_everything(directory_path)