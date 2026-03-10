# Retool App Builder

Build production-ready Retool apps from natural language instructions. Output valid JSON files for direct import into Retool.

## Current Project

<!-- UPDATE THIS SECTION each time you start a new build project -->
**Active project folder**: `apps/Time on site 2/`
**Reference files (if any)**: None — use only CLAUDE.md and RETOOL_JSON_REFERENCE.md

### Scoping Rules
- **ONLY read/write files inside the active project folder** listed above
- **NEVER explore or read** JSON files outside the active project folder — they are old builds and irrelevant
- **Reference docs** (this file + `RETOOL_JSON_REFERENCE.md`) are always in scope
- When the user drops a reference JSON into the active project folder, use it as a structural example
- The `.claudeignore` file enforces this at the file-discovery level, but follow these rules even if a file is technically visible

## Output Format

Save all generated files to the active project folder (e.g., `apps/Time on site 2/`).

When building apps, always output:

1. **Primary**: `apps/{app-name}.json` - Clean, valid JSON ready for Retool import
   - No comments (JSON doesn't support them)
   - Complete app structure: components, queries, event handlers, pages, modules
   - Standard components only unless custom components are specified

2. **Secondary** (when needed): `apps/{app-name}-instructions.md` - Setup documentation for:
   - Workflow creation steps (workflows can't be included in app JSON)
   - Resource/data source configuration
   - External dependencies or permissions
   - Post-import configuration steps

If no workflows or external setup is needed, output only the JSON.

## Critical Rules

- **Never edit production apps directly** - Always duplicate for testing
- **Validate JSON before import** - Ensure structure is complete and valid
- **Avoid legacy components** - Use current components for security/features
- **Handle errors** - Include error states in event handlers
- **Test with sample data** - Verify bindings work before deployment

## Resources

- **JSON Reference**: See `RETOOL_JSON_REFERENCE.md` for complete technical specs (Transit encoding, widget templates, query types, positioning, event handlers)
- **Retool Docs**: https://docs.retool.com
- **LLM-Optimized Docs**: https://docs.retool.com/llms.txt
- **Retool CLI**: https://github.com/tryretool/retool-cli (export/import apps)
- **Components**: 100+ UI elements (tables, forms, charts, inputs, modals, etc.)
- **Queries**: REST, GraphQL, SQL/NoSQL, JavaScript transformers, AI integrations

**Important**: Always consult `RETOOL_JSON_REFERENCE.md` when planning and building apps for correct JSON structure, widget types, and Transit encoding format.

## App Patterns

### CRUD Dashboard
Table + forms for data management with filters, modals, and actions.

**Example request**:
"Generate a Retool app JSON for a product management dashboard:
- Table showing products from `get_products` query (columns: id, name, price, stock)
- Filters for name search and price range
- Add/Edit modals with form validation
- Delete button with confirmation
- Success notifications and refresh functionality"

### Form with Validation
Input collection with validation rules, submission handling, and feedback.

**Example request**:
"Generate a Retool app JSON for a customer feedback form:
- Text input (name), email input, textarea (feedback), rating selector (1-5)
- Validation: required fields, email format check
- Submit triggers `submit_feedback` query
- Success toast and form reset on completion"

### AI Integration
User input processed by LLM with results display and history tracking.

**Example request**:
"Generate a Retool app JSON for an AI text analyzer:
- Textarea for user input
- Button triggers `analyze_text` AI query for sentiment/keywords
- Results displayed in formatted text component
- Loading states and error handling
- History table from `get_history` query"

### Multi-Page App
Navigation between pages with URL params for state management.

### Mobile App
Native mobile components with camera, GPS, offline support.

## Build Process (Step-by-Step)

For complex apps, follow this structured workflow:

### Phase 1: Discovery
1. **Find/set up resources** - Identify existing database connections, APIs, or create new tables in Retool DB
2. **Design UI wireframe** - Create a text-based component map before writing JSON

### Phase 2: Specification
3. **Create technical spec** - Document variables, queries, components, and data flows
4. **Build implementation plan** - Break down into discrete, ordered tasks

### Phase 3: Implementation
5. **Create database tables** - Set up Retool DB tables with proper schemas
6. **Create state variables** - Define app-level variables for state management
7. **Create queries** - Build all data fetching and mutation queries
8. **Build UI from wireframe** - Implement components following the wireframe
9. **Wire data bindings** - Connect components to queries and variables
10. **Set up event handlers** - Configure all interactions and query chains

### Phase 4: Review
11. **Validate structure** - Run Transit validation script
12. **Review with user** - Confirm implementation meets requirements

### Wireframe Format

Before building, create a text wireframe mapping every component. Use `-` for list items and indentation for nesting:

```
MAIN PAGE STRUCTURE:
- [Text] appTitle "# App Title" (row 2, col 0, width 10, height 6)
- [Container] controlsContainer (row 11, col 0, width 12, height 11)
  - [Button] actionButton "Action" (row 1, col 0, width 1, height 5)
  - [Text] statusText "{{ status.value }}" (row 1, col 1, width 3, height 5)
- [Container] sidebarContainer (row 24, col 0, width 3, height 80)
  - [Text] sidebarTitle "#### Sidebar" (row 0, col 0, width 12, height 4)
  - [Button] addButton "Add New" (row 4, col 0, width 12, height 5)
  - [Text] listItems "{{ items.value.map(i => `• ${i.name}`).join('\\n') }}" (row 10, col 0, width 12, height 60)
- [Container] mainContainer (row 24, col 3, width 9, height 80)
  - [Text Area] inputArea "Enter content..." (row 5, col 0, width 12, height 8)
  - [Button] submitButton "Submit" (row 14, col 0, width 2, height 5)
  - [Table] resultsTable "" (row 20, col 0, width 12, height 54)

FRAMES STRUCTURE:
- [Modal Frame] editModal
  - [header]
    - [Text] modalTitle "#### Edit Item" (row 0, col 0, width 12, height 3)
  - [body]
    - [Text Input] nameInput "Name" (row 0, col 0, width 12, height 1)
    - [Text Area] descInput "Description" (row 3, col 0, width 12, height 5)
  - [footer]
    - [Button] cancelButton "Cancel" (row 0, col 0, width 2, height 5)
    - [Button] saveButton "Save" (row 0, col 2, width 2, height 5)
```

Format: `[WidgetType] componentId "label/placeholder" (row, col, width, height)`

**Notes:**
- Use markdown in text values: `"# Heading"`, `"#### Subheading"`, `"**bold**"`
- Include dynamic bindings: `"{{ variable.value }}"`
- Modal frames have header/body/footer sections
- Heights are in row units (5 = standard button height)

### Technical Spec Format

Document the app architecture before implementation using this state diagram format:

```
stateDiagram-v2

%% Variables
lastSyncTime: "Variable -- stores timestamp of last successful sync"
syncStatus: "Variable -- stores current sync status message"
savedItems: "Variable -- array of saved items with name, config"
currentValue: "Variable -- stores the current working value"

%% Queries
fetchData: "RESTQuery -- fetches data from external API"
syncToDatabase: "JavascriptQuery -- syncs external data to Retool DB"
processWithAI: "JavascriptQuery -- uses AI to process user input"
executeAction: "SqlQuery -- executes the generated action against Retool DB"
saveToStorage: "JavascriptQuery -- saves current state to variable"

%% UI Components - Controls
actionButton: "Button -- triggers main action"
statusText: "Text -- displays current status"

%% UI Components - Input
userInput: "Text Area -- user enters input"
submitButton: "Button -- triggers processing"
outputDisplay: "Text Area -- displays processed output"

%% UI Components - Results
resultsTable: "Table -- displays results"
resultsCount: "Text -- shows count of results"

%% Data Flow - Auto Load
fetchData --> syncToDatabase : onSuccess
syncToDatabase --> lastSyncTime : onSuccess
syncToDatabase --> syncStatus : onSuccess

%% Data Flow - User Action
userInput --> processWithAI
submitButton --> processWithAI : onClick
processWithAI --> outputDisplay
processWithAI --> currentValue

%% Data Flow - Execution
outputDisplay --> executeAction
runButton --> executeAction : onClick
executeAction --> resultsTable
executeAction --> resultsCount

%% Data Flow - Save/Load
saveButton --> saveToStorage : onClick
currentValue --> saveToStorage
saveToStorage --> savedItems
savedItems --> itemsList
itemsList --> loadItem : onClick
loadItem --> userInput
loadItem --> currentValue
```

**Spec Sections:**
- `%% Variables` - State slots with descriptions
- `%% Queries` - All queries with type and purpose
- `%% UI Components - [Group]` - Components organized by function
- `%% Data Flow - [Feature]` - How data moves through the app

## Requirements Gathering

Before building, clarify these details:

1. **Purpose**: What does the app do? (dashboard, form, reporting, automation)
   - Web, mobile, or both?
   - Specific pattern preference?

2. **Data Sources**:
   - What databases/APIs? (Postgres, REST, Google Sheets, etc.)
   - Key queries needed? (fetch, create, update, delete)
   - Sample columns/fields?

3. **UI Components**:
   - Main components? (tables, forms, charts, modals)
   - Layout structure? (single page, multi-page, modules)
   - Mobile-specific features?

4. **Interactions**:
   - User actions and buttons?
   - Validation rules?
   - Conditional logic? (show/hide based on role/state)

5. **Integrations**:
   - AI/LLM features?
   - External APIs or notifications?
   - Retool Workflows needed?

6. **Testing**:
   - Sample data available?
   - Edge cases to handle?

## Workflow Dependencies

Retool Workflows are separate backend automations - they cannot be included in app JSON exports.

When an app requires workflows:

1. **In the JSON**: Include queries that reference the workflow by name
2. **In the instructions markdown**: Provide step-by-step setup:
   - Navigate to Retool Workflows in UI
   - Create workflow matching the referenced name
   - Configure triggers (HTTP, schedule, etc.)
   - Add action blocks (queries, JS/Python code, branches)
   - Set inputs/outputs to match app query parameters
   - Test integration and verify in workflow logs

Common workflow triggers: form submissions, scheduled syncs, external webhooks, complex multi-step automations.

## State Management

### App-Level Variables

Use Retool variables (state slots) for:
- **Sync timestamps**: Track when data was last refreshed
- **Status messages**: Display current operation state to users
- **Saved configurations**: Store user preferences, saved views, filter states
- **Computed results**: Cache expensive calculations or AI-generated content
- **Current selections**: Track selected items across components

### Variable Naming Convention

```
lastSyncTime      — timestamps
syncStatus        — status/progress messages
savedViews        — arrays of saved configurations
currentSQL        — current working values
sqlExplanation    — AI/computed explanations
selectedRecord    — current selection state
```

### Query Chaining Patterns

Document data flows explicitly:

```
%% Auto Sync on Load
fetchData → syncToDatabase.onSuccess
syncToDatabase → lastSyncTime (update on success)
syncToDatabase → syncStatus (update on success)
syncToDatabase → refreshTable (trigger on success)

%% User Action Flow
userInput → generateQuery.onClick
generateQuery → generatedOutput (on success)
generateQuery → explanationText (on success)
executeButton → runQuery.onClick
runQuery → resultsTable (on success)
```

## Technical Notes

**Data Binding**:
- Use `{{ }}` for dynamic values
- Access query data: `queryName.data`
- Ensure queries run before components bind to them

**JSON Export Limitations**:
- Runtime state may not persist
- Custom components must exist in target instance
- Very new features may lag in export support

**Mobile Considerations**:
- Platform-specific permissions required
- Test with Retool Mobile preview
- Hardware integrations (camera, GPS) need explicit setup

**Performance**:
- Use query caching for frequently accessed data
- Implement server-side pagination for large datasets
- Monitor AI/LLM usage costs

## Wireframe Component Notation

When creating wireframes, use this detailed notation for each component:

### Basic Format
```
[WidgetType] componentId "visible text/label" (row X, col Y, width W, height H)
```

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

### Nested Components
Indent children under their parent container:
```
[Container] mainContainer (row 0, col 0, width 12, height 8)
  [Text] title "Dashboard" (row 0, col 0, width 6, height 1)
  [Button] refreshBtn "Refresh" (row 0, col 10, width 2, height 1)
  [Table] dataTable (row 1, col 0, width 12, height 6)
```

### Special Annotations
```
[Modal] editModal "Edit Record" (hidden)     ← starts hidden
[Button] deleteBtn "Delete" (danger)          ← danger style variant
[TextInput] emailInput (required, email)      ← validation rules
[Container] adminSection (hidden: !isAdmin)   ← conditional visibility
```

### Frame Structure
```
FRAMES STRUCTURE:
- [Main frame] $main
  - Components in main content area
- [Header frame] $header (optional)
  - App title, navigation
- [Modal] modalName (hidden)
  - Modal content
```
