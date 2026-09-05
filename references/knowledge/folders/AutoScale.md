# AutoScale functions

Functions in folder `AutoScale`.

## `GetLastAutoScaleQueryOfCM`

- Folder: `AutoScale`
- Parameters: `(jobName:string, source:string, start:timespan=time(1.00:00:00), end:timespan=time(00:00:00))`
- Docstring: Function for getting the query that the CM runs in a given lookback period
- Usage example: `GetLastAutoScaleQueryOfCM('jobName-value', 'source-value', 1d, 1d) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetLastAutoScaleQueryOfCM(jobName, source, start, end)
    )
    | order by start desc
 }
```

## `ReasonWeDoOrDontScaleCluster`

- Folder: `AutoScale`
- Parameters: `(clusterName:string, lookback:timespan, scaleOperationType:string, wasScaled:bool)`
- Docstring: Function for getting why we do (don't) scale in (out) cluster in a given lookback period
- Usage example: `ReasonWeDoOrDontScaleCluster('clusterName-value', 1d, 'scaleOperationType-value', true) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.ReasonWeDoOrDontScaleCluster(clusterName, lookback, scaleOperationType, wasScaled)
    )
 }
```

