# V3Migration functions

Functions in folder `V3Migration`.

## `FindDMs`

- Folder: `V3Migration`
- Parameters: `(engine_name:string)`
- Docstring: Find all DMs of engine
- Usage example: `FindDMs('engine_name-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindDMs(engine_name)
    )
 }
```

## `V3MigrationProgress`

- Folder: `V3Migration`
- Parameters: `(migration:string, userfilter:string="any")`
- Docstring: Show progress of data migration
- Usage example: `V3MigrationProgress('migration-value', 'userfilter-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.V3MigrationProgress(migration, userfilter)
    )
    | order by progress desc
 }
```

