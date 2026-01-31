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

Retool uses Transit JSON, a format that compresses repeated keys.

### Type Markers

| Marker | Meaning |
|--------|---------|
| `~#iR` | Root Record |
| `~#iL` | List (array) |
| `~#iOM` | Ordered Map |
| `~#iM` | Map |
| `~m` | Timestamp (milliseconds) |
| `["^ "]` | Empty map |

### Key Caching

Transit caches repeated keys with `^X` notation:
- First occurrence: `"type"`
- Subsequent: `"^1;"` (reference to cached key)

Common cached key references:
| Reference | Typical Meaning |
|-----------|-----------------|
| `^0` | Record wrapper |
| `^7` | `createdAt` |
| `^15` / `^18` | Empty array reference |
| `^19` | `uuid` |
| `^1;` | `type` |
| `^1<` | `subtype` |
| `^1=` | `namespace` |
| `^1>` | `resourceName` |
| `^1@` | `template` |
| `^1M` | Map marker |

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

Every widget follows this plugin template structure:

```json
{
  "id": "componentId",
  "uuid": "unique-uuid",
  "_comment": null,
  "type": "widget",
  "subtype": "WidgetType",
  "namespace": null,
  "resourceName": null,
  "resourceDisplayName": null,
  "template": { /* widget-specific properties */ },
  "style": null,
  "position2": { /* positioning */ },
  "mobilePosition2": null,
  "mobileAppPosition": null,
  "tabIndex": null,
  "container": "parentContainerId",
  "createdAt": "~m1234567890",
  "updatedAt": "~m1234567890",
  "folder": "",
  "presetName": null,
  "screen": null,
  "boxId": null,
  "subBoxIds": null
}
```

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
- `height`: Row units (typically 0.4-2+ per component)
- `row`: Starting row position
- `col`: Starting column (0-11)

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

**CRITICAL**: Every plugin (query, widget, screen, frame) MUST have a complete footer with fields `^1A` through `^1L`. Missing footer fields cause subsequent plugins to be nested incorrectly and not recognized by Retool on import.

#### Required Footer Fields

```
"^1A",null,"^1B",null,"^1C",null,"^1D",null,"^1E",null,"^1F","","^7","~m<timestamp>","^1G","~m<timestamp>","^1H","","^1I",null,"^1J","<pageId>","^1K",null,"^1L",null
```

Key fields:
| Field | Purpose |
|-------|---------|
| `^1A` - `^1I` | Internal metadata (usually null or empty) |
| `^1J` | **Page assignment** (e.g., `"page1"`, `"favorites"`) |
| `^1K`, `^1L` | Additional metadata (usually null) |
| `^7`, `^1G` | Timestamps (`~m` prefix + milliseconds) |

#### Plugin Closing Pattern

Each plugin definition should end with this bracket pattern:

```
...,"^1J","page1","^1K",null,"^1L",null]]],
```

**Correct**: `]]],"` (3 closing brackets + comma) before the next sibling plugin
**Wrong**: `]]]]]],"` (6+ brackets) indicates missing footer fields

### Common Structural Bugs

#### 1. Missing Footer After Events

**Symptom**: Queries/widgets defined after the affected plugin are not visible in Retool after import.

**Cause**: When a plugin has an `events` array, the footer fields must come AFTER the events array closes. If the footer is omitted, subsequent plugins are nested at the wrong level.

**Example of bug**:
```
// WRONG - missing footer after events
"events",[["^1M",[...]]]]]]],"nextQuery"
                       ↑
                       Too many closing brackets, no footer
```

**Correct structure**:
```
// CORRECT - footer fields after events, then proper closing
"events",[["^1M",[...]]]]]]],"^1A",null,...,"^1J","page1","^1K",null,"^1L",null]]],"nextQuery"
```

#### 2. Bracket Count Mismatch

**How to verify**: Check what appears immediately before each plugin definition:

```python
# Validation script
for query_name in ['query1', 'query2', 'query3']:
    idx = app_state.find(f'"{query_name}",["^0"')
    before = app_state[idx-15:idx]
    print(f'{query_name}: {before}')
    # Should show: ]]]," pattern for all siblings
```

