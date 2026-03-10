# Retool App JSON Reference

Complete reference for generating valid Retool app JSON files for import.

## Table of Contents

1. [JSON Structure Overview](#json-structure-overview)
2. [Transit JSON Encoding](#transit-json-encoding)
3. [Widget Components (96 Types)](#widget-components)
4. [Query Types (5 Types)](#query-types)
5. [Event Handlers](#event-handlers)
6. [Positioning System](#positioning-system)
7. [App Theme](#app-theme)
8. [Multi-Page Apps](#multi-page-apps)

---

## JSON Structure Overview

### Top-Level Structure

```json
{
  "uuid": "unique-app-uuid",
  "page": {
    "id": 123456789,
    "data": {
      "appState": "<Transit-encoded JSON string>"
    },
    "changesRecord": [],
    "changesRecordV2": [],
    "checksum": null,
    "multiplayerSessionId": "uuid",
    "appTestingSaveId": null,
    "subflows": null,
    "isCopilotGenerated": false,
    "createdAt": "ISO-8601 timestamp",
    "updatedAt": "ISO-8601 timestamp",
    "pageId": 123456,
    "userId": 123456
  },
  "modules": {}
}
```

### AppState Structure (decoded)

The `appState` field contains the entire app definition in Transit JSON format:

```
["~#iR", ["^ ", "n", "appTemplate", "v", [app configuration...]]]
```

Key sections within appState:
- **appTemplate** - Global app settings
- **plugins** - All components, queries, screens, and frames
- **preloadedAppData** - Data loaded at app startup

---

## Transit JSON Encoding

Retool uses Transit JSON, a format that compresses repeated string keys across the document.

### ⚠️ CRITICAL: Never Build appState From Scratch

**Building appState from scratch will always fail** with:
> "Failed import — Tried to deserialize Record type named 'undefined'"

The Transit cache key assignments (`^0`, `^1;`, `^1M`, etc.) are established by the encoding sequence of the original file. Any hand-written file will have different cache slot assignments and the Retool reader will fail to resolve them.

**The only correct approach:**
1. Start from a real Retool-exported JSON file (use a file from `apps/general references/` or a previous working build)
2. Modify it in Python by navigating the parsed structure
3. Re-serialize with `json.dumps(separators=(',', ':'))`

See the [Building Apps by Modifying a Base File](#building-apps-by-modifying-a-base-file) section for the Python pattern.

---

### Type Markers

| Marker | Meaning |
|--------|---------|
| `~#iR` | Root Record |
| `~#iL` | List (array) |
| `~#iOM` | Ordered Map |
| `~#iM` | Map |
| `~m` | Timestamp (milliseconds) |
| `["^ ", ...]` | Transit map (flat key-value list) |

### appState Root Structure

```
["~#iR", ["^ ", "n", "appTemplate", "v",
  ["^ ",
    "appMaxWidth", "100%",
    ...app config fields...,
    "plugins", ["~#iOM", [
      "page1",  [plugin_data],
      "$main",  [plugin_data],
      "query1", [plugin_data],
      ...
    ]]
  ]
]]
```

### Plugin Wrapper Format (REQUIRED)

Every plugin value in the iOM **must** follow this exact structure:

```
["^0", ["^ ", "n", "pluginTemplate", "v",
  ["^ ",
    "id",   "pluginId",
    "^19",  null,             // uuid
    "^1:",  null,             // _comment
    "^1;",  "widget",         // type: "widget" | "datasource" | "frame" | "screen"
    "^1<",  "ButtonWidget2",  // subtype (widget class name)
    "^1=",  null,             // namespace
    "^1>",  null,             // resourceName ("Samsara", "JavascriptQuery", etc.)
    "^1?",  null,             // resourceDisplayName
    "^1@",  ["^1M", [...]],   // template (settings map)
    "^1A",  ["^1M", []],      // style (["^1M", []] for widgets; null for queries)
    "^1B",  [position2],      // position2 (see below; null for queries)
    "^1C",  null,             // mobilePosition2
    "^1D",  null,             // mobileAppPosition
    "^1E",  null,             // tabIndex
    "^1F",  "$main",          // container (parent frame ID)
    "^7",   "~m1769620000000", // createdAt
    "^1G",  "~m1769620000000", // updatedAt
    "^1H",  "",               // folder
    "^1I",  null,             // presetName
    "^1J",  "page1",          // screen (page assignment)
    "^1K",  null,             // boxId
    "^1L",  null              // subBoxIds
  ]
]]
```

### Position2 Format

```
["^0", ["^ ", "n", "position2", "v",
  ["^ ",
    "^1;", "grid",    // type = "grid"
    "^1F", "$main",   // container (parent frame)
    "^1N", "body",    // rowGroup: "body" | "header" | "footer"
    "^1O", "",        // subcontainer
    "row", 0,         // grid row (literal key)
    "col", 0,         // grid column (literal key)
    "^1P", 5,         // height (row units)
    "^1Q", 12,        // width (columns, 1–12)
    "^1R", 0,         // tabNum
    "^1S", null       // stackPosition
  ]
]]
```

### Confirmed Transit Cache Key Reference

These cache ref → field name mappings are confirmed from real Retool-exported files:

| Cache Ref | Field / Meaning | Notes |
|-----------|----------------|-------|
| `^0` | pluginTemplate record type | Outer plugin wrapper + position2 wrapper |
| `^7` | `createdAt` | Timestamp field |
| `^19` | `uuid` | Plugin UUID |
| `^1:` | `_comment` | Always null |
| `^1;` | `type` | Also reused as `"grid"` key in position |
| `^1<` | `subtype` | Widget/query class name |
| `^1=` | `namespace` | Usually null |
| `^1>` | `resourceName` | e.g. `"Samsara"`, `"JavascriptQuery"` |
| `^1?` | `resourceDisplayName` | |
| `^1@` | `template` | Settings map |
| `^1A` | `style` | `["^1M", []]` for widgets, null for queries |
| `^1B` | `position2` | Grid position wrapper |
| `^1C` | `mobilePosition2` | null |
| `^1D` | `mobileAppPosition` | null |
| `^1E` | `tabIndex` | null |
| `^1F` | `container` | Parent frame ID (also reused in position2) |
| `^1G` | `updatedAt` | Timestamp |
| `^1H` | `folder` | Empty string `""` |
| `^1I` | `presetName` | null |
| `^1J` | `screen` | Page assignment, e.g. `"page1"` |
| `^1K` | `boxId` | null |
| `^1L` | `subBoxIds` | null |
| `^1M` | Inner map type marker | Used as `["^1M", [...]]` for template/column maps |
| `^1N` | `rowGroup` (in position) | `"body"` \| `"header"` \| `"footer"` |
| `^1O` | `subcontainer` (in position) | Empty string |
| `^1P` | `height` (in position) | Row units |
| `^1Q` | `width` (in position) | Grid columns (1–12) |
| `^1R` | `tabNum` (in position) | `0` |
| `^1S` | `stackPosition` (in position) | null |
| `^A` | Empty array | `["^A", []]` |

---

## Building Apps by Modifying a Base File

### The Python Modification Pattern

```python
import json, copy

# 1. Load a valid base file
with open('apps/general references/components exmple.json', 'r') as f:
    outer = json.loads(f.read())

app_state = outer['page']['data']['appState']
transit = json.loads(app_state)

# 2. Navigate to the plugins iOM list
def find_iom(obj, depth=0):
    if depth > 10: return None
    if isinstance(obj, list):
        if len(obj) >= 2 and obj[0] == '~#iOM':
            return obj[1]
        for item in obj:
            r = find_iom(item, depth+1)
            if r: return r
    return None

plugins_list = find_iom(transit)
# plugins_list is a flat list: [key, value, key, value, ...]
# where each value is ["^0", ["^ ", "n", "pluginTemplate", "v", [v_map]]]

# 3. Navigation helpers
def get_plugin(name):
    for i in range(0, len(plugins_list)-1, 2):
        if plugins_list[i] == name:
            return plugins_list[i+1]
    return None

def get_v(pdata):
    """Get the v-map from a plugin."""
    # pdata = ["^0", ["^ ", "n", "pluginTemplate", "v", v_map]]
    outer = pdata[1]
    return outer[outer.index('v') + 1]

def get_template_data(v_map):
    """Get the flat list inside the '^1@' template map."""
    return v_map[v_map.index('^1@') + 1][1]

def set_val(flat_list, key, new_val):
    """Set value by key in a flat [k, v, k, v, ...] list."""
    flat_list[flat_list.index(key) + 1] = new_val

def get_position_data(v_map):
    pos_wrapper = v_map[v_map.index('^1B') + 1]
    pos_outer = pos_wrapper[1]
    return pos_outer[pos_outer.index('v') + 1]

def set_position(v_map, row, col, height, width):
    p = get_position_data(v_map)
    set_val(p, 'row', row)
    set_val(p, 'col', col)
    set_val(p, '^1P', height)
    set_val(p, '^1Q', width)

def remove_plugin(name):
    for i in range(0, len(plugins_list)-1, 2):
        if plugins_list[i] == name:
            plugins_list.pop(i)
            plugins_list.pop(i)
            return

def add_plugin(name, pdata):
    plugins_list.append(name)
    plugins_list.append(pdata)
```

### Creating a New Widget Plugin

Copy the structure of an existing similar widget — **never create from scratch**:

```python
def make_widget(plugin_id, subtype, row, col, height, width, template_kvs):
    """Build a new widget plugin in v2 Transit format."""
    position = ["^0", ["^ ", "n", "position2", "v",
        ["^ ", "^1;", "grid", "^1F", "$main", "^1N", "body", "^1O", "",
         "row", row, "col", col, "^1P", height, "^1Q", width, "^1R", 0, "^1S", None]
    ]]

    tpl_flat = []
    for k, v in template_kvs.items():
        tpl_flat.extend([k, v])

    v_map_flat = [
        "^ ",
        "id", plugin_id,
        "^19", None,      # uuid
        "^1:", None,      # _comment
        "^1;", "widget",  # type
        "^1<", subtype,   # subtype
        "^1=", None,      # namespace
        "^1>", None,      # resourceName
        "^1?", None,      # resourceDisplayName
        "^1@", ["^1M", tpl_flat],  # template
        "^1A", ["^1M", []],        # style
        "^1B", position,           # position2
        "^1C", None, "^1D", None, "^1E", None,
        "^1F", "$main",            # container
        "^7",  "~m1769620000000",  # createdAt
        "^1G", "~m1769620000000",  # updatedAt
        "^1H", "",                 # folder
        "^1I", None,               # presetName
        "^1J", "page1",            # screen
        "^1K", None,               # boxId
        "^1L", None,               # subBoxIds
    ]

    return ["^0", ["^ ", "n", "pluginTemplate", "v", v_map_flat]]

# Example: add a text widget
add_plugin('appTitle', make_widget(
    'appTitle', 'TextWidget2', 0, 0, 4, 12,
    {"heightType": "auto", "value": "# My App Title", "hidden": False,
     "margin": "4px 8px", "showInEditor": False}
))
```

### Creating a New Query Plugin

```python
def make_query(plugin_id, subtype, resource_name, code_or_query):
    """Build a new query plugin in v2 Transit format."""
    tpl_flat = [
        "queryRefreshTime", "",
        "allowedGroupIds", ["^A", []],
        "isFunction", False,
        "queryDisabledMessage", "",
        "successMessage", "",
        "queryDisabled", "",
        "runWhenModelUpdates", False,
        "showFailureToaster", True,
        "query", code_or_query,
        "showSuccessToaster", False,
        "isFetching", False,
        "finished", None,
    ]

    v_map_flat = [
        "^ ",
        "id", plugin_id,
        "^19", None,
        "^1:", None,
        "^1;", "datasource",
        "^1<", subtype,
        "^1=", None,
        "^1>", resource_name,
        "^1?", None,
        "^1@", ["^1M", tpl_flat],
        "^1A", None,    # no style for queries
        "^1B", None,    # no position for queries
        "^1C", None, "^1D", None, "^1E", None,
        "^1F", "$main",
        "^7",  "~m1769620000000",
        "^1G", "~m1769620000000",
        "^1H", "",
        "^1I", None,
        "^1J", "page1",
        "^1K", None,
        "^1L", None,
    ]

    return ["^0", ["^ ", "n", "pluginTemplate", "v", v_map_flat]]

# Example: JS query
add_plugin('qRunReport', make_query(
    'qRunReport', 'JavascriptQuery', 'JavascriptQuery',
    'return await someQuery.trigger();'
))
```

### Save and Validate

```python
# Re-serialize and validate
new_app_state = json.dumps(transit, separators=(',', ':'))

# Verify both layers parse
json.loads(new_app_state)       # appState must be valid JSON
outer['page']['data']['appState'] = new_app_state
output = json.dumps(outer, separators=(',', ':'))
json.loads(output)              # outer must be valid JSON

with open('apps/MyProject/output.json', 'w') as f:
    f.write(output)
```

### TableWidget2 Column Format

The real Retool table uses `_columnIds` + separate maps for per-column settings (not a simple `columns` array):

```python
cols = ["aa001", "bb002", "cc003"]  # column ID strings

template_kvs = {
    "selectedRowKey": None,
    "data": "{{ myQuery.data }}",
    "heightType": "fixed",
    "disableEdits": True,
    "disableSave": True,
    "_rowHeight": "medium",
    "_columnIds": ["^A", cols],
    "_columnKey": ["^1M", [               # data field → column mapping
        "aa001", "field_a",
        "bb002", "field_b",
        "cc003", "field_c",
    ]],
    "_columnTitle": ["^1M", [             # column header labels
        "aa001", "Column A",
        "bb002", "Column B",
        "cc003", "Column C",
    ]],
    "_columnFormat": ["^1M", [            # "string" | "html" | "number"
        "aa001", "string",
        "bb002", "string",
        "cc003", "html",
    ]],
    "_columnValueOverride": ["^1M", [     # cell expression per column
        "aa001", "{{ currentSourceRow.field_a || '' }}",
        "bb002", "{{ currentSourceRow.field_b || '' }}",
        "cc003", "{{ currentSourceRow.field_c || '' }}",
    ]],
    "_columnTextColor": ["^1M", [         # text color per column (empty = default)
        "aa001", "",
        "bb002", "{{ currentSourceRow.type === 'total' ? '#e6820e' : 'inherit' }}",
        "cc003", "",
    ]],
    "_columnAlignment": ["^1M", [
        "aa001", "left", "bb002", "left", "cc003", "right",
    ]],
    "_columnBackgroundColor": ["^1M", ["aa001", "", "bb002", "", "cc003", ""]],
    "_columnAlternateRowBackgroundColor": ["^1M", ["aa001", "", "bb002", "", "cc003", ""]],
    "_columnSearchMode": ["^1M", ["aa001", "default", "bb002", "default", "cc003", "default"]],
    "_columnSortDisabled": ["^1M", ["aa001", False, "bb002", False, "cc003", False]],
    "_columnEditableOptions": ["^1M", ["aa001", ["^1M", []], "bb002", ["^1M", []], "cc003", ["^1M", []]]],
    "_columnCellTooltip": ["^1M", ["aa001", "", "bb002", "", "cc003", ""]],
    "_columnTooltip": ["^1M", ["aa001", "", "bb002", "", "cc003", ""]],
    "_columnIcon": ["^1M", ["aa001", "", "bb002", "", "cc003", ""]],
    "_primaryKeyColumnId": "aa001",
    "_rowColor": "{{ currentSourceRow.type === 'total' ? '#f0f0f0' : '#ffffff' }}",
    "autoColumnWidth": False,
    "showPagination": True,
    "showSearch": False,
    "showFilter": False,
    "showDownload": True,
    "showRefresh": True,
    "hidden": False,
    "loading": False,
    "events": [],
    "style": ["^1M", [["rowSeparator", "surfacePrimaryBorder"]]],
}
```

> **Note**: Use `currentSourceRow` (not `currentRow`) in column value expressions and row color expressions.

---

## Widget Components

### Complete Widget Type List (96 Components)

#### Input Components
| Widget Type | Description |
|-------------|-------------|
| `TextInputWidget2` | Single-line text input |
| `TextAreaWidget` | Multi-line text input |
| `NumberInputWidget` | Numeric input with formatting |
| `PasswordInputWidget` | Password field |
| `PhoneNumberInputWidget` | Phone number with formatting |
| `ColorInputWidget` | Color picker |
| `DateWidget` | Date picker |
| `DateTimeWidget` | Date and time picker |
| `DateRangeWidget` | Date range selector |
| `TimeWidget` | Time picker |
| `CalendarInputWidget` | Calendar date input |
| `SelectWidget2` | Dropdown select |
| `MultiselectWidget2` | Multi-select dropdown |
| `ListboxWidget` | Listbox selection |
| `MultiselectListboxWidget` | Multi-select listbox |
| `CascaderWidget2` | Cascading dropdown |
| `CheckboxWidget2` | Single checkbox |
| `CheckboxGroupWidget2` | Checkbox group |
| `RadioGroupWidget2` | Radio button group |
| `SwitchWidget2` | Toggle switch |
| `SliderWidget2` | Slider input |
| `RangeSliderWidget` | Range slider |
| `RatingWidget2` | Star rating |
| `SegmentedControlWidget` | Segmented control |
| `FileInputWidget` | File input |
| `FileButtonWidget` | File upload button |
| `FileDropzoneWidget` | Drag-drop file zone |
| `MicrophoneWidget2` | Audio recording |
| `ScannerWidget2` | Barcode/QR scanner |

#### Display Components
| Widget Type | Description |
|-------------|-------------|
| `TextWidget2` | Text/markdown display |
| `IconWidget` | Icon display |
| `IconTextWidget` | Icon with text |
| `ImageWidget2` | Image display |
| `ImageGridWidget` | Image gallery |
| `AvatarWidget` | User avatar |
| `AvatarGroupWidget` | Avatar group |
| `StatisticWidget2` | Statistic display |
| `ProgressBarWidget` | Progress bar |
| `ProgressCircleWidget` | Circular progress |
| `StatusWidget` | Status indicator |
| `TagsWidget2` | Tags display |
| `AlertWidget2` | Alert message |
| `QRCodeWidget` | QR code generator |
| `VideoWidget` | Video player |
| `PDFViewerWidget2` | PDF viewer |
| `HTMLWidget` | Raw HTML |
| `IFrameWidget2` | Embedded iframe |
| `TimelineWidget` | Timeline display |
| `TimelineWidget2` | Timeline v2 |
| `TimerWidget` | Countdown/timer |

#### Data Components
| Widget Type | Description |
|-------------|-------------|
| `TableWidget2` | Data table |
| `ListViewWidget2` | List view |
| `KeyValueWidget2` | Key-value display |
| `JSONExplorerWidget` | JSON tree viewer |
| `JSONEditorWidget` | JSON editor |
| `ChartWidget2` | Charts/graphs |
| `CalendarWidget2` | Calendar view |
| `MapWidget` | Map display |

#### Form Components
| Widget Type | Description |
|-------------|-------------|
| `FormWidget2` | Form container |
| `JSONSchemaFormWidget` | JSON Schema form |
| `WizardWidget` | Multi-step wizard |
| `StripeCardFormWidget` | Stripe payment |

#### Layout Components
| Widget Type | Description |
|-------------|-------------|
| `ContainerWidget2` | Container |
| `TabsWidget2` | Tabs container |
| `ModalFrameWidget` | Modal dialog |
| `DrawerFrameWidget` | Drawer panel |
| `SplitPaneFrameWidget` | Split pane |
| `SpacerWidget` | Spacer |
| `DividerWidget` | Divider line |

#### Navigation Components
| Widget Type | Description |
|-------------|-------------|
| `NavigationWidget2` | Navigation menu |
| `BreadcrumbsWidget` | Breadcrumb trail |
| `StepsWidget` | Step indicator |
| `PaginationWidget` | Pagination |
| `PageInputWidget` | Page number input |
| `LinkWidget` | Link |
| `LinkListWidget` | Link list |

#### Button Components
| Widget Type | Description |
|-------------|-------------|
| `ButtonWidget2` | Button |
| `ButtonGroupWidget2` | Button group |
| `DropdownButtonWidget` | Dropdown button |
| `SplitButtonWidget` | Split button |
| `ToggleButtonWidget` | Toggle button |
| `ToggleLinkWidget` | Toggle link |

#### Advanced Components
| Widget Type | Description |
|-------------|-------------|
| `FilterWidget` | Data filter |
| `TextEditorWidget` | Rich text editor |
| `EditableTextWidget2` | Inline editable text |
| `EditableTextAreaWidget` | Inline editable textarea |
| `EditableNumberWidget` | Inline editable number |
| `TextAnnotationWidget` | Text annotation |
| `BoundingBoxWidget` | Bounding box annotation |
| `ReorderableListWidget` | Drag-reorder list |
| `CommentThreadWidget` | Comments |

#### AI Components
| Widget Type | Description |
|-------------|-------------|
| `ChatWidget` | Chat interface |
| `AgentChatWidget` | AI Agent chat |

#### Auth & Integration
| Widget Type | Description |
|-------------|-------------|
| `AuthLoginWidget` | Login form |
| `LookerWidget` | Looker embed |
| `TableauWidget` | Tableau embed |

---

### Widget Template Structure

> **Note**: The JSON objects below document the *template field contents* only — the actual in-file Transit format wraps them in the plugin wrapper structure described above. When modifying a file in Python, you navigate to the template map and edit values there.

**Template fields** (the settings inside `"^1@": ["^1M", [...]]`):

The template contains widget-specific properties as a flat key-value list. Examples for each widget type are shown in the sections below.

**Non-template plugin fields** use Transit cache refs as documented in the cache key table above. When building via Python, use the confirmed cache refs exactly — do not use literal field names like `"uuid"` or `"type"` in place of `"^19"` or `"^1;"`.

**Inner maps** within templates use `["^1M", [k, v, k, v, ...]]` format.
**Arrays** use `["^A", [item1, item2, ...]]` or plain `[]`.

---

### Common Widget Templates

#### TextWidget2
```json
{
  "heightType": "auto",
  "horizontalAlign": "left",
  "hidden": false,
  "imageWidth": "fit",
  "margin": "4px 8px",
  "showInEditor": false,
  "verticalAlign": "center",
  "tooltipText": "",
  "value": "# Heading Text",
  "disableMarkdown": false,
  "overflowType": "scroll",
  "maintainSpaceWhenHidden": false
}
```

#### ButtonWidget2
```json
{
  "heightType": "fixed",
  "horizontalAlign": "stretch",
  "clickable": false,
  "iconAfter": "",
  "submitTargetId": null,
  "hidden": false,
  "ariaLabel": "",
  "text": "Button Text",
  "margin": "4px 8px",
  "showInEditor": false,
  "tooltipText": "",
  "allowWrap": true,
  "styleVariant": "solid",
  "submit": false,
  "iconBefore": "",
  "events": [],
  "loading": false,
  "disabled": false,
  "maintainSpaceWhenHidden": false
}
```

#### TextInputWidget2
```json
{
  "spellCheck": false,
  "readOnly": false,
  "iconAfter": "",
  "showCharacterCount": false,
  "autoComplete": false,
  "enforceMaxLength": false,
  "maxLength": null,
  "hidden": false,
  "customValidation": "",
  "patternType": "",
  "hideValidationMessage": false,
  "textBefore": "",
  "validationMessage": "",
  "margin": "4px 8px",
  "textAfter": "",
  "showInEditor": false,
  "showClear": true,
  "pattern": "",
  "tooltipText": "",
  "labelAlign": "left",
  "formDataKey": "{{ self.id }}",
  "value": "",
  "labelCaption": "",
  "labelWidth": "33",
  "label": "Label",
  "placeholder": "Enter text",
  "labelWidthUnit": "%",
  "invalid": false,
  "events": [],
  "inputValue": "",
  "loading": false,
  "minLength": null,
  "disabled": false,
  "required": false,
  "maintainSpaceWhenHidden": false
}
```

#### SelectWidget2
```json
{
  "readOnly": false,
  "iconAfter": "",
  "hidden": false,
  "customValidation": "",
  "hideValidationMessage": false,
  "textBefore": "",
  "validationMessage": "",
  "margin": "4px 8px",
  "textAfter": "",
  "showInEditor": false,
  "showClear": true,
  "tooltipText": "",
  "labelAlign": "left",
  "formDataKey": "{{ self.id }}",
  "values": ["option1", "option2"],
  "labels": ["Option 1", "Option 2"],
  "value": null,
  "labelCaption": "",
  "labelWidth": "33",
  "label": "Select",
  "placeholder": "Select an option",
  "labelWidthUnit": "%",
  "invalid": false,
  "events": [],
  "loading": false,
  "disabled": false,
  "required": false,
  "maintainSpaceWhenHidden": false
}
```

#### TableWidget2
```json
{
  "selectedRowKey": null,
  "showPagination": true,
  "showSearch": true,
  "showFilter": true,
  "showDownload": true,
  "showRefresh": true,
  "allowMultiRowSelect": false,
  "data": "{{ query1.data }}",
  "columns": [],
  "events": [],
  "rowHeight": "medium",
  "striped": true,
  "bordered": true,
  "loading": false,
  "hidden": false
}
```

#### FormWidget2
```json
{
  "disableSubmit": false,
  "heightType": "auto",
  "headerPadding": "4px 12px",
  "showFooterBorder": true,
  "resetAfterSubmit": true,
  "submitting": false,
  "enableFullBleed": false,
  "showBorder": true,
  "hidden": false,
  "data": {},
  "showHeader": true,
  "hoistFetching": false,
  "initialData": null,
  "margin": "4px 8px",
  "showInEditor": false,
  "tooltipText": "",
  "padding": "12px",
  "showHeaderBorder": true,
  "footerPadding": "4px 12px",
  "invalid": false,
  "showFooter": true,
  "_type": "grid",
  "events": [],
  "loading": false,
  "overflowType": "scroll",
  "disabled": false,
  "requireValidation": true,
  "maintainSpaceWhenHidden": false,
  "showBody": true
}
```

#### ContainerWidget2
```json
{
  "_direction": "horizontal",
  "heightType": "auto",
  "currentViewKey": null,
  "clickable": false,
  "headerPadding": "4px 12px",
  "showFooterBorder": true,
  "enableFullBleed": false,
  "showBorder": true,
  "hidden": false,
  "showHeader": true,
  "margin": "4px 8px",
  "showInEditor": false,
  "tooltipText": "",
  "padding": "12px",
  "showHeaderBorder": true,
  "footerPadding": "4px 12px",
  "showFooter": true,
  "_type": "grid",
  "events": [],
  "loading": false,
  "overflowType": "scroll",
  "maintainSpaceWhenHidden": false,
  "showBody": true
}
```

#### ModalFrameWidget
```json
{
  "size": "medium",
  "hideOnEscape": true,
  "overlayInteraction": true,
  "headerPadding": "8px 12px",
  "showFooterBorder": true,
  "enableFullBleed": false,
  "isHiddenOnDesktop": false,
  "showBorder": true,
  "hidden": true,
  "showHeader": true,
  "padding": "8px 12px",
  "showOverlay": true,
  "isHiddenOnMobile": true,
  "showHeaderBorder": true,
  "footerPadding": "8px 12px",
  "showFooter": true,
  "events": []
}
```

#### MapWidget
```json
{
  "hoveredOverPoint": null,
  "pointValue": "",
  "points": "{{ query.data }}",
  "latitude": "37.7577",
  "onPointSelected": "",
  "latitudeColumnName": "latitude",
  "longitude": "-122.4376",
  "longitudeColumnName": "longitude",
  "zoom": "8",
  "onViewportChange": "",
  "selectedPoint": null,
  "visiblePoints": []
}
```

#### ChartWidget2
```json
{
  "heightType": "fixed",
  "chartType": "bar",
  "data": "{{ query.data }}",
  "xAxis": "category",
  "yAxis": ["value"],
  "hidden": false,
  "margin": "4px 8px",
  "tooltipText": "",
  "loading": false
}
```

#### DateWidget
```json
{
  "minDate": "",
  "readOnly": false,
  "iconAfter": "",
  "datePlaceholder": "{{ self.dateFormat.toUpperCase() }}",
  "dateFormat": "MMM d, yyyy",
  "hidden": false,
  "customValidation": "",
  "hideValidationMessage": false,
  "textBefore": "",
  "validationMessage": "",
  "margin": "4px 8px",
  "textAfter": "",
  "showInEditor": false,
  "showClear": false,
  "tooltipText": "",
  "labelAlign": "left",
  "formDataKey": "{{ self.id }}",
  "value": "{{ new Date() }}",
  "labelCaption": "",
  "labelWidth": "33",
  "label": "Date",
  "labelWidthUnit": "%",
  "invalid": false,
  "events": [],
  "disabled": false,
  "required": false
}
```

#### NumberInputWidget
```json
{
  "readOnly": false,
  "iconAfter": "",
  "max": null,
  "preventScroll": false,
  "inputValue": 0,
  "hidden": false,
  "customValidation": "",
  "showSeparators": true,
  "hideValidationMessage": false,
  "textBefore": "",
  "validationMessage": "",
  "margin": "4px 8px",
  "textAfter": "",
  "showInEditor": false,
  "allowNull": false,
  "showClear": false,
  "tooltipText": "",
  "currency": "USD",
  "labelAlign": "left",
  "formDataKey": "{{ self.id }}",
  "value": 0,
  "labelCaption": "",
  "labelWidth": "33",
  "label": "Number",
  "min": null,
  "placeholder": "",
  "labelWidthUnit": "%",
  "invalid": false,
  "events": [],
  "decimalPlaces": null,
  "loading": false,
  "disabled": false,
  "required": false
}
```

#### StatisticWidget2
```json
{
  "clickable": false,
  "positiveTrend": "{{ self.value >= 0 }}",
  "signDisplay": "auto",
  "secondaryCurrency": "USD",
  "secondarySuffix": "",
  "align": "left",
  "secondaryPrefix": "",
  "secondaryEnableTrend": false,
  "secondaryDecimalPlaces": 1,
  "hidden": false,
  "showSeparators": true,
  "formattingStyle": "currency",
  "margin": "4px 8px",
  "showInEditor": false,
  "tooltipText": "",
  "currency": "USD",
  "suffix": "",
  "prefix": "",
  "value": 1234,
  "decimalPlaces": 0,
  "enableTrend": false,
  "caption": "Total",
  "loading": false,
  "secondaryValue": null
}
```

#### AlertWidget2
```json
{
  "showIcon": true,
  "hidden": false,
  "title": "Alert Title",
  "description": "Alert description text",
  "margin": "4px 8px",
  "showInEditor": false,
  "tooltipText": "",
  "type": "info",
  "showClose": true,
  "events": []
}
```

---

## Query Types

### RESTQuery

```json
{
  "id": "queryName",
  "type": "datasource",
  "subtype": "RESTQuery",
  "resourceName": "resource-uuid",
  "resourceDisplayName": "Resource Name",
  "template": {
    "queryRefreshTime": "",
    "allowedGroupIds": [],
    "streamResponse": false,
    "body": "",
    "lastReceivedFromResourceAt": null,
    "isFunction": false,
    "queryDisabledMessage": "",
    "successMessage": "",
    "queryDisabled": "",
    "runWhenModelUpdates": false,
    "headers": "",
    "showFailureToaster": true,
    "query": "?param={{ value }}",
    "showSuccessToaster": false,
    "runWhenPageLoads": true,
    "confirmationMessage": "",
    "requireConfirmation": false,
    "events": []
  }
}
```

### RetoolTableQuery (SQL)

```json
{
  "id": "queryName",
  "type": "datasource",
  "subtype": "RetoolTableQuery",
  "resourceName": "resource-uuid",
  "resourceDisplayName": "retool_db",
  "template": {
    "queryRefreshTime": "",
    "allowedGroupIds": [],
    "records": "",
    "isFunction": false,
    "queryDisabledMessage": "",
    "successMessage": "",
    "queryDisabled": "",
    "runWhenModelUpdates": false,
    "showFailureToaster": true,
    "query": "SELECT * FROM table WHERE id = {{ value }}",
    "showSuccessToaster": false,
    "runWhenPageLoads": true,
    "actionType": "select",
    "filterBy": [],
    "sortBy": [],
    "events": []
  }
}
```

### JavascriptQuery

```json
{
  "id": "queryName",
  "type": "datasource",
  "subtype": "JavascriptQuery",
  "resourceName": "JavascriptQuery",
  "template": {
    "queryRefreshTime": "",
    "allowedGroupIds": [],
    "isFunction": false,
    "queryDisabledMessage": "",
    "successMessage": "",
    "queryDisabled": "",
    "runWhenModelUpdates": false,
    "showFailureToaster": true,
    "query": "// JavaScript code\nconst result = table1.data.map(row => ({\n  ...row,\n  total: row.price * row.quantity\n}));\nreturn result;",
    "showSuccessToaster": false,
    "runWhenPageLoads": false,
    "isFetching": false,
    "events": []
  }
}
```

### RetoolAIQuery

```json
{
  "id": "aiQueryName",
  "type": "datasource",
  "subtype": "RetoolAIQuery",
  "template": {
    "prompt": "{{ textInput.value }}",
    "model": "gpt-4",
    "systemPrompt": "You are a helpful assistant.",
    "temperature": 0.7,
    "maxTokens": 1000,
    "showFailureToaster": true,
    "events": []
  }
}
```

### RetoolAIAgentInvokeQuery

```json
{
  "id": "agentQueryName",
  "type": "datasource",
  "subtype": "RetoolAIAgentInvokeQuery",
  "template": {
    "agentId": "agent-uuid",
    "input": "{{ userInput.value }}",
    "showFailureToaster": true,
    "events": []
  }
}
```

---

## State Slots (Variables)

State slots store app-level variables that persist across component interactions.

### State Slot Definition

```json
{
  "id": "variableName",
  "uuid": "unique-uuid",
  "_comment": null,
  "type": "state",
  "subtype": "StateSlot",
  "namespace": null,
  "resourceName": null,
  "resourceDisplayName": null,
  "template": {
    "value": "",
    "persistence": "none"
  },
  "style": null,
  "position2": null,
  "mobilePosition2": null,
  "mobileAppPosition": null,
  "tabIndex": null,
  "container": null,
  "createdAt": "~m1234567890",
  "updatedAt": "~m1234567890",
  "folder": "",
  "presetName": null,
  "screen": null,
  "boxId": null,
  "subBoxIds": null
}
```

### Persistence Options

| Value | Description |
|-------|-------------|
| `none` | Value resets on page refresh |
| `localStorage` | Persists in browser localStorage |
| `urlHash` | Stored in URL hash (shareable) |

### Common Variable Patterns

```json
// Timestamp variable
{
  "id": "lastSyncTime",
  "type": "state",
  "subtype": "StateSlot",
  "template": {
    "value": "",
    "persistence": "none"
  }
}

// Status message variable
{
  "id": "syncStatus",
  "type": "state",
  "subtype": "StateSlot",
  "template": {
    "value": "Ready",
    "persistence": "none"
  }
}

// Saved views array (with localStorage persistence)
{
  "id": "savedViews",
  "type": "state",
  "subtype": "StateSlot",
  "template": {
    "value": "[]",
    "persistence": "localStorage"
  }
}

// Current working value
{
  "id": "currentSQL",
  "type": "state",
  "subtype": "StateSlot",
  "template": {
    "value": "",
    "persistence": "none"
  }
}
```

### Setting Variable Values

In event handlers or JavaScript queries:

```javascript
// Set a simple value
variableName.setValue("new value")

// Set timestamp
lastSyncTime.setValue(new Date().toISOString())

// Set status message
syncStatus.setValue("Syncing...")

// Update array (saved views)
savedViews.setValue([...savedViews.value, { name: "New View", sql: currentSQL.value }])

// Clear value
variableName.setValue("")
```

### Reading Variable Values

```javascript
// In bindings
{{ variableName.value }}

// In JavaScript
const currentValue = variableName.value;

// Conditional display
{{ lastSyncTime.value ? `Last synced: ${lastSyncTime.value}` : 'Never synced' }}
```

---

## Event Handlers

### Event Structure

```json
{
  "events": [
    {
      "id": "unique-event-id",
      "type": "widget",
      "waitMs": "0",
      "waitType": "debounce",
      "event": "click",
      "method": "run",
      "pluginId": "targetQueryOrComponent",
      "targetId": null,
      "params": {
        "src": "query1.trigger()"
      }
    }
  ]
}
```

### Common Event Types

| Event | Components | Description |
|-------|------------|-------------|
| `click` | Button, Container, Image | Click action |
| `submit` | Form | Form submission |
| `change` | Input, Select, Checkbox | Value change |
| `rowClick` | Table | Row clicked |
| `rowSelect` | Table | Row selected |
| `clickToolbar` | Table | Toolbar button click |

### Common Methods

| Method | Description |
|--------|-------------|
| `run` | Execute code via `params.src` |
| `trigger` | Trigger a query |
| `setValue` | Set component value |
| `show` | Show modal/drawer |
| `hide` | Hide modal/drawer |
| `exportData` | Export table data |
| `openPage` | Navigate to page |

### Event Examples

#### Button Click - Run Query
```json
{
  "event": "click",
  "method": "run",
  "params": { "src": "saveData.trigger()" }
}
```

#### Button Click - Show Modal
```json
{
  "event": "click",
  "method": "run",
  "params": { "src": "modal1.show()" }
}
```

#### Button Click - Navigate
```json
{
  "event": "click",
  "method": "run",
  "params": { "src": "utils.openPage('pageName', {})" }
}
```

#### Form Submit
```json
{
  "event": "submit",
  "method": "run",
  "params": { "src": "submitQuery.trigger()" }
}
```

#### Query Success - Show Notification
```json
{
  "event": "success",
  "method": "run",
  "params": {
    "src": "utils.showNotification({ title: 'Success', description: 'Data saved', notificationType: 'success' })"
  }
}
```

#### Query Success - Refresh Table
```json
{
  "event": "success",
  "method": "run",
  "params": { "src": "getData.trigger()" }
}
```

---

## Positioning System

### Position2 Structure

```json
{
  "position2": {
    "type": "grid",
    "container": "parentId",
    "rowGroup": "body",
    "subcontainer": "",
    "row": 0,
    "col": 0,
    "height": 2,
    "width": 12,
    "tabNum": 0,
    "stackPosition": null
  }
}
```

### Grid System

- **12-column grid** layout
- `width`: 1-12 (columns to span)
- `height`: Row units (see standard heights below)
- `row`: Starting row position
- `col`: Starting column (0-11)

### Standard Height Units

Based on Retool AI patterns, use these consistent heights:

| Component Type | Height | Notes |
|----------------|--------|-------|
| Button | 5 | Standard clickable button |
| Text (heading) | 3-6 | `#### Heading` = 4, `# Title` = 6 |
| Text (body) | 4-5 | Single line status text |
| Text (paragraph) | 10+ | Multi-line explanations |
| TextInput | 1 | Single-line input |
| TextArea | 8-15 | Multi-line input |
| Table | 54+ | Data display area |
| Container | 11-80 | Groups of components |

### Row Spacing Conventions

```
Row 0-10:   App title and header controls
Row 11-23:  Secondary controls (sync, filters)
Row 24+:    Main content area
Row 100+:   Results/output section
```

Leave gaps between logical sections (e.g., row 24 starts main content after row 11-22 controls).

### Row Groups

| Row Group | Description |
|-----------|-------------|
| `body` | Main content area |
| `header` | Container/form header |
| `footer` | Container/form footer |

### Height Types

| Value | Description |
|-------|-------------|
| `auto` | Size to content |
| `fixed` | Fixed height in row units |
| `fill` | Fill available space |

---

## App Theme

### Theme Structure

```json
{
  "id": "$appTheme",
  "type": "setting",
  "subtype": "AppTheme",
  "template": {
    "value": {
      "surfacePrimaryBorder": "#e2e8f0",
      "primary": "#2563eb",
      "success": "#16a34a",
      "danger": "#dc2626",
      "warning": "#eab308",
      "info": "#3b82f6",
      "textDark": "#0f172a",
      "textLight": "#ffffff",
      "surfacePrimary": "#ffffff",
      "surfaceSecondary": "#f8fafc",
      "surfaceSecondaryBorder": "#cbd5e1",
      "highlight": "#fef3c7",
      "secondary": "#8b5cf6",
      "tertiary": "#06b6d4",
      "canvas": "#f8fafc",
      "borderRadius": "8px",
      "automatic": ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981", "#06b6d4"],
      "labelFont": { "size": "12px", "fontWeight": "500" },
      "labelEmphasizedFont": { "size": "12px", "fontWeight": "600" },
      "defaultFont": { "size": "12px", "fontWeight": "400" },
      "h1Font": { "size": "36px", "fontWeight": "700" },
      "h2Font": { "size": "28px", "fontWeight": "700" },
      "h3Font": { "size": "24px", "fontWeight": "700" },
      "h4Font": { "size": "18px", "fontWeight": "700" },
      "h5Font": { "size": "16px", "fontWeight": "700" },
      "h6Font": { "size": "14px", "fontWeight": "700" }
    }
  }
}
```

---

## Multi-Page Apps

### Screen Definition

```json
{
  "id": "pageName",
  "uuid": "unique-uuid",
  "type": "screen",
  "subtype": "Screen",
  "template": {
    "title": "Page Title",
    "browserTitle": "Browser Tab Title",
    "urlSlug": "page-url-slug",
    "_order": 0,
    "_searchParams": [],
    "_hashParams": [],
    "_customShortcuts": []
  }
}
```

### Frame Definition (Main Content Area)

```json
{
  "id": "$main",
  "type": "frame",
  "subtype": "Frame",
  "template": {
    "type": "main",
    "padding": "8px 12px",
    "enableFullBleed": false,
    "isHiddenOnDesktop": false,
    "isHiddenOnMobile": false
  },
  "container": "",
  "screen": "pageName"
}
```

### Header Frame

```json
{
  "id": "$header",
  "type": "frame",
  "subtype": "Frame",
  "template": {
    "type": "header",
    "sticky": true,
    "padding": "8px 12px",
    "enableFullBleed": false
  },
  "screen": "pageName"
}
```

### Navigation Between Pages

```javascript
// Navigate to page
utils.openPage('pageName', { param1: 'value1' })

// Navigate with URL params
utils.openPage('details', { id: table1.selectedRow.id })

// Access URL params in target page
{{ urlparams.id }}
```

---

## Data Binding

### Binding Syntax

```javascript
// Access query data
{{ queryName.data }}

// Access component value
{{ textInput.value }}
{{ select1.value }}
{{ table1.selectedRow }}
{{ table1.selectedRows }}

// Access form data
{{ form1.data }}

// Conditional binding
{{ condition ? 'value1' : 'value2' }}

// Transformations
{{ queryName.data.map(row => row.name) }}
{{ queryName.data.filter(row => row.active) }}

// Self reference
{{ self.value }}
{{ self.id }}
```

### Common Patterns

```javascript
// Table data from query
data: "{{ getUsers.data }}"

// Dropdown options from query
values: "{{ getOptions.data.map(r => r.id) }}"
labels: "{{ getOptions.data.map(r => r.name) }}"

// Conditional visibility
hidden: "{{ !currentUser.isAdmin }}"

// Form field default value
value: "{{ table1.selectedRow?.name || '' }}"

// Disabled state
disabled: "{{ form1.data.status === 'locked' }}"
```

---

## JavaScript Query Gotchas

### CRITICAL: `query.trigger()` Returns Data Directly

When using `await query.trigger()` inside a JavaScript query, the data is returned **directly from the trigger call**, NOT stored in `query.data` immediately.

#### The Problem

```javascript
// ❌ WRONG - query.data is null during execution
await myQuery.trigger();
console.log(myQuery.data);  // null!
const result = myQuery.data.results;  // Error!
```

The query executes successfully, but `myQuery.data` remains `null` until after the entire JavaScript function completes. This is a common source of "no results" bugs.

#### The Solution

```javascript
// ✅ CORRECT - capture the return value from trigger()
const result = await myQuery.trigger();
console.log(result);  // { results: [...], status: "OK" }
const items = result.results;  // Works!
```

#### Complete Example: Chained API Calls

```javascript
// Geocode an address, then search for hotels at those coordinates

// Step 1: Trigger geocoding and capture result
const geocodeResult = await geocodeAddress.trigger();

// Step 2: Validate the result (not geocodeAddress.data!)
if (geocodeResult && geocodeResult.status === 'OK' && geocodeResult.results?.length > 0) {
  const lat = geocodeResult.results[0].geometry.location.lat;
  const lng = geocodeResult.results[0].geometry.location.lng;

  console.log('Coordinates:', lat, lng);

  // Step 3: Trigger hotel search and capture its result
  const hotelsResult = await searchHotels.trigger();

  // Step 4: Process hotels (not searchHotels.data!)
  const hotelCount = hotelsResult?.result?.length || 0;

  if (hotelCount > 0) {
    utils.showNotification({
      title: 'Success',
      description: `Found ${hotelCount} hotels`,
      notificationType: 'success'
    });
  }
} else {
  utils.showNotification({
    title: 'Geocoding failed',
    description: 'Could not find location',
    notificationType: 'error'
  });
}
```

#### When `.data` DOES Work

The `.data` property works in these contexts:

1. **Template bindings** (outside JavaScript queries):
   ```javascript
   // In a component's data property - this works
   {{ myQuery.data }}
   {{ myQuery.data.results[0].name }}
   ```

2. **After the JavaScript query completes** - other queries/components can read `.data`

3. **In event handlers on the query itself**:
   ```javascript
   // In query success event handler - this works
   utils.showNotification({ description: myQuery.data.message })
   ```

#### Debugging Tip

Always add console.log to verify what you're getting:

```javascript
const result = await myQuery.trigger();
console.log('Direct result:', JSON.stringify(result));
console.log('Via .data:', JSON.stringify(myQuery.data));  // Likely null
```

Check Retool's built-in console (not browser console) to see these logs.

---

## Notifications

### Show Notification

```javascript
utils.showNotification({
  title: 'Success',
  description: 'Operation completed',
  notificationType: 'success',  // 'success' | 'error' | 'warning' | 'info'
  duration: 4.5
})
```

### Global Notification Settings

```json
{
  "notificationsSettings": {
    "globalQueryShowFailureToast": true,
    "globalQueryShowSuccessToast": false,
    "globalQueryToastDuration": 4.5,
    "globalToastPosition": "bottomRight"
  }
}
```

---

## Common UI Patterns

### Complete Query Builder Example

A full-featured natural language to SQL interface with saved views, sync, and AI refinement:

**Wireframe:**
```
MAIN PAGE STRUCTURE:
- [Text] appTitle "# Transaction Query Builder" (row 2, col 0, width 10, height 6)
- [Container] syncControlsContainer (row 11, col 0, width 12, height 11)
  - [Button] syncNowButton "Sync Now" (row 1, col 0, width 1, height 5)
  - [Text] lastSyncText "**Last synced:** {{ lastSyncTime.value || 'Never' }}" (row 1, col 1, width 3, height 5)
  - [Text] syncStatusText "{{ syncStatus.value }}" (row 1, col 4, width 4, height 5)
- [Container] savedViewsContainer (row 24, col 0, width 3, height 80)
  - [Text] savedViewsTitle "#### Saved Views" (row 0, col 0, width 12, height 4)
  - [Button] addViewButton "Save Current" (row 4, col 0, width 12, height 5)
  - [Text] savedViewsList "{{ savedViews.value.map(v => `• [${v.name}](javascript:void(0))`).join('\\n') }}" (row 10, col 0, width 12, height 60)
- [Container] queryBuilderContainer (row 24, col 3, width 6, height 80)
  - [Text] queryBuilderTitle "#### Natural Language Query" (row 0, col 0, width 12, height 4)
  - [Text Area] naturalLanguageInput "Describe what you want to query..." (row 5, col 0, width 12, height 8)
  - [Button] generateSQLButton "Generate SQL" (row 14, col 0, width 2, height 5)
  - [Text] sqlExplanationText "#### Generated SQL & Explanation" (row 20, col 0, width 12, height 4)
  - [Text Area] generatedSQLInput "SELECT * FROM transactions LIMIT 10" (row 25, col 0, width 12, height 15)
  - [Text] explanationText "{{ sqlExplanation.value || '_SQL explanation will appear here_' }}" (row 41, col 0, width 12, height 10)
  - [Button] runQueryButton "Run Query" (row 52, col 0, width 2, height 5)
  - [Button] editSQLButton "Edit SQL" (row 52, col 2, width 2, height 5)
- [Container] aiChatContainer (row 24, col 9, width 3, height 80)
  - [Text] aiChatTitle "#### AI Refinement" (row 0, col 0, width 12, height 4)
  - [Text Area] aiRefinementInput "e.g., 'Add a WHERE clause for last month'" (row 11, col 0, width 12, height 8)
  - [Button] refineQueryButton "Refine Query" (row 20, col 0, width 12, height 5)
- [Container] resultsContainer (row 106, col 0, width 12, height 65)
  - [Text] resultsTitle "#### Query Results" (row 0, col 0, width 8, height 5)
  - [Text] resultsCount "{{ queryResults.data ? queryResults.data.length : 0 }} rows" (row 0, col 8, width 4, height 5)
  - [Table] resultsTable "" (row 6, col 0, width 12, height 54)

FRAMES STRUCTURE:
- [Modal Frame] saveViewModal
  - [header]
    - [Text] saveViewModalTitle "#### Save Query View" (row 0, col 0, width 12, height 3)
  - [body]
    - [Text Input] viewNameInput "View name" (row 0, col 0, width 12, height 1)
    - [Text Area] viewDescriptionInput "Description (optional)" (row 3, col 0, width 12, height 5)
  - [footer]
    - [Button] cancelSaveButton "Cancel" (row 0, col 0, width 2, height 5)
    - [Button] confirmSaveButton "Save View" (row 0, col 2, width 2, height 5)
```

**Technical Spec:**
```
stateDiagram-v2

%% Variables
lastSyncTime: "Variable -- stores timestamp of last successful sync"
syncStatus: "Variable -- stores current sync status message"
savedViews: "Variable -- array of saved query views with name, sql, description"
sqlExplanation: "Variable -- stores AI explanation of generated SQL"
currentSQL: "Variable -- stores the current SQL query being worked on"

%% Queries
query1: "GoogleSheetsQuery -- fetches all transaction data from Google Sheets"
createTransactionsTable: "SqlQuery -- creates transactions table in Retool DB if not exists"
syncToRetoolDB: "JavascriptQuery -- syncs Google Sheets data to Retool DB (truncate and insert)"
generateSQLQuery: "JavascriptQuery -- uses AI to convert natural language to SQL"
refineSQL: "JavascriptQuery -- uses AI to refine existing SQL based on user feedback"
queryResults: "SqlQuery -- executes the generated/edited SQL query against Retool DB"
saveViewToStorage: "JavascriptQuery -- saves current query as a named view"
loadViewQuery: "JavascriptQuery -- loads a saved view and populates the interface"

%% Data Flow - Auto Sync on Load
query1 --> syncToRetoolDB : onSuccess
syncToRetoolDB --> lastSyncTime : onSuccess
syncToRetoolDB --> syncStatus : onSuccess
syncToRetoolDB --> queryResults : onSuccess

%% Data Flow - Manual Sync
syncNowButton --> query1 : onClick (trigger)
syncNowButton --> syncStatus : onClick (set "Syncing...")

%% Data Flow - Natural Language to SQL
naturalLanguageInput --> generateSQLQuery
generateSQLButton --> generateSQLQuery : onClick
generateSQLQuery --> generatedSQLInput
generateSQLQuery --> sqlExplanation
generateSQLQuery --> currentSQL

%% Data Flow - SQL Refinement
aiRefinementInput --> refineSQL
currentSQL --> refineSQL
refineQueryButton --> refineSQL : onClick
refineSQL --> generatedSQLInput
refineSQL --> sqlExplanation
refineSQL --> currentSQL

%% Data Flow - Query Execution
generatedSQLInput --> queryResults
runQueryButton --> queryResults : onClick
queryResults --> resultsTable

%% Data Flow - Saved Views
addViewButton --> saveViewModal : onClick (open)
confirmSaveButton --> saveViewToStorage : onClick
saveViewToStorage --> savedViews
saveViewToStorage --> saveViewModal : onSuccess (close)
savedViewsList --> loadViewQuery : onClick links
loadViewQuery --> generatedSQLInput
loadViewQuery --> currentSQL
```

### Three-Column Layout Pattern

For apps with sidebar + main content + auxiliary panel:

```
LAYOUT (12-column grid):
- Sidebar: col 0, width 3 (25%)
- Main content: col 3, width 6 (50%)
- Auxiliary: col 9, width 3 (25%)

Row positioning:
- Header/controls: row 0-20
- Main content area: row 24+
- Use consistent row heights (5 units for buttons, 8 for text areas)
```

### Sync Status Pattern

For apps that sync data from external sources:

```
%% Variables
lastSyncTime: "Variable -- ISO timestamp of last sync"
syncStatus: "Variable -- 'Ready' | 'Syncing...' | 'Synced' | 'Error'"

%% Data Flow
syncButton.onClick --> syncStatus.setValue("Syncing...")
syncButton.onClick --> fetchExternalData.trigger()
fetchExternalData.onSuccess --> syncToLocalDB.trigger()
syncToLocalDB.onSuccess --> lastSyncTime.setValue(new Date().toISOString())
syncToLocalDB.onSuccess --> syncStatus.setValue("Synced")
syncToLocalDB.onFailure --> syncStatus.setValue("Sync failed")
```

### Modal Save/Cancel Pattern

Standard modal with form inputs and action buttons:

```
FRAMES STRUCTURE:
- [Modal Frame] actionModal
  - [header]
    - [Text] modalTitle "#### Modal Title" (row 0, col 0, width 12, height 3)
  - [body]
    - [Text Input] field1 "Field 1" (row 0, col 0, width 12, height 1)
    - [Text Area] field2 "Field 2" (row 3, col 0, width 12, height 5)
  - [footer]
    - [Button] cancelButton "Cancel" (row 0, col 0, width 2, height 5)
    - [Button] confirmButton "Confirm" (row 0, col 2, width 2, height 5)

%% Event Handlers
openButton.onClick --> actionModal.show()
cancelButton.onClick --> actionModal.hide()
confirmButton.onClick --> saveAction.trigger()
saveAction.onSuccess --> actionModal.hide()
saveAction.onSuccess --> refreshData.trigger()
```

### Clickable List with Dynamic Content

For saved items, history, or navigation lists:

```javascript
// In savedViewsList text component value:
{{ savedViews.value && savedViews.value.length > 0
   ? savedViews.value.map(v => `• [${v.name}](javascript:void(0))`).join('\\n')
   : '_No saved items yet_' }}

// Note: Links in markdown text can trigger events via click handlers
```

---

## Best Practices

### Component IDs
- Use descriptive camelCase IDs: `userTable`, `submitButton`, `searchInput`
- Prefix related components: `form1`, `formTitle1`, `formSubmit1`

### Query Naming
- Use action-oriented names: `getUsers`, `saveOrder`, `deleteItem`
- Group related queries: `users_get`, `users_create`, `users_update`

### Event Handling
- Always include error handling in query success/failure events
- Chain queries using `.trigger()` in success handlers
- Use confirmation for destructive actions

### Layout
- Use containers for logical grouping
- Leverage the 12-column grid system
- Set appropriate height types (auto for content, fixed for inputs)

### Performance
- Set `runWhenPageLoads: true` only for essential queries
- Use `runWhenModelUpdates: false` to prevent unnecessary triggers
- Implement pagination for large datasets

---

## Transit Structure Validation

### Plugin Footer Requirements

Every plugin (query, widget, screen, frame) MUST have the complete footer fields `^1A` through `^1L`. These are the last fields in the v-map before the plugin's closing brackets.

Key fields:
| Field | Meaning | Typical Value |
|-------|---------|---------------|
| `^1A` | style | `["^1M", []]` for widgets; null for queries |
| `^1B` | position2 | Grid position wrapper for widgets; null for queries |
| `^1C`–`^1E` | mobile/tab metadata | null |
| `^1F` | container | `"$main"` |
| `^7` | createdAt | `"~m1769620000000"` |
| `^1G` | updatedAt | `"~m1769620000000"` |
| `^1H` | folder | `""` |
| `^1I` | presetName | null |
| `^1J` | **screen (page assignment)** | `"page1"` |
| `^1K`, `^1L` | boxId, subBoxIds | null |

### Common Structural Bugs

#### 1. "Record type named undefined" on Import

**Symptom**: Retool shows "Failed import — Tried to deserialize Record type named 'undefined'"

**Cause**: The appState was built from scratch (or copied from another format) and doesn't match the Transit cache slot assignments that Retool's reader expects. Specifically:
- Missing `["^0", ["^ ", "n", "pluginTemplate", "v", [...]]]` outer wrapper
- Plugin data wrapped in double array `[["^0", [...]]]` instead of `["^0", [...]]`
- Literal string keys (`"uuid"`, `"type"`) instead of cache refs (`"^19"`, `"^1;"`)

**Fix**: Always build from a real Retool-exported file using Python. Never construct appState as a string or from scratch.

#### 2. Bracket Imbalance (Extra Data Error)

**Symptom**: `json.JSONDecodeError: Extra data: line 1 column XXXXX (char XXXXX)`

**Cause**: The appState string has more `]` than `[`. Usually from copy-paste errors or manual editing.

**Diagnosis**:
```python
app_state = outer['page']['data']['appState']
opens = app_state.count('[')
closes = app_state.count(']')
print(f"Balance: {opens - closes}")  # Must be 0
```

**Fix**: Parse the file with `json.loads`, navigate to the imbalanced plugin using the Python structure, and correct it there. Never edit the raw JSON string.

#### 3. Plugin Not Visible After Import

**Symptom**: Import succeeds but some widgets/queries are missing in the app.

**Cause**: Plugin's `^1J` (screen assignment) is null or wrong, OR the plugin was accidentally nested inside another plugin's data during manual editing.

**Check**: Verify each plugin's `^1J` field is set to the correct page ID (`"page1"` etc.).

### Validation Script

Use this Python script to validate Transit structure before import. It uses JSON parsing (not regex) to navigate the actual structure:

```python
import json

def validate_retool_json(filepath):
    with open(filepath) as f:
        outer = json.load(f)

    # Check 1: outer JSON structure
    app_state = outer['page']['data']['appState']
    print("[1] Outer JSON: VALID")

    # Check 2: appState is valid JSON
    try:
        transit = json.loads(app_state)
        print("[2] appState JSON: VALID")
    except json.JSONDecodeError as e:
        print(f"[2] CRITICAL: appState is not valid JSON: {e}")
        return False

    # Check 3: Transit root
    assert transit[0] == '~#iR', f"Expected ~#iR root, got {transit[0]}"
    print("[3] Transit root ~#iR: OK")

    # Find plugins iOM
    def find_iom(obj, depth=0):
        if depth > 10: return None
        if isinstance(obj, list):
            if len(obj) >= 2 and obj[0] == '~#iOM':
                return obj[1]
            for item in obj:
                r = find_iom(item, depth+1)
                if r: return r
        return None

    plugins_list = find_iom(transit)
    assert plugins_list, "Could not find ~#iOM plugins map"
    plugin_count = (len(plugins_list) - 1) // 2
    print(f"[4] Plugins iOM: OK ({plugin_count} plugins)")

    # Check 5: Each plugin wrapper format and bracket balance
    errors = []
    print("[5] Per-plugin checks:")
    for i in range(1, len(plugins_list), 2):
        pid = plugins_list[i]
        pdata = plugins_list[i+1]
        pjson = json.dumps(pdata)

        # Wrapper format
        if not (isinstance(pdata, list) and len(pdata) == 2 and pdata[0] == '^0'):
            errors.append(f"{pid}: Wrong wrapper — expected ['^0', [...]]")
            print(f"  {pid}: ✗ WRONG WRAPPER FORMAT")
            continue

        inner = pdata[1]
        has_n_v = isinstance(inner, list) and 'n' in inner and 'v' in inner
        if not has_n_v:
            errors.append(f"{pid}: Missing n/v wrapper inside ^0 record")
            print(f"  {pid}: ✗ MISSING n/v WRAPPER")
            continue

        # Bracket balance per plugin
        opens = pjson.count('[')
        closes = pjson.count(']')
        bal = opens - closes
        bal_str = "✓" if bal == 0 else f"✗ IMBALANCED ({bal:+d})"

        # Footer fields
        has_1j = '"^1J"' in pjson
        has_1l = '"^1L"' in pjson
        footer_str = "✓" if (has_1j and has_1l) else "✗ MISSING FOOTER"

        print(f"  {pid}: brackets={bal_str}, footer={footer_str}")

        if bal != 0:
            errors.append(f"{pid}: Bracket imbalance {bal:+d}")
        if not has_1j or not has_1l:
            errors.append(f"{pid}: Missing footer fields")

    print()
    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
        return False

    print("✓ Transit structure validated successfully")
    print(f"  File size: {len(json.dumps(outer))} bytes")
    return True

# Usage
validate_retool_json('apps/Time on site 2/samsara_trips_report.json')
```

---

## File Generation Checklist

When generating a Retool app JSON:

**Structure (mandatory)**:
1. [ ] **Started from a real Retool-exported file as base — NEVER built appState from scratch**
2. [ ] Built by Python-modifying the base file, not string concatenation
3. [ ] `json.loads(outer_json)` succeeds
4. [ ] `json.loads(app_state)` succeeds — appState is valid JSON
5. [ ] Each plugin follows `["^0", ["^ ", "n", "pluginTemplate", "v", [...]]]` wrapper format
6. [ ] Each plugin's v-map has all footer fields `^1A` through `^1L`
7. [ ] Bracket balance = 0 for every individual plugin (not just global total)
8. [ ] All components have unique IDs

**Content**:
9. [ ] Queries defined before components that reference them
10. [ ] Event handlers have valid target IDs
11. [ ] Position2 values create valid layout (row, col, height, width)
12. [ ] Container references point to existing frame IDs
13. [ ] Screen/page assignment (`^1J`) set to correct page ID
14. [ ] No comments in JSON (invalid syntax)

**Widget-specific**:
15. [ ] TableWidget2 uses `_columnIds` + separate maps (not `columns` array)
16. [ ] Table cell expressions use `currentSourceRow` (not `currentRow`)
17. [ ] DateRangePickerWidget: `.startDate` / `.endDate` properties
18. [ ] MultiselectWidget2: `.value` returns array
