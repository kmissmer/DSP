import spacy
import os
import json
from datetime import datetime
import sys

def extract_organization_name(file_path):
    parts = file_path.split('/')
    data_index = parts.index('data')
    organization_name = parts[data_index + 2]
    return organization_name

def extract_docket_name(file_path):
    parts = file_path.split('/')
    data_index = parts.index('data')
    docket_name = parts[data_index + 3]
    return docket_name

def extract_file_type(file_path):
    parts = file_path.split('/')
    file_type = parts.index('data')
    file_type = parts[file_type + 5]
    return file_type

def extract_year_from_docket_id(docket_id):
    if not docket_id:
        return None
    try:
        return int(docket_id.split('-')[1])
    except (IndexError, ValueError):
        return None

def chunk_reader(file_path, chunk_size=100000):
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
                if len(cleaned_name.split()) > 1:
                    names.append(cleaned_name)
    return names

def process_files(file_path, nlp):
    NamesExtracted = []
    try:
        print(f"Processing file: {file_path}")
        start_time = datetime.now()
        file_size = os.path.getsize(file_path)
        print("File Size:", file_size, "bytes")
        chunk_count = 0
        for chunk in chunk_reader(file_path):
            chunk_count += 1
            names = extract_names(nlp, chunk)
            NamesExtracted.extend(names)
            if chunk_count % 10 == 0:
                print(f"Processed {chunk_count * 100000} characters...")
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print("Time taken to process:", elapsed_time)
        print("Done!")
        return NamesExtracted
    except (json.JSONDecodeError, OSError) as error:
        print(f"Error processing file {file_path}: {str(error)}")
        return []

def find_names_in_everything(directory_path):
    nlp = spacy.load("en_core_web_lg")
    nlp.max_length = 1000000

    results = []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            abs_file_path = os.path.abspath(file_path)
            base_filename = os.path.basename(file_path)

            if file.endswith(('.htm', '.txt')):
                org_name = extract_organization_name(file_path)
                output_filename = f"output{org_name}.txt"

                # Check if the file has already been processed for this organization
                processed_files = set()
                if os.path.exists(output_filename):
                    with open(output_filename, 'r') as output_file:
                        try:
                            for line in output_file:
                                entry = json.loads(line.strip())
                                processed_filename = entry.get("FileName")
                                if processed_filename:
                                    processed_files.add(processed_filename.strip())
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in {output_filename}")

                if base_filename in processed_files:
                    print(f"Skipping {file}. Already processed.")
                    continue

                names = process_files(file_path, nlp)

                if names:
                    result = {
                        "Organization": org_name,
                        "FileName": base_filename,
                        "FileSize": os.path.getsize(file_path),
                        "DocketID": extract_docket_name(file_path),
                        "FileType": extract_file_type(file_path),
                        "Name": names,
                        "Year": extract_year_from_docket_id(extract_docket_name(file_path)),
                        "FilePath": abs_file_path
                    }
                    results.append(result)
                    with open(output_filename, "a") as text_file:
                        text_file.write(json.dumps(result))
                        text_file.write("\n")
                else:
                    result = {
                        "Organization": org_name,
                        "FileName": base_filename,
                        "FileSize": os.path.getsize(file_path),
                        "DocketID": extract_docket_name(file_path),
                        "FileType": extract_file_type(file_path),
                        "Name": None,
                        "Year": extract_year_from_docket_id(extract_docket_name(file_path)),
                        "FilePath": abs_file_path
                    }
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