# DM functions

Functions in folder `DM`.

## `GetServiceUrls`

- Folder: `DM`
- Parameters: `(service:string)`
- Docstring: Jarvis, ICM and service urls
- Usage example: `GetServiceUrls('service-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetServiceUrls(service)
    )
 }
```

