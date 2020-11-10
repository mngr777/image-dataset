#!/bin/bash
OutputDir="filtered"

for file in $*; do
    echo $file
    ./filter.py copy $file $OutputDir
    if [ $? -ne 0 ]; then exit; fi
done
