from __future__ import annotations

import csv
import re
import typing as ta
from collections import defaultdict

if ta.TYPE_CHECKING:
    import io

    Tree = dict[str, Item]
    List = ta.Union[list[Tree], list[str]]
    Item = ta.Union[str, Tree, List]

LISTKEY = re.compile(r"(\w+)\[(\d+|.)\]")


def tree() -> Tree:
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


def ensurelist(lst: List, index: int, itemfunc: ta.Callable[[], ta.Any]) -> None:
    lst.extend((itemfunc() for _ in range((index + 1) - len(lst))))


def getdictitem(item: Tree, key: str) -> Item:
    return item[key]


def getlist(item: Tree, key: str, index: int, itemfunc: ta.Callable[[], ta.Any]) -> List:
    if key not in item:
        item[key] = ta.cast("List", [])
    lst = item[key]
    if not isinstance(lst, list):
        raise ValueError(f"{key} is not a list")
    ensurelist(lst, index, itemfunc)
    return lst


def getlistitem(item: Tree, key: str, index: int, itemfunc: ta.Callable[[], ta.Any]) -> Item:
    lst = getlist(item, key, index, itemfunc)
    return lst[index]


def getitem(item: Tree, key: str) -> Item:
    key, index = parsekey(key)
    if isinstance(index, int):
        return getlistitem(item, key, index, tree)
    else:
        return getdictitem(item, key)


def parse(f: io.TextIOBase) -> ta.Generator[Tree, None, None]:
    reader = csv.DictReader(f)
    for row in reader:
        scsv = tree()
        for keypath, value in ta.cast(dict[str, str], row).items():
            keys = keypath.split(".")
            item = scsv
            for key in keys[:-1]:
                item = ta.cast("Tree", getitem(item, key))
            key, index = parsekey(keys[-1])

            if isinstance(index, int):
                lst = getlist(item, key, index, lambda: "")
                lst[index] = value
            elif isinstance(index, str):
                item[key] = value.split(index)
            else:
                item[key] = value
        yield scsv
