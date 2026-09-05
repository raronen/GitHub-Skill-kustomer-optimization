# Geospatial functions

Functions in folder `Geospatial`.

## `Geospatial_Clusters_Usage`

- Folder: `Geospatial`
- Parameters: `(from:datetime)`
- Docstring: No docstring provided.
- Usage example: `Geospatial_Clusters_Usage(datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Geospatial_Clusters_Usage(from)
    )
    | summarize sum(['count']) by Source
    | order by sum_count desc
 }
```

## `Geospatial_ClustersByAccount_Usage`

- Folder: `Geospatial`
- Parameters: `(from:datetime)`
- Docstring: No docstring provided.
- Usage example: `Geospatial_ClustersByAccount_Usage(datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
// ⚠️ NOT CORRECT: Geospatial_ClustersByAccount_Usage_Internal is an internal regional function — not available on kuskushead. This function body may be outdated or only resolvable on regional Kuskus instances.
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Geospatial_ClustersByAccount_Usage_Internal(from)
    )
    | summarize QueriesCount = sum(QueriesCount) by Source
    | join kind=leftouter
        (
        cluster('kustoproductfw.westus.kusto.windows.net').database('KustoBilling').KustoFinancials
        | project Cluster, Account, Day
        | where strlen(Cluster) > 0 and strlen(Account) > 0 and isnotnull(Day)
        | summarize arg_max(Day, Cluster, Account) by Cluster
        | project Source = toupper(Cluster), Account
        )
        on Source
    | project Account, Source, QueriesCount
    | summarize QueriesCount = sum(QueriesCount), make_set(Source) by Account
    | project
        Account,
        QueriesCount,
        ClustersCount = array_length(set_Source),
        Clusters = tostring(set_Source)
    | order by QueriesCount, ClustersCount desc
 }
```

## `Geospatial_Functions_Usage`

- Folder: `Geospatial`
- Parameters: `(from:datetime)`
- Docstring: No docstring provided.
- Usage example: `Geospatial_Functions_Usage(datetime(2026-01-01)) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Geospatial_Functions_Usage(from)
    )
    | summarize sum(['count']) by func_name
    | order by sum_count desc
 }
```

