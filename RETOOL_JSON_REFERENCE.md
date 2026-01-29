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
