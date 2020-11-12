#!/bin/bash
OutputDir="filtered"

mkdir -p "$OutputDir"

for file in $*; do
    echo $file
    ./filter.py --processed "$OutputDir/.processed" copy $file "$OutputDir"
    if [ $? -ne 0 ]; then exit; fi
done
