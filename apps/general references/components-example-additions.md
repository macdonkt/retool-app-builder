# Components Example App — Additions Checklist

Step-by-step instructions for adding missing patterns to the components example app in Retool, then re-exporting. Each section has the exact component to modify, where to click, and what values to enter.

---

## 1. Query Event Handlers

### 1A. exampleGlobalSqlQuery — Add onSuccess + onFailure

**Add onSuccess handler:**
1. Open the app in Retool editor
2. In the left panel under **Queries**, click `exampleGlobalSqlQuery`
3. At the bottom of the query editor, find the **Event handlers** section
4. Click **+ Add event handler**
5. Configure:
   - **Event**: `Success`
   - **Action**: `Control component`
   - **Component**: select `exampleGlobalNone` (the state variable)
   - **Method**: `setValue`
   - **Value**: `{{ exampleGlobalSqlQuery.data }}`
6. Click **+ Add event handler** again for a second success handler
7. Configure:
   - **Event**: `Success`
   - **Action**: `Show notification`
   - **Title**: `SQL query complete`
   - **Description**: `Fetched {{ exampleGlobalSqlQuery.data.length }} rows`
   - **Type**: `Success`

**Add onFailure handler:**
1. Click **+ Add event handler**
2. Configure:
   - **Event**: `Failure`
   - **Action**: `Show notification`
   - **Title**: `SQL query failed`
   - **Description**: `{{ exampleGlobalSqlQuery.error }}`
   - **Type**: `Error`
   - **Duration (seconds)**: `6`

---

### 1B. ExampleGlobalRestQuery — Add Body + onSuccess + onFailure

**Add a request body (change to POST):**
1. Click `ExampleGlobalRestQuery` in the Queries panel
2. Change the **Method** dropdown from `GET` to `POST`
3. Below the URL field, click the **Body** tab
4. Select body type: **JSON**
5. Enter this example body:
```json
{
  "tagIds": [1234, 5678],
  "startTime": "{{ moment().subtract(7, 'days').toISOString() }}",
  "endTime": "{{ moment().toISOString() }}"
}
```

**Add onSuccess handler:**
1. Scroll to **Event handlers** section
2. Click **+ Add event handler**
3. Configure:
   - **Event**: `Success`
   - **Action**: `Trigger query`
   - **Query**: select `exampleGlobalJsQuery`

**Add onFailure handler:**
1. Click **+ Add event handler**
2. Configure:
   - **Event**: `Failure`
   - **Action**: `Show notification`
   - **Title**: `API request failed`
   - **Description**: `{{ ExampleGlobalRestQuery.error }}`
   - **Type**: `Error`

---

### 1C. exampleGlobalJsQuery — Add onFailure

This query already has 2 onSuccess handlers. Just add a failure handler:

1. Click `exampleGlobalJsQuery` in the Queries panel
2. Scroll to **Event handlers**
3. Click **+ Add event handler**
4. Configure:
   - **Event**: `Failure`
   - **Action**: `Show notification`
   - **Title**: `JavaScript error`
   - **Description**: `{{ exampleGlobalJsQuery.error }}`
   - **Type**: `Error`
   - **Duration (seconds)**: `6`

---

### 1D. llmChat1_query1 (RetoolAIQuery) — Fill in Prompt + Add onSuccess

**Fill in the prompt and instruction:**
1. Click `llmChat1_query1` in the Queries panel (it may be nested under the llmChat1 widget)
2. In the **Prompt** field, enter:
```
Summarize the following data in 3 bullet points: {{ JSON.stringify(exampleGlobalSqlQuery.data) }}
```
3. In the **System Instructions** field (may be labeled "Instruction" or "System prompt"), enter:
```
You are a helpful data analyst. Always respond with clear, concise bullet points. Use numbers and percentages when possible.
```

**Add onSuccess handler:**
1. Scroll to **Event handlers**
2. Click **+ Add event handler**
3. Configure:
   - **Event**: `Success`
   - **Action**: `Control component`
   - **Component**: select `exampleGlobalNone`
   - **Method**: `setValue`
   - **Value**: `{{ llmChat1_query1.data }}`

---

### 1E. agentChat1_query1 (RetoolAIAgentInvokeQuery) — Optional

Only do this if you have a Retool AI Agent configured:
1. Click `agentChat1_query1`
2. Select an agent from the **Agent** dropdown
3. Fill in the query/prompt field

If no agent is available, skip this — the generic `query()` builder function handles it.

---

## 2. Widget onChange Events

### 2A. textInput1 — onChange → setValue

1. In the canvas, click on `textInput1` (or find it in the component tree)
2. In the right **Inspector** panel, scroll to **Event handlers**
3. Click **+ Add event handler**
4. Configure:
   - **Event**: `Change` (this is the onChange event)
   - **Action**: `Control component`
   - **Component**: select `exampleGlobalNone`
   - **Method**: `setValue`
   - **Value**: `{{ textInput1.value }}`

---

### 2B. select1 — onChange → Trigger Query

