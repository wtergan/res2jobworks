CREATE TABLE exports_next (
    id TEXT PRIMARY KEY,
    export_type TEXT NOT NULL,
    format TEXT NOT NULL CHECK (format IN ('markdown', 'csv', 'json', 'pdf', 'docx')),
    target_table TEXT NOT NULL,
    target_id TEXT NOT NULL,
    path TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    generated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

INSERT INTO exports_next(
    id,
    export_type,
    format,
    target_table,
    target_id,
    path,
    metadata_json,
    generated_at
)
SELECT
    id,
    export_type,
    format,
    target_table,
    target_id,
    path,
    metadata_json,
    generated_at
FROM exports;

DROP TABLE exports;

ALTER TABLE exports_next RENAME TO exports;
