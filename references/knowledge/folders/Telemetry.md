# Telemetry functions

Functions in folder `Telemetry`.

## `ClusterDataCapacity`

- Folder: `Telemetry`
- Parameters: `()`
- Docstring: Data capacity snapshots
- Usage example: `ClusterDataCapacity() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDataCapacity
    )
 }
```