1. Click on `select1` in the canvas
2. In the **Inspector** panel, scroll to **Event handlers**
3. Click **+ Add event handler**
4. Configure:
   - **Event**: `Change`
   - **Action**: `Trigger query`
   - **Query**: select `exampleGlobalSqlQuery`

---

### 2C. numberInput1 — onChange → setValue

1. Click on `numberInput1` in the canvas
2. In the **Inspector** panel, scroll to **Event handlers**
3. Click **+ Add event handler**
4. Configure:
   - **Event**: `Change`
   - **Action**: `Control component`
   - **Component**: select `exampleGlobalNone`
   - **Method**: `setValue`
   - **Value**: `{{ numberInput1.value }}`

---

### 2D. date1 — onChange → Trigger Query

1. Click on `date1` in the canvas
2. In the **Inspector** panel, scroll to **Event handlers**
3. Click **+ Add event handler**
4. Configure:
   - **Event**: `Change`
   - **Action**: `Trigger query`
   - **Query**: select `exampleGlobalSqlQuery`

---

### 2E. modalFrame1 — onClose → Clear State

1. Click on the modal frame `modalFrame1` (you may need to show it first by clicking its name in the component tree)
2. In the **Inspector** panel, find **Event handlers**
3. Click **+ Add event handler**
4. Configure:
   - **Event**: `Close`
   - **Action**: `Control component`
   - **Component**: select `exampleGlobalNone`
   - **Method**: `setValue`
   - **Value**: `""`  (empty string to clear)

---

### 2F. Add a Button with Open URL Action

1. Find `button4` in the canvas (or any button on page2)
2. In the **Inspector** panel, scroll to **Event handlers**
3. Click **+ Add event handler** (or edit existing)
4. Configure:
   - **Event**: `Click`
   - **Action**: `Open URL`
   - **URL**: `https://docs.retool.com`
   - **Open in**: `New tab`

If button4 already has a click handler, add this as a second handler, or use a different button.

---

## 3. State Variable Additions

### 3A. Add a Number State Variable

1. In the left panel, click the **+** button next to **State** (or right-click the State section)
2. Click **Add state variable**
3. Name it: `exampleNumberState`
4. In the **Default value** field, enter: `0`
5. Make sure it's **Global** (not page-scoped) — it should appear under the Global section, not under a specific page

---

### 3B. Add an Array State Variable

1. Add another state variable
2. Name it: `exampleArrayState`
3. In the **Default value** field, enter: `[]`
4. Keep it **Global**

---

### 3C. Add an Object State Variable

1. Add another state variable
2. Name it: `exampleObjectState`
3. In the **Default value** field, enter: `{}`
4. Keep it **Global**

---

### 3D. Verify Page-Scoped State Variable

The app already has `examplePageNone` which should be page-scoped. Verify:
1. Check that `examplePageNone` appears under **Page 1** (not under Global)
2. If it's global, drag it into a page scope, or create a new one:
   - Navigate to **Page 2**
   - Add a state variable named `examplePage2State`
   - Set default value to: `"page2 default"`
   - Ensure it appears under Page 2's scope

---

## 4. Table Column Visual Customization

### 4A. Add Conditional Column Text Color

1. Click on `table1` in the canvas
2. In the **Inspector** panel, find the **Columns** section
3. Click on the **name** column (or any text column)
4. Look for **Text color** or **Color** setting (may be under "Format" or "Style")
5. Click the code toggle (fx) to switch to dynamic mode
6. Enter:
```
{{ currentSourceRow.name === 'test' ? '#e53e3e' : '#2d3748' }}
```
This makes rows where name = "test" show red text, others dark gray.

---

### 4B. Add Conditional Row Background Color

1. Still in `table1` inspector
2. Look for **Row color** or **Row background** setting (may be at the table level, not column level — check under "Styles" or "Row settings")
3. Click the code toggle (fx) to switch to dynamic mode
4. Enter:
```
{{ currentSourceRow.id === 1 ? '#fff5f5' : '' }}
```
This highlights the first row with a light red background.

---

## 5. Query Chaining Pattern

This wires up a complete chain: button → query → [3 success handlers + 1 failure handler].

### 5A. Create a New JavaScript Query for the Chain

1. In the Queries panel, click **+** → **JavaScript Query**
2. Name it: `exampleChainQuery`
3. Enter this code:
```javascript
// Simulated save operation
const inputValue = exampleGlobalNone.value;
if (!inputValue || inputValue === '""') {
  throw new Error("No data to save — state variable is empty");
}
return { saved: true, timestamp: new Date().toISOString(), value: inputValue };
```
4. Keep **Run on page load** OFF

### 5B. Add Success Handlers to exampleChainQuery

**Handler 1 — Update state variable:**
1. In `exampleChainQuery` event handlers, click **+ Add event handler**
2. Configure:
   - **Event**: `Success`
   - **Action**: `Control component`
   - **Component**: `exampleGlobalNone`
   - **Method**: `setValue`
   - **Value**: `{{ JSON.stringify(exampleChainQuery.data) }}`

