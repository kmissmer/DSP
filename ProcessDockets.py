import os
import sys

def process_dockets(input_file, output_file):
    docket_counts = {}

    # Read the input file and process each line
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                docket_name, count_str = line.rsplit(' - ', 1)
                count = int(count_str.split()[0])
                if docket_name not in docket_counts or count > docket_counts[docket_name]:
                    docket_counts[docket_name] = count

    # Write the docket with the highest count for each docket to the output file
    with open(output_file, 'w') as f:
        for docket_name, count in docket_counts.items():
            f.write(f"{docket_name} - {count} files\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 ProcessDockets.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        process_dockets(input_file, output_file)
        print(f"Results written to {output_file}")