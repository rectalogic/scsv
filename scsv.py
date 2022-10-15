import csv
import json
import re
import sys
from collections import defaultdict

LISTKEY = re.compile(r"(\w+)\[(\d+)\]")
NOTSET = object()


def tree():
    return defaultdict(tree)


def parsekey(key):
    m = LISTKEY.fullmatch(key)
    if m:
        return m.group(1), int(m.group(2))
    else:
        return key, None


def ensurelist(lst, index, itemfunc):
    lst.extend((itemfunc() for _ in range((index + 1) - len(lst))))


def getdictitem(item, key):
    return item[key]


def getlistitem(item, key, index, itemfunc):
    if key not in item:
        item[key] = []
    ensurelist(item[key], index, itemfunc)
    return item[key][index]


def getitem(item, key):
    key, index = parsekey(key)
    if index is not None:
        return getlistitem(item, key, index, tree)
    else:
        return getdictitem(item, key)


def parse(f):
    reader = csv.DictReader(f)
    for row in reader:
        scsv = tree()
        for keypath, value in row.items():
            keys = keypath.split(".")
            item = scsv
            for key in keys[:-1]:
                item = getitem(item, key)
            key, index = parsekey(keys[-1])
            if index is not None:
                getlistitem(item, key, index, lambda: None)
                item[key][index] = value
            else:
                item[key] = value
        yield scsv


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        for row in parse(f):
            json.dump(row, sys.stdout, indent=4)