**Handler 2 — Trigger table refresh:**
1. Click **+ Add event handler**
2. Configure:
   - **Event**: `Success`
   - **Action**: `Trigger query`
   - **Query**: `exampleGlobalSqlQuery`

**Handler 3 — Show success notification:**
1. Click **+ Add event handler**
2. Configure:
   - **Event**: `Success`
   - **Action**: `Show notification`
   - **Title**: `Save complete`
   - **Description**: `Data saved at {{ exampleChainQuery.data.timestamp }}`
   - **Type**: `Success`

### 5C. Add Failure Handler to exampleChainQuery

1. Click **+ Add event handler**
2. Configure:
   - **Event**: `Failure`
   - **Action**: `Show notification`
   - **Title**: `Save failed`
   - **Description**: `{{ exampleChainQuery.error }}`
   - **Type**: `Error`
   - **Duration (seconds)**: `6`

### 5D. Wire a Button to Trigger the Chain

1. Find an available button (or add a new `ButtonWidget2` near the form area)
2. If adding new: drag a **Button** component onto the canvas, label it `Save & Refresh`
3. Add event handler:
   - **Event**: `Click`
   - **Action**: `Trigger query`
   - **Query**: `exampleChainQuery`

---

## 6. Re-Export and Verification

### 6A. Export from Retool

1. In the Retool editor, click the **⋯** menu (top right) → **Export as JSON**
2. Save the file as `components example.json`
3. Move/copy it to: `apps/general references/components example.json` (replace the existing file)

### 6B. Run Extraction

```bash
cd "/Users/kevin/Documents/Agentic workflows/Retool Builder"
python3 tools/extract_transit_patterns.py "apps/general references/components example.json"
```

**Expected output:**
- Cache keys: ~31+ (should stay same or increase slightly)
- Widget subtypes: 95+ (may increase if new button added)
- Query subtypes: 5 (unchanged)
- **Event patterns: 40-50+** (was 29, should increase significantly)

### 6C. Run Validation

```bash
python3 tools/validate_retool_json.py "apps/general references/components example.json"
```

**Expected**: `PASS — 0 warning(s)`

### 6D. Verify Specific Patterns

```bash
python3 -c "
import json
with open('tools/transit_patterns.json') as f:
    p = json.load(f)

# Check query events
for qt_name, qt in p['query_templates'].items():
    events = qt['template'].get('events', [])
    count = len(events) if isinstance(events, list) else 0
    print(f'{qt_name}: {count} events')

print()

# Check event types
event_types = set()
methods = set()
for ep in p['event_patterns']:
    event_types.add(ep['event'].get('event', '?'))
    methods.add(ep['event'].get('method', '?'))
print(f'Event types: {sorted(event_types)}')
print(f'Methods: {sorted(methods)}')

print()

# Check state variety
print(f'State templates: {len(p[\"state_templates\"])}')
for name, s in p['state_templates'].items():
    print(f'  {s[\"example_id\"]}: value={s[\"template\"].get(\"value\", \"?\")}')
"
```

**What to verify:**
- [ ] SqlQueryUnified events > 0 (was 0)
- [ ] RESTQuery events > 0 (was 0)
- [ ] RetoolAIQuery events > 0 (was 0)
- [ ] `change` appears in event types (from input onChange handlers)
- [ ] `failure` or error-type events appear
- [ ] State templates show different value types (number, array, object)
- [ ] Event methods include: `setValue`, `trigger`, `showNotification`, `openUrl`

---

## Summary Checklist

```
QUERY EVENTS:
  □ exampleGlobalSqlQuery: onSuccess (setValue + notify) + onFailure (notify)
  □ ExampleGlobalRestQuery: POST body + onSuccess (trigger) + onFailure (notify)
  □ exampleGlobalJsQuery: onFailure (notify)
  □ llmChat1_query1: fill prompt + instruction + onSuccess (setValue)
  □ agentChat1_query1: optional (skip if no agent)

WIDGET onChange EVENTS:
  □ textInput1: change → setValue
  □ select1: change → trigger query
  □ numberInput1: change → setValue
  □ date1: change → trigger query
  □ modalFrame1: close → setValue (clear)
  □ button (any): click → open URL

STATE VARIABLES:
  □ exampleNumberState (value: 0)
  □ exampleArrayState (value: [])
  □ exampleObjectState (value: {})
  □ Verify examplePageNone is page-scoped (or add examplePage2State)

TABLE VISUALS:
  □ table1: column text color (conditional)
  □ table1: row background color (conditional)

QUERY CHAIN:
  □ Create exampleChainQuery (JS)
  □ 3 onSuccess handlers (setValue + trigger + notify)
  □ 1 onFailure handler (notify)
  □ Button → trigger exampleChainQuery

EXPORT:
  □ Export JSON from Retool
  □ Replace apps/general references/components example.json
  □ Run extract_transit_patterns.py
  □ Run validate_retool_json.py
  □ Verify event counts and new patterns
```
