CREATE SCHEMA IF NOT EXISTS `jmc-01.raw`
  OPTIONS (location = 'us-central1', description = 'Bản sao dữ liệu từ lake. Chỉ job load ghi.');

CREATE SCHEMA IF NOT EXISTS `jmc-01.staging`
  OPTIONS (location = 'us-central1', description = 'dbt: đổi tên, ép kiểu, khử trùng.');

CREATE SCHEMA IF NOT EXISTS `jmc-01.intermediate`
  OPTIONS (location = 'us-central1', description = 'dbt: logic trung gian.');

CREATE SCHEMA IF NOT EXISTS `jmc-01.marts`
  OPTIONS (location = 'us-central1', description = 'dbt: bảng cho dashboard.');

CREATE SCHEMA IF NOT EXISTS `jmc-01.lab`
  OPTIONS (location = 'us-central1', description = 'Lab. Bảng tự xoá sau 7 ngày.',
           default_table_expiration_days = 7);
