#!/usr/bin/python
import argparse
import os
from pathlib import Path
import tkinter as tk
import shutil
import sys
from PIL import Image, ImageTk

def parse_args():
    binding_description = """
Bindings:
  a         Apply action end exit with success status
  <space>   Exit with success status
  <Escape>  Exit with error status.

Exit status is supposed to be used for breaking cycle in wrapper script.
"""
    parser = argparse.ArgumentParser(
        epilog=binding_description,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('action', choices=['link', 'copy', 'move'], help='Action to apply')
    parser.add_argument('image', help='Image file')
    parser.add_argument('output_dir', help='Output dir')
    parser.add_argument('--processed', '-p', required=False, help='File containing a list of processed files.')
    return parser.parse_args()

def get_absolute_path(path):
    return Path(path) if path.is_absolute() else Path.cwd() / path

def load_processed(path):
    processed = {}
    with open(path, 'r') as f:
        for line in f:
            processed[line[:-1]] = True
    return processed

def main():
    # Parse arguments
    args = parse_args()

    # Make paths
    image_path = Path(args.image)
    target_path = Path(args.output_dir) / image_path.name
    processed_path = Path(args.processed) if args.processed else None

    # Check if output dir exists
    if not os.path.isdir(args.output_dir):
        sys.exit(-1)

    # Load processed files
    processed = {}
    if processed_path:
        if processed_path.is_file():
            processed = load_processed(processed_path)
        else:
            print("File `{}' does not exist".format(processed_path))

    # Check if file is in processed list
    if image_path.name in processed:
        print("File `{}' has already been processed, skipping".format(image_path.name))
        sys.exit(0)

    # Check if file exists
    if target_path.exists():
        print("File `{}' already exists, skipping".format(target_path))
        sys.exit(0)

    # Init Tk
    root = tk.Tk()

    # Load imagek
    image = Image.open(image_path)
    image_tk = ImageTk.PhotoImage(image)

    # Main frame
    content = tk.Frame(root)
    content.grid()

    # Create canvas and show image
    canvas = tk.Canvas(content, width=image_tk.width(), height=image_tk.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk, tags="image")
    canvas.grid()

    # Adding file to processed list
    def add_to_processed():
        if processed_path:
            with open(processed_path, 'a') as f:
                print(image_path.name, file=f)

    ## Bind actions
    def apply_action(_):
        action = args.action
        if (action == 'link'):
            os.symlink(get_absolute_path(image_path), target_path)
            print("  symlink: {}".format(target_path))
        elif (action == 'copy'):
            shutil.copy(image_path, target_path)
            print("  copy: {}".format(target_path))
        elif (action == 'move'):
            shutil.move(image_path, target_path)
            print("  moved: {}".format(target_path))
        else:
            raise Exception('invalid action {}'.format(action));
        add_to_processed()
        sys.exit(0)
    root.bind('a', apply_action)
    root.bind('<Return>', apply_action)

    def skip(_):
        add_to_processed()
        sys.exit(0)
    root.bind('<space>', skip)

    def stop(_):
        sys.exit(-1)
    root.bind('<Escape>', stop)

    # Loop
    root.mainloop()

if __name__ == "__main__":
    main()
