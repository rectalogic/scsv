from __future__ import annotations

import csv
import re
import typing as ta
from collections import defaultdict

if ta.TYPE_CHECKING:
    import io


LISTKEY = re.compile(r"(\w+)\[(\d+|.)\]")


def tree() -> dict:
    return defaultdict(tree)


def parsekey(key: str) -> tuple[str, ta.Optional[ta.Union[str, int]]]:
    m = LISTKEY.fullmatch(key)
    if m:
        index = m.group(2)
        try:
            index = int(index)
        except ValueError:
            pass
        return m.group(1), index
    else:
        return key, None


def ensurelist(lst: list, index: int, itemfunc: ta.Callable[[], ta.Any]) -> None:
    lst.extend((itemfunc() for _ in range((index + 1) - len(lst))))


def getdictitem(item: dict, key: str) -> dict:
    return item[key]


def getlistitem(item: dict, key: str, index: int, itemfunc: ta.Callable[[], ta.Any]) -> ta.Any:
    if key not in item:
        item[key] = []
    ensurelist(item[key], index, itemfunc)
    return item[key][index]


def getitem(item: dict, key: str) -> dict:
    key, index = parsekey(key)
    if index is not None:
        return getlistitem(item, key, index, tree)
    else:
        return getdictitem(item, key)


def parse(f: io.TextIOBase) -> ta.Generator[dict, None, None]:
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
                if isinstance(index, int):
                    getlistitem(item, key, index, lambda: None)
                    item[key][index] = value
                elif isinstance(index, str):
                    item[key] = value.split(index)
            else:
                item[key] = value
        yield scsv
