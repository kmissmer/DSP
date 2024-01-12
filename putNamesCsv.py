import spacy
import os
import json
from nameparser import HumanName

def find_names_in_documents(directory_path):
    nlp = spacy.load("en_core_web_sm")

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.json'):
                try:
                    with open(file_path, 'r') as json_file:
                        content = json_file.read()

                    doc = nlp(content)
                    names = []
                    for ent in doc.ents:
                        if ent.label_ == "PERSON":
                            human_name = HumanName(ent.text)
                            if len(ent.text) > 3 and human_name.first != '' and human_name.last != '':
                                if "Value" not in ent.text and "Submitted" not in ent.text:
                                    if "<" not in ent.text and ">" not in ent.text:  # Exclude entities containing "<" or ">"
                                        names.append(ent.text)

                    if names:
                        print(file_path)  # Output the directory path
                        print(names)  # Output the list of names

                except (json.JSONDecodeError, KeyError) as error:
                    print(f"Error parsing JSON in file {file_path}: {str(error)}")

if __name__ == "__main__":
    find_names_in_documents("/Users/missmerk/Desktop/DataScienceProejct/FDA-2012-N-1210/text-FDA-2012-N-1210")