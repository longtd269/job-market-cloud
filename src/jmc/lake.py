from datetime import date

from google.api_core.exceptions import NotFound
from google.cloud import storage

SUCCESS = "_SUCCESS"

class LandingNotReady(Exception):
    """Landing của ngày cần xử lý chưa có _SUCCESS."""

def landing_prefix(source: str, ingest_date: date) -> str:
    return f"landing/source={source}/ingest_date={ingest_date.isoformat()}/"

def raw_prefix(source: str, ingest_date: date) -> str:
    return f"raw/source={source}/ingest_date={ingest_date.isoformat()}/"

def replace_prefix(client: storage.Client, bucket_name: str, prefix: str, 
                   files: dict[str, tuple[str, str]]) -> None:
    bucket = client.bucket(bucket_name)
    try:
        bucket.blob(prefix + SUCCESS).delete()
    except NotFound:
        pass

    for blod in client.list_blobs(bucket_name, prefix=prefix):
        blod.delete()

    for name, (body, content_type) in files.items():
        bucket.blob(prefix + name).upload_from_string(body, content_type)

    bucket.blob(prefix + SUCCESS).upload_from_string("")

def read_landing_pages(client: storage.Client, bucket_name: str, 
                       source: str, ingest_date: date ) -> list[tuple[str, str]]:
    prefix =  landing_prefix(source, ingest_date)
    blobs = list(client.list_blobs(bucket_name, prefix=prefix))          
    if not any(b.name == prefix + SUCCESS for b in blobs):
        raise LandingNotReady(f"Chưa có gs://{bucket_name}/{prefix}{SUCCESS}")
    return [
        (f"gs://{bucket_name}/{b.name}", b.download_as_text(encoding="utf-8"))
        for b in sorted(blobs, key=lambda b: b.name)
        if b.name.endswith(".html")
    ]



