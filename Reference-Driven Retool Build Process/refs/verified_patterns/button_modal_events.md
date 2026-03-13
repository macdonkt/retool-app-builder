# Verified Pattern: Button + Modal + Event Handlers

**Source**: step4.json (verified import)
**Components**: Screen + Frame + TextWidget2 + ButtonWidget2 + JavascriptQuery + TableWidget2 + ModalFrameWidget
**Status**: PASS

## What This Tests
- ButtonWidget2 with click event handler
- ModalFrameWidget (starts hidden)
- Event: button click → show modal
- Event handler Transit encoding (must be `tom()`)

## ButtonWidget2 Template (key fields)
```python
tom(
    "text", "+ Add Item",
    "disabled", "",
    "hidden", "",
    "loading", "",
    "iconBefore", None,
    "iconAfter", None,
    "iconColor", "",
    "loaderPosition", "center",
    "maintainSpaceWhenHidden", False,
    "heightType", "fixed",
    "variant", "solid",
    "tooltipText", "",
    "showBorderOnHover", True,
    "events", tlist([
        evt_show_frame("click", "addModal"),
    ]),
)
```

## Event Handler Structure
All event handlers MUST use `tom()` — Retool calls `.get()` on them.

### Show Modal Event
```python
evt_show_frame("click", "addModal")
# Expands to:
tom(
    "id", str(uuid.uuid4()),
    "type", "widget",
    "waitMs", "0",
    "waitType", "debounce",
    "event", "click",
    "method", "show",
    "pluginId", "addModal",
    "targetId", None,
    "params", tom()
)
```

### Hide Modal Event
```python
evt_hide_frame("click", "addModal")
# method: "hide" instead of "show"
```

### Trigger Query Event
```python
evt_trigger_query("success", "nextQuery")
# type: "datasource", method: "trigger"
```

### Set State Variable Event
```python
evt_set_var("success", "varName", "{{ expression }}")
# type: "state", method: "setValue"
# params: tom("value", "{{ expression }}")
```

### Show Notification Event
```python
evt_notification("click", "success", "Title", "Description", 4.5)
# type: "util", method: "showNotification"
# params: tom("options", tom("notificationType", "success", "title", ..., "description", ..., "duration", 4.5))
```

## ModalFrameWidget Template
```python
tom(
    "size", "medium",           # "small", "medium", "large", "extraLarge"
    "hideOnEscape", True,
    "overlayInteraction", True,
    "headerPadding", "8px 12px",
    "showFooterBorder", True,
    "enableFullBleed", False,
    "isHiddenOnDesktop", False,
    "showBorder", True,
    "hidden", True,             # starts hidden — shown via event
    "showHeader", True,
    "padding", "8px 12px",
    "showOverlay", True,
    "isHiddenOnMobile", True,
    "showHeaderBorder", True,
    "footerPadding", "8px 12px",
    "showFooter", True,
    "events", tlist([])
)
```

## Modal Children Positioning
Widgets inside a modal use `row_group` for section placement:
```python
# Header section
pos(0, 0, 3, 12, "addModal", "page1", row_group="header")

# Body section
pos(0, 0, 7, 6, "addModal", "page1", row_group="body")

# Footer section
pos(0, 0, 5, 2, "addModal", "page1", row_group="footer")
```

## Transit Encoding Rules
- Event handlers: `tom()` — NEVER `tmap()`
- Events list: `tlist([...])` — NEVER plain `[...]`
- Nested `params` in events: `tom()` — NEVER `tmap()`
- Widget `style`: `tom()` (empty ordered map)
- Modal/frame `style`: `tom()` (empty ordered map)

## Gotchas
- `hidden=True` on the modal template makes it start invisible
- Modal children reference the modal ID in `subcontainer` (via `pos()` helper)
- Event `waitMs` is a STRING `"0"`, not integer `0`
- Event `id` must be a UUID string
