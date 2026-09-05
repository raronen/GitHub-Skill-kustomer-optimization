# CMHelpers functions

Functions in folder `CMHelpers`.

## `CmHelperShowAuditLogByClientActivityId`

- Folder: `CMHelpers`
- Parameters: `(clientActivityId:string, from:datetime=datetime(null), ['to']:datetime=datetime(null), cm:string="")`
- Docstring: No docstring provided.
- Usage example: `CmHelperShowAuditLogByClientActivityId('clientActivityId-value', datetime(2026-01-01), datetime(2026-01-01), 'cm-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmHelperShowAuditLogByClientActivityId(clientActivityId, from, ['to'], cm)
    )
 }
```

## `CmHelperShowClusterAuditLog`

- Folder: `CMHelpers`
- Parameters: `(cluster:string, from:datetime=datetime(null), ['to']:datetime=datetime(null), cm:string="")`
- Docstring: No docstring provided.
- Usage example: `CmHelperShowClusterAuditLog('cluster-value', datetime(2026-01-01), datetime(2026-01-01), 'cm-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmHelperShowClusterAuditLog(cluster, from, ['to'], cm)
    )
 }
```

## `CmHelperShowOperations`

- Folder: `CMHelpers`
- Parameters: `(cm:string="", operations:dynamic=dynamic([]), state:string="")`
- Docstring: No docstring provided.
- Usage example: `CmHelperShowOperations('cm-value', /* operations */, 'state-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmHelperShowOperations(cm, operations, state)
    )
 }
```

## `CmHelperShowServiceAuditLog`

- Folder: `CMHelpers`
- Parameters: `(service:string, from:datetime=datetime(null), ['to']:datetime=datetime(null), cm:string="")`
- Docstring: No docstring provided.
- Usage example: `CmHelperShowServiceAuditLog('service-value', datetime(2026-01-01), datetime(2026-01-01), 'cm-value') | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmHelperShowServiceAuditLog(service, from, ['to'], cm)
    )
 }
```

## `GetADXCMsOperations`

- Folder: `CMHelpers`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `GetADXCMsOperations() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetADXCMsOperations()
    )
 }
```

## `GetADXCMsServiceOperations`

- Folder: `CMHelpers`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `GetADXCMsServiceOperations() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetADXCMsServiceOperations()
    )
 }
```

## `GetAllCMsOperations`

- Folder: `CMHelpers`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `GetAllCMsOperations() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmOperations
    )
 }
```

## `GetAllCMsServiceOperations`

- Folder: `CMHelpers`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `GetAllCMsServiceOperations() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.CmServiceOperations
    )
 }
```

## `GetFabricCMsOperations`

- Folder: `CMHelpers`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `GetFabricCMsOperations() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetFabricCMsOperations()
    )
 }
```

## `GetFabricCMsServiceOperations`

- Folder: `CMHelpers`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `GetFabricCMsServiceOperations() | take 10`
- Notes: Simple cross-cluster wrapper/shortcut.

```kusto
{
     declare query_parameters(KuskusEntityGroup: string = "Kuskus");
     macro-expand best_effort=true hint.concurrency=64 entity_group(KuskusEntityGroup)
        as Kuskus (
        Kuskus.GetFabricCMsServiceOperations()
    )
 }
```

