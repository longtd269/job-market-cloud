# IAM của job-market-cloud

Nguyên tắc: pipeline chạy bằng sa-pipeline, không dùng file key.
Quyền cấp trên tài nguyên hẹp nhất, vào lúc tài nguyên được tạo.

| Principal              | Role                                 | Resource                                       | Lý do                           | Trạng thái |
| ---------------------- | ------------------------------------ | ---------------------------------------------- | -------------------------------- | ------------ |
| sa-pipeline            | roles/bigquery.jobUser               | project jmc-01                                 | Chạy query và load job         | Đã cấp    |
| user:<email của bạn> | roles/iam.serviceAccountTokenCreator | service account sa-pipeline                    | Impersonate khi dev trên laptop | Đã cấp    |
| sa-pipeline            | roles/storage.objectAdmin            | bucket jmc-01-lake                             | Ghi và ghi đè file ingest     | Đã cấp    |
| sa-pipeline            | roles/bigquery.dataEditor            | các dataset raw, staging, intermediate, marts | Load và dbt ghi bảng           | Dự kiến    |
| sa-pipeline            | roles/logging.logWriter              | project jmc-01                                 | VM ghi log lên Cloud Logging    | Dự kiến    |
