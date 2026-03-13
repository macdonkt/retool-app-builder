# Retool App Builder — Reference-Driven Process

Build production-ready Retool apps from natural language instructions. Output valid JSON files for direct import into Retool.

## Current Project

**Active project folder**: `apps/`
**Reference files**: `refs/` folder (widget catalog, components example, verified patterns)

### Scoping Rules
- **ONLY read/write files inside the active project folder** listed above
- **Reference docs** (this file, `RETOOL_JSON_REFERENCE.md`, and `refs/`) are always in scope
- **Always read references before building** — never write widget/query templates from memory

## Core Principle: Reference-First Build

**NEVER write widget or query template fields from memory.** Instead:
1. Read the exact field structure from `tools/transit_patterns.json` for the component type
2. Copy ALL fields verbatim into a `tom()` call
3. Change ONLY the fields that need to differ (text, value, data, events, position)
4. Validate against the golden reference after each step

This eliminates the entire class of "missing field" bugs.

## Reference Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `refs/widget_catalog.md` | Quick lookup: 95 widget types + key fields | Before choosing components |
| `tools/transit_patterns.json` | Full field structures for every component | Before writing ANY template |
| `refs/components example.json` | Real Retool export (ground truth) | When checking Transit encoding |
| `refs/verified_patterns/*.md` | Working patterns from successful imports | Before building a pattern you've used before |
| `RETOOL_JSON_REFERENCE.md` | Transit encoding rules, positioning, app structure | When unsure about encoding rules |

## Build Library

**`tools/retool_core.py`** — Slim Transit primitives only. No template factories.

### Available Functions

**Transit encoding:**
- `tmap(k1, v1, k2, v2, ...)` — Transit map (plain JS object, NO `.get()`)
- `tom(k1, v1, k2, v2, ...)` — Ordered map (HAS `.get()`, required for templates & events)
- `tlist([...])` — Transit list (HAS `.toArray()`, required for _columnIds, events, etc.)
- `record(name, value)` — Transit record wrapper

**Positioning:**
- `pos(row, col, height, width, container, screen, row_group)` — Grid position

**Plugin builders (generic wrappers):**
- `widget(id, subtype, template_tom, position, container, screen)` — Any widget
- `query(id, subtype, template_tom, resource_uuid, resource_name, screen)` — Any query
- `state_var(id, value, screen)` — State variable
- `screen_plugin(id, title, slug, order)` — Page/screen
- `frame_plugin(id, screen_id, frame_type)` — Main content frame
- `modal_plugin(id, screen_id, size)` — Modal frame
- `drawer_plugin(id, screen_id, width)` — Drawer frame

**Event helpers:**
- `evt(event_type, src)` — Run JS code
- `evt_trigger_query(event_type, query_id)` — Trigger a query
- `evt_show_frame(event_type, frame_id)` — Show modal/drawer
- `evt_hide_frame(event_type, frame_id)` — Hide modal/drawer
- `evt_set_var(event_type, var_id, value_expr)` — Set state variable
- `evt_notification(event_type, notif_type, title, description, duration)` — Toast notification

**App assembly:**
- `build_app(plugins_list)` — Assemble all plugins into appState
- `save_app(app_state, output_path, app_name)` — Write to JSON file

## Transit Encoding Rules (Critical)

| What | Encoding | Python | Why |
|------|----------|--------|-----|
| Widget/query templates | Ordered Map | `tom()` | Retool calls `.get()` on templates |
| Event handlers | Ordered Map | `tom()` | Retool calls `.get()` on events |
| `events` field | Transit List | `tlist([])` | Retool calls `.toArray()` |
| `_columnIds` | Transit List | `tlist([...])` | Retool calls `.toArray()` |
| `_actionIds` | Transit List | `tlist([])` | Retool calls `.toArray()` |
| `_toolbarButtonIds` | Transit List | `tlist([...])` | Retool calls `.toArray()` |
| `_groupByColumns` | Transit List | `tlist([])` | Retool calls `.toArray()` |
| Widget `style` | Ordered Map | `tom()` | Empty ordered map |
| Screen `style` | null | `None` | Screens don't have styles |
| Query `style` | null | `None` | Queries don't have styles |

## Build Process (Step-by-Step)

### Phase 1: Discovery
1. **Clarify requirements** — What does the app do? What data sources?
2. **Design UI wireframe** — Text-based component map (see Wireframe Format below)

### Phase 2: Specification
3. **Create technical spec** — Variables, queries, components, data flows
4. **Build implementation plan** — Ordered steps, one component at a time

### Phase 3: Implementation (Reference-Driven)

For EACH build step:

