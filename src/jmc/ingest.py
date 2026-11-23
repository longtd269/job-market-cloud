"""Job ingest: HTML trong landing -> JSONL trong raw.

Cách chạy:  python -m jmc.ingest --date 2026-11-20
Mã thoát:   0 thành công · 1 lỗi · 2 landing chưa sẵn sàng"""

import argparse
import json
import logging
import sys
from datetime import date, datetime, timezone
import pandas as pd
from google.cloud import storage

from jmc import config
from jmc.lake import LandingNotReady, raw_prefix, read_landing_pages, replace_prefix
from jmc.topcv_parser import parse_list_page

logger = logging.getLogger(__name__)
def build_records(pages: list[tuple[str, str]], ingest_date: date) -> list[dict]:
    """Parse các trang HTML thành record, bỏ tin trùng theo job_url, gắn metadata."""
    ingested_at = datetime.now(timezone.utc).isoformat()
    seen: set[str] = set()
    records: list[dict] = []
    for source_file, html in pages:
        df = parse_list_page(html, ingest_date)
        logger.info("%s: %d tin", source_file, len(df))
        for row in df.to_dict("records"):
            job_url = str(row["link_description"]).split("?")[0]
            if job_url in seen:
                continue
            seen.add(job_url)
            record = {k: (None if pd.isna(v) else v) for k, v in row.items()}
            record.update(job_url=job_url, _source_file=source_file, _ingested_at=ingested_at)
            records.append(record)
    return records

def to_jsonl(records: list[dict]) -> str:
    return "".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in records)

def run(ingest_date: date) -> int:
    client = storage.Client(project=config.GCP_PROJECT)
    pages = read_landing_pages(client, config.LAKE_BUCKET, config.SOURCE, ingest_date)
    records = build_records(pages, ingest_date)
    if not records:
        raise ValueError("Landing có file nhưng parse ra 0 tin: kiểm tra lại HTML hoặc giao diện page")
    prefix = raw_prefix(config.SOURCE, ingest_date)
    replace_prefix(
        client, config.LAKE_BUCKET, prefix,
        {"part-000.jsonl": (to_jsonl(records), "application/x-ndjson")},
    )
    logger.info("Đã ghi %d tin vào gs://%s/%s", len(records), config.LAKE_BUCKET, prefix)
    return len(records)

def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Landing HTML -> raw JSONL")
    parser.add_argument("--date", type=date.fromisoformat, required=True, help="Ngày dữ liệu, YYYY-MM-DD")
    args = parser.parse_args(argv)
    try:
        run(args.date)
    except LandingNotReady as exc:
        logger.error("%s", exc)
        return 2
    except Exception:
        logger.exception("Ingest thất bại")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
    