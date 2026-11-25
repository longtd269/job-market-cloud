
# BigQuery

- Dataset: raw, staging, intermediate, marts, lab (us-central1), tạo bằng infra/bigquery/datasets.sql
- Quyền: sa-pipeline có dataEditor trên 4 dataset pipeline (infra/bigquery/grants.sql)
- Hàng rào: ~/.bigqueryrc maximum_bytes_billed = 1 GB; bảng thật luôn partition theo ngày + require_partition_filter

## Kết quả phòng lab (ngày 2026-11-25)

Bảng jobs_flat: 2,000,000 dòng, 532.66 MB

| Query | Mô tả                       | Ước tính | Bytes billed | Ghi chú                                                                                                                                               |
| ----- | ----------------------------- | ----------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Q1    | Phẳng, 1 ngày               | 40.44 MB    | 41 MB        |                                                                                                                                                        |
| Q2    | Partition, 1 ngày            | 414.06 KB   | 10 MB        |                                                                                                                                                        |
| Q3    | Chạy lại Q2                 | 414.06 KB   | 0 B          | (results cached)                                                                                                                                       |
| Q4    | Quên lọc ngày              |             |              | Báo lỗi<br />Cannot query over table 'jmc-01.lab.jobs_part' without a filter over column(s) 'ingest_date' that can be used for partition elimination |
| Q5    | CAST cột partition           | 414.06 KB   | 10 MB        |                                                                                                                                                        |
| Q6    | SELECT * LIMIT 10             | 5.33 MB     | 10 MB        |                                                                                                                                                        |
| Q7    | Tháng + city, không cluster | 21.18 MB    | 22 MB        |                                                                                                                                                        |
| Q8    | Tháng + city, có cluster    | 21.18 MB    | 21 MB        |                                                                                                                                                        |

## Rút ra

Có partition thì query sẽ tốn ít bytes billed hơn
Nếu được cached thì sẽ không tốn bytes billed
Hãy để require partition để gom nhóm tránh query quá nhiều



## Thiết kế bảng

raw.jobs (DAY + require filter)

fct (DAY hay MONTH, cluster city/category)
