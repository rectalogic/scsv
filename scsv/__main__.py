import argparse
import json
import sys

from .parser import parse

parser = argparse.ArgumentParser(description="Convert SCSV to JSON.")
parser.add_argument("file", nargs="?", help="CSV file")
args = parser.parse_args()

with open(args.file) as f:
    for row in parse(f):
        json.dump(row, sys.stdout, indent=4)
        print()
