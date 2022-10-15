# scsv
Structured CSV

Given this SCSV:

https://github.com/rectalogic/scsv/blob/801e4fd9f5d84f5283a3682ebe1d5e88949e03fa/test.scsv#1

Generate this JSON:

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
    ]
}
```
