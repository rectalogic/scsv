from __future__ import annotations

import csv
import io
import re
import typing as ta
from collections import defaultdict

if ta.TYPE_CHECKING:
    Tree: ta.TypeAlias = dict[str, TreeItem]
    TreeList: ta.TypeAlias = list[Tree] | list[str]
    TreeItem: ta.TypeAlias = str | Tree | TreeList
    SCSV: ta.TypeAlias = Tree
    T = ta.TypeVar("T", Tree, str)
    ItemFunc: ta.TypeAlias = ta.Callable[[], T]

LISTKEY = re.compile(r"(\w+)\[(\d+|.)\]")


class SCSVError(Exception):
    pass


def tree() -> Tree:
    return defaultdict(tree)


def parsekey(key: str) -> tuple[str, str | int | None]:
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


def is_str_list(lst: list[ta.Any]) -> ta.TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in lst)


def is_tree_list(lst: list[ta.Any]) -> ta.TypeGuard[list[Tree]]:
    return all(isinstance(x, dict) for x in lst)


def is_tree(t: ta.Any) -> ta.TypeGuard[Tree]:
    return isinstance(t, dict)


def ensurelist(lst: list[T], index: int, itemfunc: ItemFunc[T]) -> list[T]:
    lst.extend((itemfunc() for _ in range((index + 1) - len(lst))))
    return lst


def get_nonleaf_dictitem(item: Tree, key: str) -> Tree:
    node = item[key]
    if not isinstance(node, dict):
        raise SCSVError(f"{key} is not a dict")
    return node


def get_leaf_list(item: Tree, key: str, index: int) -> list[str]:
    if key not in item:
        item[key] = [""]
    lst = item[key]
    if not isinstance(lst, list):
        raise SCSVError(f"{key} not a list")
    if is_str_list(lst):
        return ensurelist(lst, index, str)
    raise SCSVError(f"{key} not a string list")


def get_nonleaf_listitem(item: Tree, key: str, index: int) -> Tree:
    if key not in item:
        item[key] = [tree()]
    lst = item[key]
    if not isinstance(lst, list):
        raise SCSVError(f"{key} not a list")
    if is_tree_list(lst):
        treelist = ensurelist(lst, index, tree)
        return treelist[index]
    raise SCSVError(f"{key} not a dict list")


def get_nonleaf_item(item: Tree, key: str) -> Tree:
    key, index = parsekey(key)
    if isinstance(index, int):
        return get_nonleaf_listitem(item, key, index)
    else:
        return get_nonleaf_dictitem(item, key)


def neuter(d: Tree) -> Tree:
    if isinstance(d, defaultdict):
        d.default_factory = None
    for v in d.values():
        if isinstance(v, dict):
            neuter(v)
    return d


def parse_scsv(row: dict[str, str]) -> SCSV:
    scsv = tree()
    for keypath, value in row.items():
        keys = keypath.split(".")
        item = scsv
        for key in keys[:-1]:
            item = get_nonleaf_item(item, key)
        key, index = parsekey(keys[-1])

        if isinstance(index, int):
            lst = get_leaf_list(item, key, index)
            lst[index] = value
        elif isinstance(index, str):
            item[key] = value.split(index)
        else:
            item[key] = value
    # Disable defaultdict functionality
    return neuter(scsv)


def parse(f: io.TextIOBase) -> ta.Generator[SCSV, None, None]:
    reader = csv.DictReader(f)
    for row in reader:
        yield parse_scsv(row)
