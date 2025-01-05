#!/bin/bash

# Loop through each file or directory in /data/data/
for d in /data/data/* ; do
    # Execute run_pipeline.sh on each item
    ./run_pipeline.sh $d
done
