"""Ghi thử một partition vào data lake, chạy lại không trùng (DE-202)."""
import argparse
import json
from datetime import date

from google.api_core.exceptions import NotFound
from google.cloud import storage

PROJECT_ID = "jmc-01"
BUCKET = "jmc-01-lake"


def partition_prefix(source: str, ingest_date: date) -> str:
    return f"raw/source={source}/ingest_date={ingest_date.isoformat()}/"

def write_partition(client: storage.Client, source: str, ingest_date: date, records: list[dict]) -> str:
    bucket = client.bucket(BUCKET)
    prefix = partition_prefix(source, ingest_date)

    try:
        bucket.blob(prefix + "_SUCCESS").delete()
    except NotFound:
        pass

    for blob in client.list_blobs(BUCKET, prefix=prefix):
        blob.delete()

    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records) 
    bucket.blob(prefix + "part-000.jsonl").upload_from_string(
        body, content_type="application/x-ndjson"
    )   

    bucket.blob(prefix + "_SUCCESS").upload_from_string("")
    return prefix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()

    records = [
        {"job_id": "demo-1", "title": "Data Engineer", "city": "Hà Nội", "salary_text": "20 - 30 triệu"},
        {"job_id": "demo-2", "title": "Data Analyst", "city": "Hồ Chí Minh", "salary_text": "Thỏa thuận"},
        {"job_id": "demo-3", "title": "BI Developer", "city": "Đà Nẵng", "salary_text": "Up to 1500 USD"},
    ]
    client = storage.Client(project=PROJECT_ID)
    prefix = write_partition(client, "demo", args.date, records)

    print(f"Đã ghi gs://{BUCKET}/{prefix}")
    for blob in client.list_blobs(BUCKET, prefix=prefix):
        print(f"  {blob.name}  {blob.size} bytes")

if __name__ == "__main__":
    main()