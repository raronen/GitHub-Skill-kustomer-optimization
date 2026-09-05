# MaterializedViews functions

Functions in folder `MaterializedViews`.

## `MaterializedViewByRaid`

- Folder: `MaterializedViews`
- Parameters: `(rootActivityId:string)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewByRaid('rootActivityId-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewByRaid(rootActivityId))
 }
```

## `MaterializedViewParseSampleExtentRebuild`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewParseSampleExtentRebuild(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewParseSampleExtentRebuild(startTime, endTime))
 }
```

## `MaterializedViewsAgeMetric`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsAgeMetric(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsAgeMetric(startTime, endTime))
 }
```

## `MaterializedViewsAlerts`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsAlerts(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsAlerts(startTime, endTime))
 }
```

## `MaterializedViewsArgMaxOptimization`

- Folder: `MaterializedViews`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsArgMaxOptimization() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsArgMaxOptimization())
 }
```

## `MaterializedViewsCompletionMetric`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsCompletionMetric(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsCompletionMetric(startTime, endTime))
 }
```

## `MaterializedViewsDurations`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsDurations(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsDurations(startTime, endTime))
 }
```

## `MaterializedViewsErrors`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime, source:string)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsErrors(datetime(2026-01-01), datetime(2026-01-01), 'source-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsErrors(startTime, endTime, source))
 }
```

## `MaterializedViewsMonitoring`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsMonitoring(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsMonitoring(startTime, endTime))
 }
```

## `MaterializedViewsParseStatus`

- Folder: `MaterializedViews`
- Parameters: `(start:datetime, end:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsParseStatus(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsParseStatus(['start'], end))
 }
```

## `MaterializedViewsRetainRemoveStats`

- Folder: `MaterializedViews`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsRetainRemoveStats() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsRetainRemoveStats())
 }
```

## `MaterializedViewsSoftDeletePartitions`

- Folder: `MaterializedViews`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsSoftDeletePartitions() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsSoftDeletePartitions())
 }
```

## `MaterializedViewsStatisticsCollector`

- Folder: `MaterializedViews`
- Parameters: `(fromTime:datetime, toTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsStatisticsCollector(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsStatisticsCollector(fromTime, toTime))
 }
```

## `MaterializedViewsTrigger`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsTrigger(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsTrigger(startTime, endTime))
 }
```

## `MaterializedViewsUnknownErrors`

- Folder: `MaterializedViews`
- Parameters: `(startTime:datetime, endTime:datetime)`
- Docstring: No docstring provided.
- Usage example: `MaterializedViewsUnknownErrors(datetime(2026-01-01), datetime(2026-01-01)) | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.MaterializedViewsUnknownErrors(startTime, endTime))
 }
```

