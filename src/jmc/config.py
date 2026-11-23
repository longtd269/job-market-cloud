import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

GCP_PROJECT = os.environ["GCP_PROJECT"]
LAKE_BUCKET = os.environ["LAKE_BUCKET"]
SOURCE = "topcv"

