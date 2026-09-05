# Financials\Views functions

Functions in folder `Financials\Views`.

## `FabricFinancials`

- Folder: `Financials\Views`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `FabricFinancials() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('kustoproductfw.westus.kusto.windows.net').database('KustoBilling').FabricFinancials
 }
```

## `KustoFinancials`

- Folder: `Financials\Views`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KustoFinancials() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('kustoproductfw.westus.kusto.windows.net').database('KustoBilling').KustoFinancials
 }
```

## `KustoFinancialsWithRegions`

- Folder: `Financials\Views`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KustoFinancialsWithRegions() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('kustoproductfw.westus.kusto.windows.net').database('KustoBilling').KustoFinancialsWithRegions
 }
```

## `KustoGrossMargin`

- Folder: `Financials\Views`
- Parameters: `()`
- Docstring: No docstring provided.
- Usage example: `KustoGrossMargin() | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('kustoproductfw.westus.kusto.windows.net').database('KustoBilling').GrossMargin
 }
```

