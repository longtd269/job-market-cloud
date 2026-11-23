"""Đưa các trang đã lưu trên laptop lên landing zone (chạy tay mỗi ngày).

Cách chạy:  python -m jmc.drop --date 2026-11-20 --dir ../job-market-etl/data/raw/html/2026-11-20
"""
import argparse
import logging
import sys
from datetime import date
from pathlib import Path

from google.cloud import storage

from jmc import config
from jmc.lake import landing_prefix, replace_prefix

logger = logging.getLogger(__name__)

def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Upload file from local -> landing zone")
    parser.add_argument("--date", type=date.fromisoformat, required=True)
    parser.add_argument("--dir", type=Path,required=True, help="Folder contain files .html by date" )

    args = parser.parse_args(argv)

    files = {
        path.name: (path.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        for path in sorted(args.dir.glob("*.html"))
    }

    if not files:
        logger.error("Không có file .html nào trong %s", args.dir)
        return 2

    prefix = landing_prefix(config.SOURCE, args.date)
    replace_prefix(storage.Client(project=config.GCP_PROJECT), config.LAKE_BUCKET, prefix, files)
    logger.info("Đã đưa %d trang lên gs://%s/%s", len(files), config.LAKE_BUCKET, prefix)
    return 0

if __name__ == "__main__":
    sys.exit(main())

