# CMHelpersReporting functions

Functions in folder `CMHelpersReporting`.

## `CmServiceOperationsFailures`

- Folder: `CMHelpersReporting`
- Parameters: `(startTime:datetime, timePeriod:timespan)`
- Docstring: No docstring provided.
- Usage example: `CmServiceOperationsFailures(datetime(2026-01-01), 1d) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmServiceOperations
        | where StartTime between(startTime .. timePeriod)
        | where State in ("PartiallySucceeded", "Failed")
        | where StateDetails !startswith "Insufficient resources of type 'Cores'" and StateDetails !has "restricted due to enforced user limitations"
        | project-rename Cluster=Source
    )
 }
```

## `CmServiceOperationsRolledUpSLA`

- Folder: `CMHelpersReporting`
- Parameters: `(BeginTime:datetime, TimePeriod:timespan)`
- Docstring: No docstring provided.
- Usage example: `CmServiceOperationsRolledUpSLA(datetime(2026-01-01), 1d) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     CmServiceOperationsSLA(BeginTime, TimePeriod)
    | summarize Total = sum(Total), Failed = sum(Failed) by OperationKind
    | extend SLA= (1 - (Failed / todouble(Total))) * 100
    | extend StartTime = BeginTime, EndTime = BeginTime + TimePeriod
    | sort by SLA asc
 }
```

## `CmServiceOperationsSLA`

- Folder: `CMHelpersReporting`
- Parameters: `(BeginTime:datetime, TimePeriod:timespan)`
- Docstring: No docstring provided.
- Usage example: `CmServiceOperationsSLA(datetime(2026-01-01), 1d) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmServiceOperations
        | where StartTime between (BeginTime .. TimePeriod)
        | where State !in ("InProgress", "Scheduled")
        | summarize arg_max(StartTime + Duration, *) by OperationId, ServiceName, Source
        | extend State = iif(OperationKind == "ServiceConfigurationAlter" and State == "PartiallySucceeded", "Completed", State) // ignore restriction on instances count and insufficient resources
        | summarize
            Total=count(),
            Failed=countif(State in ("Failed", "PartiallySucceeded")),
            percentiles(Duration, 50, 90, 95)
            by OperationKind, Source
        | extend SLA= (1 - (Failed / todouble(Total))) * 100
        | project-rename Cluster=Source
    )
    | extend StartTime = BeginTime, EndTime = BeginTime + TimePeriod
    | sort by SLA asc
 }
```

## `CmServiceOperationsSLAOverTime`

- Folder: `CMHelpersReporting`
- Parameters: `(NumOperations:int=10)`
- Docstring: No docstring provided.
- Usage example: `CmServiceOperationsSLAOverTime(1) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let TimePeriod = 7d;
     let data = materialize(
        union
            (CmServiceOperationsSLA(startofweek(ago(56d)), TimePeriod)),
            (CmServiceOperationsSLA(startofweek(ago(49d)), TimePeriod)),
            (CmServiceOperationsSLA(startofweek(ago(42d)), TimePeriod)),
            (CmServiceOperationsSLA(startofweek(ago(35d)), TimePeriod)),
            (CmServiceOperationsSLA(startofweek(ago(28d)), TimePeriod)),
            (CmServiceOperationsSLA(startofweek(ago(21d)), TimePeriod)),
            (CmServiceOperationsSLA(startofweek(ago(14d)), TimePeriod)),
            (CmServiceOperationsSLA(startofweek(ago(7d)), TimePeriod))
        | extend StartWeek = format_datetime(StartTime, 'yyyyMM/dd/yyyy')
        | summarize Total=sum(Total), Failed=sum(Failed), P95=min(percentile_Duration_95) by StartWeek, OperationKind);
     let topOperations = dynamic(["ClusterCreateExternal", "ClusterDelete", "ClusterSuspend", "ClusterResume", "DatabaseCreate", "DatabaseDelete", "ServiceInstall", "ServiceRestart", "ServiceConfigurationAlter"]);
     data
    | where OperationKind in (topOperations)
    | project
        StartWeek,
        OperationKind,
        Total,
        Failed,
        SLA=1.0 - (todouble(Failed) / Total),
        P95=(P95 / 1ms)
 }
```

## `CmServiceOperationsWoWSLA`

- Folder: `CMHelpersReporting`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `CmServiceOperationsWoWSLA() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     let TimePeriod = 7d;
     union
        (CmServiceOperationsSLA(startofweek(ago(28d)), TimePeriod)),
        (CmServiceOperationsSLA(startofweek(ago(21d)), TimePeriod)),
        (CmServiceOperationsSLA(startofweek(ago(14d)), TimePeriod)),
        (CmServiceOperationsSLA(startofweek(ago(7d)), TimePeriod))
    | where Total >= 100
    | extend StartWeek = format_datetime(StartTime, 'MM/dd/yyyy')
    | project StartWeek, OperationKind, SLA
    | evaluate pivot(StartWeek, sum(SLA), OperationKind)
 }
```

