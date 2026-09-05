# Shortcuts functions

Functions in folder `Shortcuts`.

## `Admins`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `Admins() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Admins
    )
 }
```

## `Alerts`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `Alerts() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Alerts
    )
 }
```

## `CmOperations`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `CmOperations() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmOperations
    )
 }
```

## `CmOperationsResults`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `CmOperationsResults() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmOperationsResults
    )
 }
```

## `CmServiceOperations`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `CmServiceOperations() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmServiceOperations
    )
 }
```

## `CmUsage`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `CmUsage() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmUsage
    )
 }
```

## `CommandCompletion`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `CommandCompletion() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CommandCompletion
    )
 }
```

## `CriticalTraces`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `CriticalTraces() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CriticalTraces
    )
 }
```

## `DataCapacityHistoryMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataCapacityHistoryMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataCapacityHistoryMv
    )
 }
```

## `DataIngest`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataIngest() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataIngest
    )
 }
```

## `DataIngestHistoryMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataIngestHistoryMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataIngestHistoryMv
    )
 }
```

## `DataOperations`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataOperations() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataOperations
     )
 }
```

## `DataOperationsHistoryMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DataOperationsHistoryMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DataOperationsHistoryMv
    )
 }
```

## `Deployments`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `Deployments() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Deployments
    )
 }
```

## `DiagnosticsResults`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DiagnosticsResults() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DiagnosticsResults
    )
 }
```

## `DimClusters`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DimClusters() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DimClusters
    )
 }
```

## `DimClustersDailyMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DimClustersDailyMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DimClustersDailyMv
    )
 }
```

## `DimClustersMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DimClustersMv() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let EUS2Regions = datatable(Region: string)
[
    "East US 2", "West US", "South Central US", "West US 3", 
    "Southwest US" 
];
     let SEASRegions = datatable(Region: string)
[
    "Southeast Asia"
];
     let movedRegions = EUS2Regions | union SEASRegions;
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DimClustersMv
        | where (Region in (EUS2Regions) and Kuskus.$current_cluster_endpoint contains 'EUS2') 
            or (Region in (SEASRegions) and Kuskus.$current_cluster_endpoint contains 'SEAS') 
            or not(Region in (movedRegions))
    )
 }
```

## `DmMemento`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DmMemento() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.
- ⚠️ **Do NOT restrict queries to the last 28 days.** Changes (policies, tables, functions, etc.) can have been applied years ago. Memento contains data going back to **2023**.
- Always look for the **latest change** to the same policy or object (table, function, etc.) — use `arg_max(Timestamp, *)` or `top 1 by Timestamp desc` grouped by the object identifier to find the most recent state.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DmMemento
    )
 }
```

## `DmPurgeCommands`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DmPurgeCommands() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DmPurgeCommands
    )
 }
```

## `DmSettings`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DmSettings() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DmSettings
    )
 }
```

## `DmSettingsMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DmSettingsMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DmSettingsMv
    )
}
```

## `DmUsage`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `DmUsage() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.DmUsage
    )
 }
```

## `KubernetesContainersStdoutLogs`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KubernetesContainersStdoutLogs() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KubernetesContainersStdoutLogs
    )
 }
```

## `KubernetesEvents`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KubernetesEvents() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KubernetesEvents
    )
 }
```

## `KuiperFlights`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KuiperFlights() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KuiperFlights
    )
 }
```

## `KuiperMetrics`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KuiperMetrics() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KuiperMetrics
    )
 }
```

## `KuiperTelemetry`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KuiperTelemetry() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KuiperTelemetry
    )
 }
```

## `KustoLogs`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KustoLogs() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KustoLogs
    )
 }
```

## `KustoMdmMetricsV1`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KustoMdmMetricsV1() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KustoMdmMetricsV1
    )
 }
```

## `KustoWorkloadLogs`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KustoWorkloadLogs() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.KustoWorkloadLogs
    )
 }
```

## `LegacyMetadataContainersDeletions`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `LegacyMetadataContainersDeletions() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.LegacyMetadataContainersDeletions
    )
 }
```

## `MaHeartBeats`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: MaHeartBeats
- Usage example: `MaHeartBeats() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaHeartBeats
    )
 }
```

## `Memento`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `Memento() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.
- ⚠️ **Do NOT restrict queries to the last 28 days.** Changes (policies, tables, functions, etc.) can have been applied years ago. Memento contains data going back to **2023**.
- Always look for the **latest change** to the same policy or object (table, function, etc.) — use `arg_max(Timestamp, *)` or `top 1 by Timestamp desc` grouped by the object identifier to find the most recent state.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Memento
    )
 }
```

## `MetadataContainersDeletion`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `MetadataContainersDeletion() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MetadataContainersDeletion
    )
 }
```

## `OverallQueryStats`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `OverallQueryStats() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.OverallQueryStats
    )
 }
```

## `PerfCounterEvent`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `PerfCounterEvent() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.PerfCounterEvent
    )
 }
```

## `QueryCompletion`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `QueryCompletion() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.QueryCompletion
    )
 }
```

## `SqlMonitoringAttachMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `SqlMonitoringAttachMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.SqlMonitoringAttachMv()
    )
 }
```

## `TraceTelemetry`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `TraceTelemetry() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TraceTelemetry
    )
 }
```

## `TraceTelemetryResults`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: TraceTelemetryResults
- Usage example: `TraceTelemetryResults() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.TraceTelemetryResults
    )
 }
```

## `Usage`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `Usage() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.Usage
    )
 }
```

## `UsageDailyMv`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `UsageDailyMv() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.UsageDailyMv
    )
 }
```

## `WebJobsLogs`

- Folder: `Shortcuts`
- Parameters: `()`
- Docstring: Temporary shortcut to WebJobLogs in kuskusdfv3
- Usage example: `WebJobsLogs() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('kuskusdfv3.kusto.windows.net').database('Kuskus').WebJobsLogs
 }
```

