import os

import pytest

from scsv import parse

testdata = [
    (
        "test.csv",
        [
            {
                "patient": {"name": {"given": ["rob", "bob"], "family": "halford"}, "dob": "02/16/1993"},
                "iid": "cureatr",
                "insurance": [{"policy": "pol123"}, {"policy": "pol456"}],
                "tags": ["tag1", "tag2", "tag3"],
            },
            {
                "patient": {"name": {"given": ["joe", "joseph"], "family": "blow"}, "dob": "01/13/1984"},
                "iid": "davita",
                "insurance": [{"policy": "pol-abc"}, {"policy": "pol-def"}],
                "tags": ["tag1"],
            },
        ],
    ),
    (
        "override.csv",
        [
            {"name": "one", "tags": ["a", "b", "X", "d"]},
            {"name": "two", "tags": ["e", "", "Y"]},
            {"name": "three", "tags": ["h", "i", "Z"]},
        ],
    ),
]


@pytest.mark.parametrize("csv,results", testdata)
def test_parse(csv, results):
    with open(os.path.join(os.path.dirname(__file__), csv)) as f:
        assert list(parse(f)) == results
