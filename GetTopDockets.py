import sys

def get_top_dockets(input_file, output_file, top_n=50):
    docket_counts = []

    # Read the input file and process each line
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                docket_name, count_str = line.rsplit(' - ', 1)
                count = int(count_str.split()[0])
                docket_counts.append((docket_name, count))

    # Sort the dockets by file count in descending order and get the top N
    docket_counts.sort(key=lambda x: x[1], reverse=True)
    top_dockets = docket_counts[:top_n]

    # Write the top dockets to the output file
    with open(output_file, 'w') as f:
        for docket_name, count in top_dockets:
            f.write(f"{docket_name} - {count} files\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 GetTopDockets.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

        get_top_dockets(input_file, output_file)
        print(f"Results written to {output_file}")