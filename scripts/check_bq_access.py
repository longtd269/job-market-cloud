import sys

from google.api_core.exceptions import BadRequest, Forbidden
from google.cloud import bigquery

from jmc import config

SHOULD_WRITE = ["raw", "staging", "intermediate", "marts"]
SHOULD_NOT_WRITE = ["lab"]

def can_write(client: bigquery.Client, dataset: str) -> bool:
    table = f"`{config.GCP_PROJECT}.{dataset}._access_check`"
    try:
        client.query(f"CREATE OR REPLACE TABLE {table} (x INT64); DROP TABLE {table};").result()
        return True
    except (BadRequest, Forbidden) as e:
        if "Access Denied" in str(e) or isinstance(e, Forbidden):
            return False
        raise

def main() -> int:
    client = bigquery.Client(project=config.GCP_PROJECT, location="us-central1")
    ok = True
    for dataset in SHOULD_WRITE + SHOULD_NOT_WRITE:
        expected = dataset in SHOULD_WRITE
        actual = can_write(client, dataset)
        status = "OK " if actual == expected else "WRONG "
        ok &= actual == expected
        print(f"{status} {dataset:<13} mong đợi ghi={expected}, thực tế ghi={actual}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())   