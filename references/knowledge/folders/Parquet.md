# Parquet functions

Functions in folder `Parquet`.

## `NativeParquetIngestionUsage`

- Folder: `Parquet`
- Parameters: `(from:datetime)`
- Docstring: No docstring provided.
- Usage example: `NativeParquetIngestionUsage(datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.NativeParquetIngestionUsage(from)
    )
    | summarize IngestionsCount = sum(IngestionsCount), ClusterCount = sum(ClusterCount) by Reason
    | project Reason, IngestionsCount, ClusterCount
    | as Results
    | extend NativeIngestionsPercentage = round(IngestionsCount * 100.0 / toscalar(Results | summarize sum(IngestionsCount)), 1)
    | order by IngestionsCount desc
 }
```

## `NativeParquetQueryUsage`

- Folder: `Parquet`
- Parameters: `(from:datetime)`
- Docstring: No docstring provided.
- Usage example: `NativeParquetQueryUsage(datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.NativeParquetQueryUsage(from)
    )
    | summarize QueryCount = sum(QueryCount), ClusterCount = sum(ClusterCount) by Reason
    | project Reason, QueryCount, ClusterCount
    | as Results
    | extend NativeQueriesPercentage = round(QueryCount * 100.0 / toscalar(Results | summarize sum(QueryCount)), 1)
    | order by QueryCount desc
 }
```