**Expected output** (all siblings should match):
```
query1: ","^1L",null]]],"
query2: ","^1L",null]]],"
query3: ","^1L",null]]],"
```

**Bug indicator** (mismatched brackets):
```
query1: ","^1L",null]]],"   ✓ correct
query2: ror'})"]]]]]],"     ✗ WRONG - 6 brackets, missing footer
query3: ","^1L",null]]],"   ✓ correct (but may be nested wrong)
```

#### 3. Duplicate Footer/Ending Sections (Copy-Paste Error)

**Symptom**: A plugin has too many closing brackets, often 5+ extra `]` characters. Other plugins may appear to be missing brackets.

**Cause**: When copying plugin definitions as templates, the footer+closing section (`]],"^1A",null,...,"^1L",null]]]`) gets duplicated. This adds 5 extra closing brackets to one plugin.

**Example of bug**:
```
// WRONG - duplicate footer (first one is incomplete, second is complete)
"queryTimeout","10000","requireConfirmation",false,"type","GET"]],"^1A",null,...,"^1L",null]]],"queryTimeout","10000","workflowId",...
                                                              ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
                                                              This entire section is a duplicate and should be removed
```

**Detection**: Look for `]]],"queryTimeout"` or `]]],"<any-template-prop>"` patterns - the footer should only be followed by the next plugin name, not more template properties.

#### 4. Cross-Plugin Bracket Compensation

**Symptom**: Global bracket count is balanced, but individual plugins have mismatched brackets. Retool import may fail with cryptic errors or silently drop plugins.

**Cause**: When one plugin is missing content (fewer closing brackets), another plugin has extra content (more closing brackets). The errors cancel out globally but break the nesting structure.

**Example**:
```
Plugin A: 23 open, 18 close  ← Missing 5 closing brackets
Plugin B: 17 open, 22 close  ← Has 5 extra closing brackets
Total:    40 open, 40 close  ← LOOKS BALANCED but is BROKEN
```

**How to detect**: Always check bracket balance PER PLUGIN, not just globally. Use the enhanced validation script below.

### Per-Plugin Bracket Balance

**IMPORTANT**: Each plugin must have balanced brackets INDIVIDUALLY. A globally balanced file can still be broken if brackets are misallocated between plugins.

#### How to Extract and Validate Individual Plugins

```python
import re

def extract_plugin_content(app_state, plugin_name):
    """Extract the content of a single plugin from appState."""
    # Find plugin start
    start_pattern = f'"{plugin_name}",["^0"'
    start_idx = app_state.find(start_pattern)
    if start_idx == -1:
        return None

    # Find next sibling plugin (or end)
    # Look for pattern: ]]],"pluginName",["^0"
    next_plugin = re.search(r'\]\]\],"([a-zA-Z][a-zA-Z0-9_]+)",\["\^0"', app_state[start_idx+10:])

    if next_plugin:
        end_idx = start_idx + 10 + next_plugin.start() + 3  # Include the ]]]
    else:
        # Last plugin - find the closing ]]] before "]
        end_idx = app_state.find(']]]"]', start_idx) + 3

    return app_state[start_idx:end_idx]

def check_plugin_brackets(app_state, plugin_name):
    """Check if a plugin has balanced brackets."""
    content = extract_plugin_content(app_state, plugin_name)
    if not content:
        return None, None, "Plugin not found"

    opens = content.count('[')
    closes = content.count(']')

    if opens == closes:
        return opens, closes, "✓ Balanced"
    elif opens > closes:
        return opens, closes, f"✗ Missing {opens - closes} closing bracket(s)"
    else:
        return opens, closes, f"✗ Has {closes - opens} extra closing bracket(s)"
```

### Validation Script (Enhanced)

Use this Python script to validate Transit structure before import:

