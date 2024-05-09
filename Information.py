from concurrent.futures import ThreadPoolExecutor
import spacy
import os
import json
from datetime import datetime
import sys

def chunk_reader(file_content, nlp):
    doc = nlp(file_content)
    return doc

def extract_information(doc):
    names = set()
    emails = set()
    organizations = set()
    if doc.ents:
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                names.add(ent.text)
            elif ent.label_ == "EMAIL":
                emails.add(ent.text)
            elif ent.label_ == "ORG":
                organizations.add(ent.text)
    return list(names), list(emails), list(organizations)

def process_chunk(chunk, nlp):
    doc = chunk_reader(chunk, nlp)
    return extract_information(doc)

def process_file(file_path, nlp):
    try:
        print(f"Processing file: {file_path}")
        print("Start Time:", datetime.now())

        with open(file_path, 'r') as file:
            content = file.read()
            chunk_size = 1000000  # 1 million characters per chunk
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda chunk: process_chunk(chunk, nlp), chunks))

        NamesExtracted, EmailsExtracted, OrganizationsExtracted = zip(*results)
        return list(sum(NamesExtracted, [])), list(sum(EmailsExtracted, [])), list(sum(OrganizationsExtracted, []))

    except OSError as error:
        print(f"Error processing file {file_path}: {str(error)}")
        return [], [], []

def find_names_in_everything(directory_path):
    output_filename = "output.txt"
    processed_files = set()

    nlp = spacy.load("en_core_web_lg")

    if os.path.exists(output_filename):
        with open(output_filename, "r") as output_file:
            try:
                data = output_file.readlines()
                processed_files.update(json.loads(line)["filename"] for line in data)
            except json.JSONDecodeError:
                pass

    results = []

    def process_file_and_save(file_path):
        if file_path in processed_files:
            print(f"Skipping {file_path}. Already processed.")
            return

        if file_path.endswith(('json', '.htm', '.txt')):
            names, emails, organizations = process_file(file_path, nlp)
            if any([names, emails, organizations]):
                result = {"filename": file_path, "names": names, "emails": emails, "organizations": organizations}
                with open(output_filename, "a") as text_file:
                    json.dump(result, text_file)
                    text_file.write("\n")

    files_to_process = [os.path.join(root, file) for root, _, files in os.walk(directory_path) for file in files]

    with ThreadPoolExecutor() as executor:
        executor.map(process_file_and_save, files_to_process)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 <script_name.py> <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    find_names_in_everything(directory_path)
