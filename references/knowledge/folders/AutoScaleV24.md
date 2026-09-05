# AutoScaleV24 functions

Functions in folder `AutoScaleV24`.

## `GetLastAutoScaleQueryOfCMV24`

- Folder: `AutoScaleV24`
- Parameters: `(jobName:string, source:string, start:timespan=timespan(1d), end:timespan=timespan(0h))`
- Docstring: Function for getting the query that the CM runs in a given lookback period
- Usage example: `GetLastAutoScaleQueryOfCMV24('jobName-value', 'source-value', 1d, 1d) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
KustoLogs
| where Timestamp between (ago(start).. ago(end))
| where Source =~ source
| parse-where EventText with "ExecuteAutoScaleQueryByBatch: AutoScale will run " JobName " :" * "];" Query
| where JobName =~ jobName
| project Source, Timestamp, JobName, Query
| summarize arg_max(Timestamp, *);
}
```

## `ReasonWeDoOrDontScaleClusterV24`

- Folder: `AutoScaleV24`
- Parameters: `(clusterName:string, lookback:timespan=time(7.00:00:00), scaleOperationType:string="scalein", wasScaled:bool=false)`
- Docstring: Function for getting why we do (don't) scale in (out) cluster in a given lookback period
- Usage example: `ReasonWeDoOrDontScaleClusterV24('clusterName-value', 1d, 'scaleOperationType-value', true) | take 10`
- Notes: Composed function with custom logic.

```kusto
{
    let IsScalingOrNot = iff(wasScaled, "is scaling", "is not scaling");
    let AutoScaleJob = iff(scaleOperationType hassuffix "out", "EngineScaleOutJob ", "EngineScaleInJob ");
    KustoLogs
     | where Timestamp > ago(lookback)
     | where Source startswith "MANAGE-"
     | where Directory startswith "AutoScale"
     | where EventText has strcat(AutoScaleJob, IsScalingOrNot) and EventText has clusterName
}
```

