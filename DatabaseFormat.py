import csv
import sys
from collections import defaultdict

def remove_null_bytes(input_file_path, cleaned_file_path):
    with open(input_file_path, 'rb') as infile, open(cleaned_file_path, 'wb') as outfile:
        for line in infile:
            outfile.write(line.replace(b'\x00', b''))

def process_csv(input_file_path):
    cleaned_file_path = 'cleaned_' + input_file_path

    # Remove null bytes
    remove_null_bytes(input_file_path, cleaned_file_path)

    try:
        # Read the cleaned CSV file
        with open(cleaned_file_path, mode='r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            data = [row for row in csvreader]

        # Group data by Organization
        organizations = defaultdict(list)
        for row in data:
            org = row['Organization']
            organizations[org].append(row)

        for org, rows in organizations.items():
            # Process and write the INFO file
            info_file_path = f"{org}_INF.csv"
            with open(info_file_path, mode='w', newline='') as infofile:
                fieldnames = ['FileName', 'Organization', 'FileSize', 'DocketID', 'FileType', 'Year', 'FilePath']
                csvwriter = csv.DictWriter(infofile, fieldnames=fieldnames)
                csvwriter.writeheader()
                for row in rows:
                    csvwriter.writerow({
                        'FileName': row['FileName'],
                        'Organization': row['Organization'],
                        'FileSize': row['FileSize'],
                        'DocketID': row['DocketID'],
                        'FileType': row['FileType'],
                        'Year': row['Year'],
                        'FilePath': row['FilePath']
                    })

            # Process and write the Name file
            name_file_path = f"{org}_Name.csv"
            with open(name_file_path, mode='w', newline='') as namefile:
                fieldnames = ['FileName', 'Name', 'Count']
                csvwriter = csv.DictWriter(namefile, fieldnames=fieldnames)
                csvwriter.writeheader()
                for row in rows:
                    csvwriter.writerow({
                        'FileName': row['FileName'],
                        'Name': row['Name'],
                        'Count': row['Count']
                    })

        print(f'Processed data and saved it in "{info_file_path}" and "{name_file_path}".')

    except FileNotFoundError:
        print(f"Error: Input file '{cleaned_file_path}' not found.")
    except csv.Error as e:
        print(f"Error reading CSV file '{cleaned_file_path}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 process_csv.py InputFile")
        sys.exit(1)

    input_file_path = sys.argv[1]
    process_csv(input_file_path)
