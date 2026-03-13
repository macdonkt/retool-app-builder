# Verified Pattern: Table with Static Data

**Source**: step2.json (verified import)
**Components**: Screen + Frame + TextWidget2 + TableWidget2
**Status**: PASS (after tlist fix)

## What This Tests
- TableWidget2 with inline static JSON data
- Column definitions using per-column property maps
- Transit List encoding for `_columnIds`, `_actionIds`, `_toolbarButtonIds`, `_groupByColumns`

## Critical Table Structure

TableWidget2 does NOT use a `columns` array. Instead it uses:
1. `_columnIds` — `tlist(["col1_id", "col2_id", ...])` — ordered list of column IDs
2. Per-property maps — one `tmap()` per property, keyed by column ID

### Column Property Maps (one per property, each is a `tmap()`)
```python
"_columnLabel":     tmap("col1", "ID", "col2", "Name", "col3", "Price"),
"_columnSizeType":  tmap("col1", "auto", "col2", "auto", "col3", "auto"),
"_columnFormat":    tmap("col1", "decimal", "col2", "string", "col3", "decimal"),
"_columnAlignment": tmap("col1", "right", "col2", "left", "col3", "right"),
# ... 30+ more property maps
```

### Required tlist() Fields
These MUST use `tlist()`, NOT plain arrays — otherwise: "t.get(...).toArray is not a function"
- `_columnIds`
- `_actionIds`
- `_toolbarButtonIds`
- `_groupByColumns`
- `events`

### Column ID Convention
Use short random-looking 5-char hex IDs (e.g., `"6b4dc"`, `"e3e2b"`, `"3f13a"`) — matches Retool's internal format.

## Plugin Structure (4 plugins)

### TableWidget2 Template (key fields only)
```python
tom(
    "data", '[{"id":1,"name":"Wireless Mouse","price":29.99}...]',
    "_columnIds", tlist(["col_id", "col_name", "col_price"]),
    "_columnLabel", tmap("col_id", "ID", "col_name", "Name", "col_price", "Price"),
    "_columnFormat", tmap("col_id", "decimal", "col_name", "string", "col_price", "decimal"),
    # ... all other _column* maps with defaults for each column ID
    "_actionIds", tlist([]),
    "_toolbarButtonIds", tlist(["filter", "sort", "download", "addRow", "refresh"]),
    "_groupByColumns", tlist([]),
    "events", tlist([]),
    # ... 100+ more fields — copy ALL from transit_patterns.json
)
```

## Gotchas
- TableWidget2 template has **100+ fields** — copy ALL from transit_patterns.json
- Every `_column*` property map must include an entry for EVERY column ID
- `data` is a string (JSON string or `{{ query.data }}` binding), not an object
- `selectedRowKey` is `null` by default
- Cell expressions use `currentSourceRow` (not `currentRow`)
