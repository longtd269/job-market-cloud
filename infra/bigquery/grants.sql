GRANT `roles/bigquery.dataEditor` ON SCHEMA `jmc-01.raw`
  TO "serviceAccount:sa-pipeline@jmc-01.iam.gserviceaccount.com";

GRANT `roles/bigquery.dataEditor` ON SCHEMA `jmc-01.staging`
  TO "serviceAccount:sa-pipeline@jmc-01.iam.gserviceaccount.com";

GRANT `roles/bigquery.dataEditor` ON SCHEMA `jmc-01.intermediate`
  TO "serviceAccount:sa-pipeline@jmc-01.iam.gserviceaccount.com";

GRANT `roles/bigquery.dataEditor` ON SCHEMA `jmc-01.marts`
  TO "serviceAccount:sa-pipeline@jmc-01.iam.gserviceaccount.com";