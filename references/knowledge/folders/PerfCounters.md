# PerfCounters functions

Functions in folder `PerfCounters`.

## `PerfCounterCPU`

- Folder: `PerfCounters`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `PerfCounterCPU() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.PerfCounterCPU
    )
 }
```

## `PerfCounterDiskCQueue`

- Folder: `PerfCounters`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `PerfCounterDiskCQueue() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.PerfCounterDiskCQueue()
    )
 }
```

## `PerfCounterMemoryAvailable`

- Folder: `PerfCounters`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `PerfCounterMemoryAvailable() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.PerfCounterMemoryAvailable()
    )
 }
```

## `PerfCounterThreads`

- Folder: `PerfCounters`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `PerfCounterThreads() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.PerfCounterThreads()
    )
 }
```

## `PerfCounterTimeInGC`

- Folder: `PerfCounters`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `PerfCounterTimeInGC() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.PerfCounterTimeInGC()
    )
 }
```

