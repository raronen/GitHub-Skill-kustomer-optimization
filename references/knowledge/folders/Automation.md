# Automation functions

Functions in folder `Automation`.

## `Automation_ClusterDiagnostics_Steps`

- Folder: `Automation`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `Automation_ClusterDiagnostics_Steps() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     datatable(Step: string, Description: string, Parameters: dynamic)
    [
    "HighQueryLatency", "Check query P90 latency anomalies", dynamic(null),
    "HighDiskQueue", "Check disk-queue length", dynamic(null),
    "HighCPU", "Check CPU of the machines", dynamic(null),
    "UnhealthyMachines", "Check machines health", dynamic(null),
    "HighGC", "Check GC of the machines", dynamic(null),
    "MachinesWithHighGC", "Check percentage of the machines with high GC", dynamic(null),
    "FindMachinesWithHighGC", "Find what machines had high GC", dynamic(null),
    "MachinesWithHighCPU", "Check percentage of the machines with high CPU", dynamic(null),
    "AnalyzeUsage", "Analyze what consumes cluster CPU", dynamic(null),
    "AdminCPU", "Analyze Admin\'s machines CPU", dynamic(null),
    "DrillIntoQueriesUsage", "Drill into query usage", dynamic(null),
    "DrillIntoCommandsUsage", "Drill into control-commands usage", dynamic(null),
    "RareFF", "Find rare feature-flags", dynamic(null),
    "CriticalTraces", "Check critical traces", dynamic(null),
    "OnOffMachines", "Checks restarting machines", dynamic(null),
    "CriticalAlerts", "Check critical alerts", dynamic(null),
    "HighQueryLatencyDetails", "Check query high concurency details", dynamic(null),
    "AdminStability", "Checks Admin\'s role stability", dynamic(null),
    "TopHeavyQueries", "The most heavy queries", dynamic(null),
    "AnalyzePerNodeUsage", "Analyze usage based on per-node traces", dynamic(null),
    "AdminGC", "Analyze Admin\'s GC profile", dynamic(null),
    ]
 }
```

## `Automation_ClusterDiagnostics_Transitions`

- Folder: `Automation`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `Automation_ClusterDiagnostics_Transitions() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     datatable(Step: string, NextStep: string)
    [
    "HighQueryLatency", "HighDiskQueue",
    "HighQueryLatency", "HighCPU",
    "HighQueryLatency", "UnhealthyMachines",
    "HighQueryLatency", "RareFF",
    "HighQueryLatency", "HighQueryLatencyDetails",
    "HighCPU", "MachinesWithHighCPU",
    "HighCPU", "HighGC",
    "UnhealthyMachines", "CriticalTraces",
    "HighGC", "MachinesWithHighGC",
    "MachinesWithHighGC", "FindMachinesWithHighGC",
    "MachinesWithHighCPU", "AnalyzeUsage",
    "MachinesWithHighCPU", "AdminCPU",
    "MachinesWithHighCPU", "AdminGC",
    "AnalyzeUsage", "DrillIntoQueriesUsage",
    "AnalyzeUsage", "DrillIntoCommandsUsage",
    "AnalyzeUsage", "AnalyzePerNodeUsage",
    "AdminCPU", "AdminStability",
    "DrillIntoQueriesUsage", "TopHeavyQueries",
    "CriticalTraces", "OnOffMachines",
    "CriticalTraces", "CriticalAlerts",
    "AdminStability", "AnalyzeUsage",
    ]
 }
```

