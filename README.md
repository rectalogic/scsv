# scsv
Structured CSV

Given this SCSV:

https://github.com/rectalogic/scsv/blob/develop/test.csv#L1-L3

Generate this JSON:

```sh-session
$ bin/ensure-poetry
$ bin/poetry install
$ bin/poetry run python -m scsv test.csv
```

```json
{
    "patient": {
        "name": {
            "given": [
                "rob",
                "bob"
            ],
            "family": "halford"
        },
        "dob": "02/16/1993"
    },
    "iid": "cureatr",
    "insurance": [
        {
            "policy": "pol123"
        },
        {
            "policy": "pol456"
        }
    ],
    "tags": [
        "tag1",
        "tag2",
        "tag3"
    ]
}
{
    "patient": {
        "name": {
            "given": [
                "joe",
                "joseph"
            ],
            "family": "blow"
        },
        "dob": "01/13/1984"
    },
    "iid": "davita",
    "insurance": [
        {
            "policy": "pol-abc"
        },
        {
            "policy": "pol-def"
        }
    ],
    "tags": [
        "tag1"
    ]
}

```
