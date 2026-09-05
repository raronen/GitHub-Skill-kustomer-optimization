# Automation/ClusterDiagnostics functions

Functions in folder `Automation/ClusterDiagnostics`.

## `ClusterDiagnostics`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(cluster:string, since:datetime=datetime(null), period:timespan=time(1.00:00:00))`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics('cluster-value', datetime(2026-01-01), 1d) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let _startTime = coalesce(since, ago(1d));
     let _endTime = _startTime + period;
     print strcat('#automate ClusterDiagnostics(_cluster="', toupper(cluster), '",_startTime=datetime(', _startTime, '),_endDate=datetime(', _endTime, '))')
 }
```

## `ClusterDiagnostics_AdminCPU_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AdminCPU_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_AdminCPU_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Admin CPU", legend=hidden)
 }
```

## `ClusterDiagnostics_AdminCPU_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AdminCPU_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Admin CPU",
        NextActions = dynamic(['AdminStability']),
        state=state
 }
```

## `ClusterDiagnostics_AdminGC_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AdminGC_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_AdminGC_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Admin GC", legend=hidden)
 }
```

## `ClusterDiagnostics_AdminGC_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AdminGC_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print Description = "Admins with high GC", NextActions = dynamic([]), state=state
 }
```

## `ClusterDiagnostics_AdminStability_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AdminStability_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_AdminStability_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Admin Changes over time", legend=hidden)
 }
```

## `ClusterDiagnostics_AdminStability_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AdminStability_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_AdminStability_NextSteps(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_AnalyzePerNodeUsage_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AnalyzePerNodeUsage_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_AnalyzePerNodeUsage_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_AnalyzePerNodeUsage_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AnalyzePerNodeUsage_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Top CPU consumers by Activity Type",
        NextActions = dynamic(['TopHeavyActivities']),
        state=state
 }
```

## `ClusterDiagnostics_AnalyzeUsage_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AnalyzeUsage_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_AnalyzeUsage_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_AnalyzeUsage_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_AnalyzeUsage_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_AnalyzeUsage_NextSteps(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_CriticalAlerts_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_CriticalAlerts_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_CriticalAlerts_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_CriticalAlerts_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_CriticalAlerts_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print Description = "Critical alerts", NextActions = dynamic([]), state=state
 }
```

## `ClusterDiagnostics_CriticalTraces_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_CriticalTraces_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_CriticalTraces_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Machines with critical traces", legend=hidden)
 }
```

## `ClusterDiagnostics_CriticalTraces_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_CriticalTraces_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_CriticalTraces_NextSteps(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_DrillIntoCommandsUsage_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_DrillIntoCommandsUsage_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_DrillIntoCommandsUsage_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_DrillIntoCommandsUsage_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_DrillIntoCommandsUsage_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Top CPU consumers - Control Commands",
        NextActions = dynamic([]),
        state=state
 }
```

## `ClusterDiagnostics_DrillIntoQueriesUsage_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_DrillIntoQueriesUsage_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_DrillIntoQueriesUsage_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_DrillIntoQueriesUsage_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_DrillIntoQueriesUsage_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Top CPU consumers - Queries",
        NextActions = dynamic(['TopHeavyQueries']),
        state=state
 }
```

## `ClusterDiagnostics_FindMachinesWithHighGC_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_FindMachinesWithHighGC_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_FindMachinesWithHighGC_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Top-5 machines with High GC Over time")
 }
```

## `ClusterDiagnostics_FindMachinesWithHighGC_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_FindMachinesWithHighGC_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print Description = "Machines with high GC", NextActions = dynamic([]), state=state
 }
```

## `ClusterDiagnostics_HighCPU_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighCPU_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighCPU_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Max/Average CPU over time", legend=hidden)
 }
```

## `ClusterDiagnostics_HighCPU_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: Returns single row: with NextActions (dynamic array of actios), state (dynamic context)
- Usage example: `ClusterDiagnostics_HighCPU_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighCPU_NextSteps(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_HighDiskQueue_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighDiskQueue_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighDiskQueue_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="High DiskQueue Length", ysplit=panels, legend=hidden)
 }
```

