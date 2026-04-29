CATEGORY_COLUMNS = [
    "Company public response",
    "Tags",
    "Consumer consent provided?",
    "Submitted via",
    "Company response to consumer",
    "Timely response?",
    "Consumer disputed?",
]

DATASET_TYPES = {
    "Tag": "category",
    "Consumer Claim": "string",
    "Company public response": "category",
    "Company": "string",
    "State": "string",
    "ZIP code": "string",
    "Tags": "category",
    "Consumer consent provided?": "category",
    "Submitted via": "category",
    "Company response to consumer": "category",
    "Timely response?": "category",
    "Consumer disputed?": "category",
    "Complaint ID": "int64",
}

DATASET_DATES = ["Date received", "Date sent to company"]
