#!/bin/bash

query="$*"

ApiKey="<API key>"
CseId="<Custom Search Engine ID>"
OutputDir='result'
ImgSize='xlarge'

# Search for images, store URLs in temp file
url_file=`mktemp`
echo "Temporary image URL list file: " $url_file
./search.py --apikey $ApiKey --cseid $CseId --imgsize $ImgSize --output $url_file --pagenum 1 -- $query
if [ $? -neq 0 ]; then exit; fi

# Download images
mkdir -p $OutputDir
echo "Downloading images into " $OutputDir
parallel <$url_file -j 4 wget -nc --timeout=5 --tries=3 --directory-prefix=$OutputDir {}

# Fix image file names
echo "Fixing image file names"
./fix-filenames.py move --types jpeg png --output $OutputDir -- $OutputDir/*

