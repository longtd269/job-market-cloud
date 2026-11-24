
# Data lake

- Bucket: gs://jmc-01-lake (us-central1, Standard)
- Bảo mật: uniform bucket-level access, public access prevention
- Soft delete: 7 ngày (mặc định)
- Lifecycle: xoá object trong raw/ sau 180 ngày (infra/lifecycle.json)

## Layout

raw/source=<nguồn>/ingest_date=YYYY-MM-DD/part-000.jsonl
raw/source=<nguồn>/ingest_date=YYYY-MM-DD/_SUCCESS

landing/source=<nguồn>/ingest_date=YYYY-MM-DD/*.html
landing/source=<nguồn>/ingest_date=YYYY-MM-DD/_SUCCESS

## Quy tắc

1. raw/ chỉ pipeline ghi, không ai sửa tay.
2. ingest_date là ngày thu thập, mỗi lần chạy tạo một partition.
3. Ghi lại một ngày: xoá _SUCCESS, xoá file cũ, ghi file mới, ghi _SUCCESS.
4. Bước load chỉ đọc partition có _SUCCESS.
