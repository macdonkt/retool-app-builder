# Verified Pattern: Basic Text Widget

**Source**: step1.json (verified import)
**Components**: Screen + Frame + TextWidget2
**Status**: PASS

## What This Tests
- Minimum viable Retool app structure
- Screen plugin, Frame plugin, single widget
- TextWidget2 with markdown content

## Plugin Structure (3 plugins)

### 1. Screen: `page1`
```python
screen_plugin("page1", "Step 1 Test", "step-1-test", 0)
```

### 2. Frame: `$main`
```python
frame_plugin("$main", "page1", "main")
```

### 3. Widget: `helloText` (TextWidget2)
```python
widget("helloText", "TextWidget2",
    tom(
        "heightType", "auto",
        "overflow", "scroll",
        "value", "# Hello World",
        "events", tlist([])
    ),
    pos(0, 0, 4, 6, "", "page1"),
    screen="page1")
```

## Key Fields for TextWidget2
From transit_patterns.json, TextWidget2 has these fields:
- `heightType` — "auto" (auto-resize) or "fixed"
- `overflow` — "scroll" or "hidden"
- `value` — the text content (supports `{{ }}` bindings and markdown)
- `events` — must be `tlist([])`

## Transit Encoding Notes
- Template uses `tom()` (ordered map) — required for all widget templates
- Events uses `tlist([])` — required, NOT a plain `[]`
- Style is `tom()` (empty ordered map) — set by `widget()` helper
- Screen plugins have `style=None` (not `tom()`)

## Gotchas
- TextWidget2 only has 4 template fields — one of the simplest widgets
- The `value` field supports markdown: `"# Heading"`, `"**bold**"`, etc.
- Dynamic bindings work: `"{{ queryName.data }}"`
