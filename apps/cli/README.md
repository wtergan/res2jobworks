# CLI App

Thin command-line client for `res2jobworks`.

The CLI owns argument parsing and presentation only. Product behavior runs
through `res2jobworks_core.commands` and returns `CommandEnvelope` JSON with
`--json`.

Use direct commands for humans:

```bash
res2jobworks --json jobs.evaluate --database-path workspace.sqlite3 --profile-id profile-jordan-avery --job-id job-product-operations-analyst
```

Use the registry runner for generated wrappers and automation:

```bash
res2jobworks run jobs.evaluate --json --input database_path=workspace.sqlite3 --input profile_id=profile-jordan-avery --input job_id=job-product-operations-analyst
```
