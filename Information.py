import spacy
import os
import json
import re
from datetime import datetime
import sys


def chunk_reader(file_content, nlp):
    doc = nlp(file_content)
    return doc
    
def extractInformation(doc):
    names = []
    emails = []
    organizations = []
    if doc.ents:
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                names.append(ent.text)
            if ent.label_ == "EMAIL":
                emails.append(ent.text)
            if ent.label_ == "ORG":
                organizations.append(ent.text)
        
    return names,emails,organizations



def process_files(file_path,nlp):
    NamesExtracted = []
    EmailsExtracted = []
    OrganizationsExtracted = []
    try:
        print(f"Processing file: {file_path}")  # Display the file being processed
        print("Start Time:", datetime.now())  #display time it started processing

        with open(file_path, 'r') as file:
            content = file.read()
            
            start_idx = 0
            chunk_size = 1000000  # 1 million characters per chunk
            for start_idx in range(0, len(content), chunk_size):
                chunk_text = content[start_idx:start_idx + chunk_size]
                doc = chunk_reader(chunk_text, nlp)
                NamesExtracted,EmailsExtracted,OrganizationsExtracted = extractInformation(doc)
        print("Done!")
        return NamesExtracted,EmailsExtracted, OrganizationsExtracted

    except (json.JSONDecodeError, OSError) as error:
        print(f"Error processing file {file_path}: {str(error)}")
        return [],[],[]
    




def find_names_in_everything(directory_path):
    output_filename = "output.txt"
    processed_files = set()

    nlp = spacy.load("en_core_web_lg")

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

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)

            if file_path in processed_files:
                print(f"Skipping {file_path}. Already processed.")
                continue

            if file.endswith(('json','.htm','.txt')):
                names, emails, organizations = process_files(file_path, nlp)
                result = {"filename": file_path}
                if names:
                    result["names"] = names
                if emails:
                    result["emails"] = emails
                if organizations:
                    result["organizations"] = organizations
               
                if names or emails or organizations:
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