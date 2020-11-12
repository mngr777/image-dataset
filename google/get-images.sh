#!/bin/bash

query="$*"

source config.sh

# Search for images, store URLs in temp file
found_url_file=$(mktemp)
echo "Temporary image URL list file: " $found_url_file
./search.py --apikey $ApiKey --cseid $CseId --imgsize $ImgSize --output $found_url_file --pagenum 10 -- $query
if [ $? -ne 0 ]; then exit; fi

# Subtract already used URLs
download_url_file=$(mktemp)
touch $UsedUrlFile
# `-F' for fixed strings (not patterns)
# `-x' for whole line match
# `-v' to output non-matches
# `-f <path>' is pattern file
grep -Fxv -f $UsedUrlFile $found_url_file > $download_url_file

# Download images
mkdir -p $OutputDir
echo "Downloading images into " $OutputDir
parallel <$download_url_file -j 4 wget -nc --timeout=5 --tries=3 --directory-prefix=$OutputDir {}

# Update list of used URLs
cat $download_url_file >> $UsedUrlFile

# Fix image file names
echo "Fixing image file names"
./fix-filenames.py move --method md5-content --types jpeg png --output $OutputDir -- $OutputDir/*
