# Financials\Utilities functions

Functions in folder `Financials\Utilities`.

## `GetAccount`

- Folder: `Financials\Utilities`
- Parameters: `(Source:string)`
- Docstring: No docstring provided.
- Usage example: `GetAccount('Source-value') | take 10`
- Notes: Composed function with custom logic.

```kusto
{
     cluster('kustoproductfw.westus.kusto.windows.net').database("KustoBilling").GetAccount(Source)
 }
```

