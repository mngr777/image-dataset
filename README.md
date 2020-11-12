# image-dataset

This is a bunch of Python and bash scripts cobbled together to automate getting
images from Google search via API calls.
Creating Custom Search Engine is required. This page seems relevant:
https://support.google.com/programmable-search/answer/4513882

## Dependencies

* Python 3.*
* google-api-python-client (checked with 1.10.0)

## Setting up

    $ git clone <this-repo> [image-dataset]
    $ cd image-dataset
    $ cp config.sample.sh config.sh

Edit config.sh to replace `<ApiKey>` and `<CseId>` placeholders
with corresponding values for your CSE.

## Downloading images

Single query:

    $ cd image-dataset/google
    $ ./get-images.sh grizzly bear


Multiple queries:

    $ cd image-dataset/google
    $ echo black bear > queries.txt
    $ echo teddy bear >> queries.txt
    $ ./get-images-all.sh queries.txt

By default images are downloaded into `image-dataset/google/result` directory
and renamed to `<md5-of-file-contents>.<image-ext>`
(e.g. `9589f334c6f4987fc5ddb8e0ac1c096b.jpg`). Image URLs are stored
in `urls.txt` after images are downloaded to avoid downloading from same URL twice.

## Filtering images

    $ cd image-dataset
    $ ./filter.sh google/result/*

Each image will be shown in a window. Press `a` to copy to output dir, `space` to skip
or `Escape` to stop filtering. By default images are copied to `filtered` directory,
names (without path) of copied or skipped files are appended to `filtered/.processed` file,
this files will be later skipped automatically.