```
1. READ refs/widget_catalog.md
   → Identify which component types are needed

2. READ tools/transit_patterns.json
   → Get the EXACT field structure for each component type
   → Copy ALL fields — do not skip any

3. READ refs/verified_patterns/*.md
   → Check if this pattern has been verified before
   → Follow the verified structure exactly

4. WRITE build script using ONLY:
   - tools/retool_core.py primitives
   - Field values COPIED from transit_patterns.json
   - Modify only: id, text, value, data, events, position

5. RUN the build script
   → Generate stepN.json

6. RUN validator with --golden flag:
   python3 tools/validate_retool_json.py --golden apps/stepN.json
   → Check structural validity
   → Compare against golden reference

7. USER imports to Retool
   → Confirms it works

8. ON SUCCESS: save a verified pattern file
   → refs/verified_patterns/pattern_name.md
```

### Phase 4: Review
9. **Validate** — Run validator with `--golden` flag
10. **Review with user** — Confirm implementation meets requirements

## Validation

### Standard Validation
```bash
python3 tools/validate_retool_json.py apps/my-app.json
```
Checks: outer structure, appState parsing, Transit records, plugins, positions, duplicates.

### Golden Reference Comparison
```bash
python3 tools/validate_retool_json.py --golden apps/my-app.json
```
Additionally checks: template field names vs transit_patterns.json, Transit encoding types (tlist vs array).

## Output Format

Save all generated files to the active project folder.

1. **Primary**: `apps/{app-name}.json` — Clean, valid JSON ready for Retool import
2. **Secondary** (when needed): `apps/{app-name}-instructions.md` — Setup documentation
3. **Build script**: `apps/build_{app-name}.py` — The Python script that generates the JSON

## Knowledge Accumulation

After each successful import, create a verified pattern file:

```
refs/verified_patterns/{pattern_name}.md
```

Include:
- Component types used and their key field values
- Event handler structures that imported successfully
- Any gotchas or edge cases discovered
- The exact build script call that worked

Over time, this builds a library of verified structures that can be used to build a comprehensive programmatic builder.

## Critical Rules

- **Never write template fields from memory** — Always read transit_patterns.json first
- **Never edit production apps directly** — Always duplicate for testing
- **Validate JSON before import** — Run validator with `--golden` flag
- **Copy ALL fields** — Missing fields cause import errors
- **Use correct Transit encoding** — tom() for templates/events, tlist() for array fields

## Wireframe Format

Before building, create a text wireframe mapping every component:

```
MAIN PAGE STRUCTURE:
- [Text] appTitle "# App Title" (row 2, col 0, width 10, height 6)
- [Button] actionButton "Action" (row 2, col 10, width 2, height 5)
- [Table] dataTable "" (row 8, col 0, width 12, height 40)

FRAMES STRUCTURE:
- [Modal Frame] editModal
  - [header]
    - [Text] modalTitle "#### Edit Item" (row 0, col 0, width 12, height 3)
  - [body]
    - [Text Input] nameInput "Name" (row 0, col 0, width 12, height 7)
  - [footer]
    - [Button] cancelButton "Cancel" (row 0, col 0, width 2, height 5)
    - [Button] saveButton "Save" (row 0, col 2, width 2, height 5)
```

Format: `[WidgetType] componentId "label/placeholder" (row, col, width, height)`

### Component Type Abbreviations
| Notation | Widget Type |
|----------|-------------|
| `[Text]` | TextWidget2 |
| `[Button]` | ButtonWidget2 |
| `[TextInput]` | TextInputWidget2 |
| `[TextArea]` | TextAreaWidget |
| `[Select]` | SelectWidget2 |
| `[Table]` | TableWidget2 |
| `[Container]` | ContainerWidget2 |
| `[Modal]` | ModalFrameWidget |
| `[Form]` | FormWidget2 |
| `[Tabs]` | TabsWidget2 |

## Technical Spec Format

```
stateDiagram-v2

%% Variables
selectedItem: "Variable -- currently selected item"

%% Queries
fetchData: "JavascriptQuery -- fetches mock data"

%% UI Components
dataTable: "Table -- displays data from fetchData"
addButton: "Button -- opens add modal"

%% Data Flow
addButton --> addModal : onClick (show)
fetchData --> dataTable : binds via {{ fetchData.data }}
```

## Workflow Dependencies

Retool Workflows cannot be included in app JSON exports. When needed:
1. **In the JSON**: Include queries that reference the workflow by name
2. **In instructions.md**: Provide step-by-step setup for creating the workflow

## State Management

Use `state_var()` for app-level state:
- Sync timestamps, status messages, saved configurations
- Computed results, current selections

## Requirements Gathering

Before building, clarify:
1. **Purpose**: Dashboard, form, reporting, automation?
2. **Data Sources**: Databases, APIs, sample columns?
3. **UI Components**: Tables, forms, charts, modals?
4. **Interactions**: Buttons, validation, conditional logic?
5. **Integrations**: AI, external APIs, workflows?
