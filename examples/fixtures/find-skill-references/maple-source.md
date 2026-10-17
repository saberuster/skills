# Maple Batch primary-source snapshot

This is an original fictional fixture, not a real project or fetched source.
Locator: `https://example.invalid/maple-batch/blob/maple-v2/export.py`.
Snapshot: `maple-v2`. The snippets below are the complete relevant functions
and test assertions for this simulated source.

## Export implementation

Maple exports bounded batches that fit in memory. It validates every row and
builds the replacement before touching the previous destination. A real file
backend would need to implement the replacement operation atomically.

```python
def export_rows(rows, columns, store):
    batch = list(rows)
    for row in batch:
        if any(column not in row for column in columns):
            raise ValueError("Missing selected column")
    replacement = [list(columns)]
    replacement.extend([[row[column] for column in columns] for row in batch])
    store.replace_atomically(replacement)
```

## Tests and limits

The snapshot's tests assert that a missing column in the final row leaves the
old destination unchanged. They also assert that `columns=["name", "id"]`
produces that header and the corresponding value order, even when dictionary
insertion order differs. These are source assertions; they have not been run
in this research trial.

This implementation does not support unbounded event streams or CSV escaping.
It supplies a validation and publication pattern, not a complete CSV writer.
