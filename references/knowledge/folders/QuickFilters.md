# QuickFilters functions

Functions in folder `QuickFilters`.

## `FindCIDPast1w`

- Folder: `QuickFilters`
- Parameters: `(clientActivityId:string)`
- Docstring: No docstring provided.
- Usage example: `FindCIDPast1w('clientActivityId-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindCIDPast1w(clientActivityId)
    )
 }
```

## `FindCIDPast24h`

- Folder: `QuickFilters`
- Parameters: `(clientActivityId:string)`
- Docstring: No docstring provided.
- Usage example: `FindCIDPast24h('clientActivityId-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindCIDPast24h(clientActivityId)
    )
 }
```

## `FindQueryEssentials`

- Folder: `QuickFilters`
- Parameters: `(rootActivityId:string)`
- Docstring: No docstring provided.
- Usage example: `FindQueryEssentials('rootActivityId-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindQueryEssentials(rootActivityId)
    )
 }
```

## `FindRIDPast1w`

- Folder: `QuickFilters`
- Parameters: `(rid:string)`
- Docstring: No docstring provided.
- Usage example: `FindRIDPast1w('rid-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindRIDPast1w(rid)
    )
 }
```

## `FindRIDPast24h`

- Folder: `QuickFilters`
- Parameters: `(rid:string)`
- Docstring: No docstring provided.
- Usage example: `FindRIDPast24h('rid-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.FindRIDPast24h(rid)
    )
 }
```

