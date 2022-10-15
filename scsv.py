from collections import defaultdict
import csv
import sys
import json


def tree():
    return defaultdict(tree)


def parse(f):
    reader = csv.DictReader(f)
    for row in reader:
        scsv = tree()
        for keypath, value in row.items():
            keys  = keypath.split(".")
            item = scsv
            for key in keys[:-1]:
                item = item[key]
            item[keys[-1]] = value
        yield scsv


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        for row in parse(f):
            json.dump(row, sys.stdout, indent=4)
