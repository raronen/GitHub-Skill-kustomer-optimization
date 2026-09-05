# Trident functions

Functions in folder `Trident`.

## `GetTridentHosters`

- Folder: `Trident`
- Parameters: `(HosterKind:string)`
- Docstring: No docstring provided.
- Usage example: `GetTridentHosters('HosterKind-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetTridentHosters(HosterKind)
    )
    | order by Source asc;
 }
```

## `TridentDimClusters`

- Folder: `Trident`
- Parameters: `(excludePreprovisioned:bool)`
- Docstring: No docstring provided.
- Usage example: `TridentDimClusters(true) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TridentDimClusters(excludePreprovisioned)
    )
 }
```

## `TridentTestTenants`

- Folder: `Trident`
- Parameters: `()`
- Docstring: Known Trident test tenants
- Usage example: `TridentTestTenants() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TridentTestTenants
    )
    | distinct *
 }
```

## `TridentUsageDaily`

- Folder: `Trident`
- Parameters: `(StartTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `TridentUsageDaily(datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TridentUsageDaily(StartTime)
    )
    | summarize
        Domain=take_anyif(Domain, isnotempty(Domain)),
        UsersHll=hll_merge(UsersHll),
        Users=dcount_hll(hll_merge(UsersHll)),
        ActiveClusters=sum(ActiveClusters),
        Usage=sum(Usage)
        by TridentEnvironment, Timestamp, Api, TenantId, PrincipalType
 }
```