## `ClusterDiagnostics_HighDiskQueue_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighDiskQueue_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print Description = "Done", NextActions = dynamic([]), state=state
 }
```

## `ClusterDiagnostics_HighGC_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighGC_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighGC_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Time spent in GC over time", legend=hidden)
 }
```

## `ClusterDiagnostics_HighGC_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighGC_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighGC_NextSteps(_cluster, _startTime, _endTime, state)
    )
    | render table
 }
```

## `ClusterDiagnostics_HighQueryLatency_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighQueryLatency_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighQueryLatency_GetData(_cluster, _startTime, _endTime, state)
    )
    | render anomalychart with (anomalycolumns=anomalies, title="Query duration anomalies", legend=hidden)
 }
```

## `ClusterDiagnostics_HighQueryLatency_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighQueryLatency_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighQueryLatency_NextSteps(_cluster, _startTime, _endTime, state)
    )
    | render table
 }
```

## `ClusterDiagnostics_HighQueryLatencyDetails_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighQueryLatencyDetails_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_HighQueryLatencyDetails_GetData(_cluster, _startTime, _endTime, state)
    )
    | render table
 }
```

## `ClusterDiagnostics_HighQueryLatencyDetails_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_HighQueryLatencyDetails_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Top High Query Latency events",
        NextActions = dynamic([]),
        state=state
 }
```

## `ClusterDiagnostics_MachinesWithHighCPU_Base`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_MachinesWithHighCPU_Base('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_MachinesWithHighCPU_Base(_cluster, _startTime, _endTime, state)
    )
    | render table
 }
```

## `ClusterDiagnostics_MachinesWithHighCPU_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_MachinesWithHighCPU_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_MachinesWithHighCPU_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Percentage of machines with HighCPU over time", legend=hidden)
 }
```

## `ClusterDiagnostics_MachinesWithHighCPU_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_MachinesWithHighCPU_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_MachinesWithHighCPU_NextSteps(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_MachinesWithHighGC_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_MachinesWithHighGC_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_MachinesWithHighGC_GetData(_cluster, _startTime, _endTime, state)
    )
    | render timechart with (title="Percentage of machines with High GC over time", legend=hidden)
 }
```

## `ClusterDiagnostics_MachinesWithHighGC_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_MachinesWithHighGC_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_MachinesWithHighGC_NextSteps(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_OnOffMachines_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_OnOffMachines_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_OnOffMachines_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_OnOffMachines_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_OnOffMachines_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print Description = "Restarting machines", NextActions = dynamic([]), state=state
 }
```

## `ClusterDiagnostics_RareFF_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_RareFF_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_RareFF_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_RareFF_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_RareFF_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print Description = "Rare feature flags", NextActions = dynamic([]), state=state
 }
```

## `ClusterDiagnostics_SubqueryDelayed_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_SubqueryDelayed_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_SubqueryDelayed_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_SubqueryDelayed_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_SubqueryDelayed_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Machines with delayed subqueries",
        NextActions = dynamic([]),
        state=state
 }
```

## `ClusterDiagnostics_TopHeavyQueries_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_TopHeavyQueries_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_TopHeavyQueries_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_TopHeavyQueries_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_TopHeavyQueries_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Top CPU consuming Queries",
        NextActions = dynamic([]),
        state=state
 }
```

## `ClusterDiagnostics_UnhealthyMachines_GetData`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_UnhealthyMachines_GetData('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ClusterDiagnostics_UnhealthyMachines_GetData(_cluster, _startTime, _endTime, state)
    )
 }
```

## `ClusterDiagnostics_UnhealthyMachines_NextSteps`

- Folder: `Automation/ClusterDiagnostics`
- Parameters: `(_cluster:string, _startTime:datetime, _endTime:datetime, state:dynamic)`
- Docstring: No docstring provided.
- Usage example: `ClusterDiagnostics_UnhealthyMachines_NextSteps('_cluster-value', datetime(2026-01-01), datetime(2026-01-01), /* state */) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     print
        Description = "Unhealthy machines",
        NextActions = dynamic(['CriticalTraces']),
        state=state
 }
```

