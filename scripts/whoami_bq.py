"""In ra danh tính đang chạy query BigQuery (DE-201)."""
from google.cloud import bigquery

PROJECT_ID = "jmc-01"


def main() -> None:
    # Không truyền credential: thư viện tự tìm ADC
    client = bigquery.Client(project=PROJECT_ID, location="us-central1")
    job = client.query("SELECT SESSION_USER() AS who, CURRENT_TIMESTAMP() AS run_at")
    row = next(iter(job.result()))
    print(f"Query chạy bởi : {row.who}")
    print(f"Thời điểm     : {row.run_at}")
    print(f"Job ID        : {job.job_id}")
    print(f"Bytes billed  : {job.total_bytes_billed}")


if __name__ == "__main__":
    main()