#!/bin/bash
while read query; do
    if [ ! -z "$query" ]; then
        echo "Getting image results for query \`$query'"
    fi
    ./get-images.sh $query
done < $1
