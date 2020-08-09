#!/usr/bin/python
import argparse
from googleapiclient.discovery import build
import sys

ImgSizes = ['huge', 'icon', 'large', 'medium', 'small', 'xlarge', 'xxlarge']
ImgTypes = ['clipart', 'face', 'lineart', 'stock', 'photo', 'animated']

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='+', help='Query terms')
    parser.add_argument('--apikey', required=True, help='API key')
    parser.add_argument('--cseid', required=True, help='Custom Search Engine ID')
    parser.add_argument('--pagesize', type=int, default=10, help='Page size, max value is 10')
    parser.add_argument('--pagenum', type=int, default=10, help='# of pages')
    parser.add_argument('--start', type=int, default=0, help='Start page')
    parser.add_argument('--imgtype', choices=ImgTypes, default='photo', help='Image type')
    parser.add_argument('--imgsize', choices=ImgSizes, default='xlarge', help='Image size')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--append', '-a', action='store_true', help='Append to output file')
    return parser.parse_args()


def output_result(output, result):
    for item in result['items']:
        print(item['link'], file=output)


def main():
    args = parse_args()

    # Open output file or use stdout
    output = sys.stdout
    if args.output and args.output != '-':
        mode = 'a' if args.append else 'w'
        output = open(args.output, mode)

    # Create CSE client
    service = build('customsearch', 'v1', developerKey=args.apikey)
    cse = service.cse()

    # Search
    search_string = ' '.join(args.query)
    for i in range(0, args.pagenum):
        start = (args.start + i) * args.pagesize
        request = cse.list(q=search_string, cx=args.cseid, num=args.pagesize, start=start, searchType="image", imgType=args.imgtype, imgSize=args.imgsize.upper())
        result = request.execute()
        output_result(output, result)

if __name__ == "__main__":
    main()