```python
import json
import re

def validate_retool_json(filepath):
    with open(filepath) as f:
        data = json.load(f)

    app_state = data['page']['data']['appState']

    # Verify appState is valid JSON
    try:
        json.loads(app_state)
    except json.JSONDecodeError as e:
        print(f"CRITICAL: appState is not valid JSON: {e}")
        return False

    # Find all plugin definitions
    plugins = re.findall(r'"([a-zA-Z][a-zA-Z0-9_]+)",\["\^0"', app_state)

    print(f"Found {len(plugins)} plugins: {plugins}")
    print()

    errors = []
    warnings = []

    # Check 1: Sibling pattern (]]]," before each plugin)
    for plugin in plugins:
        idx = app_state.find(f'"{plugin}",["^0"')
        before = app_state[idx-15:idx]

        if ']]],"' not in before and idx > 100:
            bracket_count = before.count(']')
            if bracket_count > 3:
                errors.append(f'{plugin}: Found {bracket_count} brackets before - missing footer in previous plugin')
            elif bracket_count < 3:
                errors.append(f'{plugin}: Found only {bracket_count} brackets before - previous plugin may have extra content')

    # Check 2: Per-plugin bracket balance
    print("Per-plugin bracket balance:")
    for i, plugin in enumerate(plugins):
        content = extract_plugin_content(app_state, plugin)
        if content:
            opens = content.count('[')
            closes = content.count(']')
            status = "✓" if opens == closes else "✗"
            diff = opens - closes

            print(f"  {plugin}: [{opens}/{closes}] {status}")

            if diff != 0:
                if diff > 0:
                    errors.append(f'{plugin}: Missing {diff} closing bracket(s)')
                else:
                    errors.append(f'{plugin}: Has {-diff} extra closing bracket(s)')

    # Check 3: Footer field presence
    print()
    print("Footer field presence:")
    for plugin in plugins:
        content = extract_plugin_content(app_state, plugin)
        if content:
            has_footer = '"^1L",null]]]' in content or '"^1L",null]],' in content
            status = "✓" if has_footer else "✗ MISSING"
            print(f"  {plugin}: {status}")

            if not has_footer:
                errors.append(f'{plugin}: Missing footer fields (^1A through ^1L)')

    # Check 4: Duplicate footer detection
    for plugin in plugins:
        content = extract_plugin_content(app_state, plugin)
        if content:
            footer_count = content.count('"^1L",null]]]')
            if footer_count > 1:
                errors.append(f'{plugin}: Has {footer_count} footer sections (duplicate detected)')

    print()
    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
        return False

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")

    print("✓ Transit structure validated successfully")
    return True

def extract_plugin_content(app_state, plugin_name):
    """Extract the content of a single plugin from appState."""
    start_pattern = f'"{plugin_name}",["^0"'
    start_idx = app_state.find(start_pattern)
    if start_idx == -1:
        return None

    next_plugin = re.search(r'\]\]\],"([a-zA-Z][a-zA-Z0-9_]+)",\["\^0"', app_state[start_idx+10:])

    if next_plugin:
        end_idx = start_idx + 10 + next_plugin.start() + 3
    else:
        end_idx = app_state.find(']]]"]', start_idx) + 3

    return app_state[start_idx:end_idx]

# Usage
validate_retool_json('apps/my-app.json')
```

---

## File Generation Checklist

When generating a Retool app JSON:

1. [ ] Valid UUID for app
2. [ ] Proper Transit JSON encoding
3. [ ] All components have unique IDs
4. [ ] Queries defined before components that reference them
5. [ ] Event handlers have valid target IDs
6. [ ] Position2 values create proper layout
7. [ ] Container references are valid
8. [ ] Screen/page structure is complete
9. [ ] Theme settings included if customized
10. [ ] No comments in JSON (invalid syntax)
11. [ ] **All plugins have complete footer fields (`^1A` through `^1L`)**
12. [ ] **Bracket pattern `]]],"` before each sibling plugin**
13. [ ] **Each plugin has balanced brackets individually (not just globally)**
14. [ ] **No duplicate footer sections from copy-paste errors**
15. [ ] **appState string is valid JSON when parsed (`json.loads(appState)` succeeds)**
