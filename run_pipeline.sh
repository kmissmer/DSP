#!/bin/bash
set -e


# Check if dataset argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dataset>"
  exit 1
fi

DATASET_PATH="$1"

DATASET=$(basename "$DATASET_PATH")

DATE=$(date +%Y-%m-%d)

# Run the pipeline with the specified dataset
python3 Information.py $DATASET_PATH
python3 NMLInformation.py $DATASET_PATH

# Convert outputs to JSON
python3 convert_output_to_json.py "output${DATASET}.txt"
python3 convert_output_to_json.py "NMLoutput${DATASET}.txt"

# Process JSON files
python3 process_files.py "output${DATASET}.json"

# Combine the processed files
python3 combine_json.py "output${DATASET}_processed.json" "NMLoutput${DATASET}.json" "${DATASET}_${DATE}.json"

# Convert combined JSON to CSV
python3 Json_To_CSV.py "${DATASET}_${DATE}.json"

# Format the CSV for database import
python3 DatabaseFormat.py "${DATASET}_${DATE}.csv"
