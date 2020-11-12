#!/usr/bin/python
import argparse
import imghdr
import hashlib
import os
from pathlib import Path
import shutil
import sys

ImageTypes = ['rgb', 'gif', 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'webp', 'exr']

ImageTypeByExt = {}
for t in ImageTypes:
    ImageTypeByExt[t] = t
ImageTypeByExt['jpg'] = 'jpeg'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['link', 'copy', 'move'], help='Action to apply')
    parser.add_argument('filenames', nargs='+', help='Files to rename')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    parser.add_argument('--types', nargs='+', choices=ImageTypes, default=['jpeg', 'png'], help='Allowed image types, space-separated')
    parser.add_argument('--force', '-f', action='store_true', help='Force file overwrite')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--method', '-m', choices=['default', 'md5-name', 'md5-content'], default='default', help='Fixing method')
    return parser.parse_args()


def image_type_to_ext(image_type):
    # use `jpg' instead of `jpeg'
    return 'jpg' if image_type == 'jpeg' else image_type


def image_type_from_ext(ext):
    return ImageTypeByExt.get(ext)


def get_image_type(path):
    # get type from data
    image_type = imghdr.what(path)
    if image_type is None and len(path.suffix):
        # fallback: get type from extension
        image_type = image_type_from_ext(path.suffix[1:])
    return image_type


def get_absolute_path(path):
    return Path(path) if path.is_absolute() else Path.cwd() / path


def fix(path, output_dir_path, args):
    image_type = get_image_type(path)

    # Check if image type is allowed
    if image_type not in args.types:
        print("  skipped, image type `{}' is not allowed".format(image_type))
        return

    # Make output file path
    ext = image_type_to_ext(image_type)
    if args.method == 'md5-name':
        m = hashlib.md5()
        m.update(path.name.encode('utf-8'))
        output_name = m.hexdigest() + '.' + ext
    elif args.method == 'md5-content':
        m = hashlib.md5();
        m.update(open(path, 'rb').read())
        output_name = m.hexdigest() + '.' + ext
    else:
        output_name = path.stem + '.' + ext
    output_path = output_dir_path / output_name

    # Check if output path matches input path
    if output_path == path:
        print("  skipped, same output path")
        return

    # Check if output file exists
    if output_path.exists():
        if args.force:
            # Remove old file
            output_path.unlink()
            if args.verbose:
                print("  old file {} removed".format(output_path))
        else:
            print("  skipped, output file {} exists (use -f to overwrite)".format(output_path))

    # Apply action
    # - link
    if args.action == "link":
        os.symlink(get_absolute_path(path), output_path)
        print("  symlink: {}".format(output_path))
    # - copy
    elif args.action == "copy":
        shutil.copy(path, output_path)
        print("  copy: {}".format(output_path))
    # - move
    elif args.action == "move":
        shutil.move(path, output_path)
        print("  moved: {}".format(output_path))


def main():
    args = parse_args()

    # Prepare output directory
    output_dir_path = Path(args.output)
    if not output_dir_path.exists():
        # make output dir
        output_dir_path.mkdir(parents=True)
    elif not output_dir_path.is_dir():
        # exists, but is not a directory
        print("{} exists, but is not a directory")
        sys.exit(-1)

    # Process files
    for filename in args.filenames:
        # create file path object
        path = Path(filename)
        if path.is_dir():
            # directory
            if args.verbose:
                print("Skipping directory `{}'".format(filename))
        elif not path.exists():
            # doesn't exist
            print("File `{}' not found".format(filename))
        else:
            # file (or symlink) exists
            print(filename)
            fix(path, output_dir_path, args)


if __name__ == "__main__":
    main()
