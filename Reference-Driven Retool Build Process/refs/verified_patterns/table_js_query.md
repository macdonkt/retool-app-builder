# Verified Pattern: Table Fed by JavaScript Query

**Source**: step3.json (verified import)
**Components**: Screen + Frame + TextWidget2 + JavascriptQuery + TableWidget2
**Status**: PASS

## What This Tests
- JavascriptQuery with `runWhenPageLoads=true`
- Table bound to query data via `{{ fetchItems.data }}`
- Data flow: query runs on load → table displays results

## JavascriptQuery Template (key fields)
```python
tom(
    "query", 'return [{id: 1, name: "Wireless Mouse", price: 29.99}, ...]',
    "runWhenPageLoads", True,
    "runWhenModelUpdates", False,
    "showSuccessToaster", False,
    "showFailureToaster", True,
    "queryTimeout", "10000",
    "queryThrottleTime", "750",
    "queryRefreshTime", "",
    "enableTransformer", False,
    "transformer", "// Query results are available as the `data` variable",
    "confirmMessage", "",
    "notificationDuration", "4.5",
    "enableCaching", False,
    "cacheDuration", "",
    "importedQueryInputs", tmap(),
    "events", tlist([]),
    # ... many more fields — copy ALL from transit_patterns.json
)
```

## Table Binding
The table's `data` field uses a binding to the query:
```python
"data", "{{ fetchItems.data }}"
```

## Query Plugin Structure
```python
query("fetchItems", "JavascriptQuery",
    tom(... all template fields ...),
    screen="page1")  # page-scoped
```

Note: `query()` helper auto-sets `resourceName="JavascriptQuery"` for JS queries.

## Key Fields for JavascriptQuery
From transit_patterns.json:
- `query` — the JavaScript code to execute (the `src` field in some contexts)
- `runWhenPageLoads` — `True` to auto-run
- `runWhenModelUpdates` — `False` usually (prevents infinite loops)
- `events` — `tlist([])` for no events, or `tlist([evt_trigger_query(...)])` for chaining
- `enableTransformer` — `False` unless you need post-processing
- `transformer` — JS code to transform query results

## Transit Encoding Notes
- Query templates use `tom()` (ordered map)
- Query plugins have `style=None` (not `tom()`)
- Query plugins have `position2=None`
- `importedQueryInputs` uses `tmap()` (plain map)

## Gotchas
- `queryTimeout` is a STRING: `"10000"` not `10000`
- `notificationDuration` is a STRING: `"4.5"` not `4.5`
- `queryThrottleTime` is a STRING: `"750"` not `750`
- JavascriptQuery field is `query`, not `src`
