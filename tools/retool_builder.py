#!/usr/bin/env python3
"""
Retool Transit JSON Builder Library

Generates valid Retool app JSON using full Transit field names (not cache keys).
This approach is immune to cache key positional drift between Retool versions.

Usage:
    from tools.retool_builder import *

    plugins = [
        ("page1", screen_plugin("page1", "My App", "my-app", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),
        ("title", widget("title", "TextWidget2",
            txt_tmpl("# Hello World"),
            pos(0, 0, 4, 12, "$main", "page1"),
            screen="page1")),
        ("fetchData", query("fetchData", "JavascriptQuery",
            js_tmpl("return [{name: 'test'}]", run_on_load=True),
            screen="page1")),
    ]
    app = build_app(plugins)
    save_app(app, "output.json", "My App")
"""

import json
import uuid
import time
import os

NOW_MS = int(time.time() * 1000)
TS = f"~m{NOW_MS}"


# ══════════════════════════════════════════════════════════════════════════════
# TRANSIT PRIMITIVES
# ══════════════════════════════════════════════════════════════════════════════

def tmap(*args):
    """Transit map: ["^ ", k1, v1, k2, v2, ...]"""
    result = ["^ "]
    for i in range(0, len(args), 2):
        result.append(args[i])
        result.append(args[i + 1])
    return result


def tom(*args):
    """Transit ordered map: ["~#iOM", [k1, v1, k2, v2, ...]]"""
    flat = []
    for i in range(0, len(args), 2):
        flat.append(args[i])
        flat.append(args[i + 1])
    return ["~#iOM", flat]


def tlist(items):
    """Transit list: ["~#iL", [...]]"""
    return ["~#iL", items]


def record(name, value):
    """Transit record: ["~#iR", ["^ ", "n", name, "v", value]]"""
    return ["~#iR", tmap("n", name, "v", value)]


# ══════════════════════════════════════════════════════════════════════════════
# POSITION BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def pos(row, col, height, width, container="", screen="page1", row_group="body"):
    """Build a position2 record for grid placement."""
    return record("position2", tmap(
        "type", "grid",
        "container", container,
        "rowGroup", row_group,
        "subcontainer", "",
        "row", row,
        "col", col,
        "height", height,
        "width", width,
        "tabNum", 0,
        "stackPosition", None
    ))


# ══════════════════════════════════════════════════════════════════════════════
# PLUGIN BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def widget(id_, subtype, template, position2, container="", screen="page1"):
    """Build a widget plugin record."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", str(uuid.uuid4()),
        "_comment", None,
        "type", "widget",
        "subtype", subtype,
        "namespace", None,
        "resourceName", None,
        "resourceDisplayName", None,
        "template", template,
        "style", None,
        "position2", position2,
        "mobilePosition2", None,
        "mobileAppPosition", None,
        "tabIndex", None,
        "container", container,
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", screen,
        "boxId", None,
        "subBoxIds", None
    ))


def query(id_, subtype, template, resource_uuid=None, resource_name=None, screen="page1"):
    """Build a query (datasource) plugin record."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", str(uuid.uuid4()),
        "_comment", None,
        "type", "datasource",
        "subtype", subtype,
        "namespace", None,
        "resourceName", resource_uuid,
        "resourceDisplayName", resource_name,
        "template", template,
        "style", None,
        "position2", None,
        "mobilePosition2", None,
        "mobileAppPosition", None,
        "tabIndex", None,
        "container", None,
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", screen,
        "boxId", None,
        "subBoxIds", None
    ))


def state_var(id_, value="", persistence="none", screen=None):
    """Build a state variable plugin record. screen=None for global, screen="page1" for page-scoped."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", str(uuid.uuid4()),
        "_comment", None,
        "type", "state",
        "subtype", "StateSlot",
        "namespace", None,
        "resourceName", None,
        "resourceDisplayName", None,
        "template", tom("value", value, "persistence", persistence),
        "style", None,
        "position2", None,
        "mobilePosition2", None,
        "mobileAppPosition", None,
        "tabIndex", None,
        "container", None,
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", screen,
        "boxId", None,
        "subBoxIds", None
    ))


def screen_plugin(id_, title, slug, order):
    """Build a screen plugin record."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", str(uuid.uuid4()),
        "_comment", None,
        "type", "screen",
        "subtype", "Screen",
        "namespace", None,
        "resourceName", None,
        "resourceDisplayName", None,
        "template", tom(
            "title", title,
            "browserTitle", title,
            "urlSlug", slug,
            "_order", order,
            "_searchParams", [],
            "_hashParams", [],
            "_customShortcuts", []
        ),
        "style", None,
        "position2", None,
        "mobilePosition2", None,
        "mobileAppPosition", None,
        "tabIndex", None,
        "container", None,
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", id_,
        "boxId", None,
        "subBoxIds", None
    ))


def frame_plugin(id_, screen_id, frame_type="main"):
    """Build a frame plugin record."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", str(uuid.uuid4()),
        "_comment", None,
        "type", "frame",
        "subtype", "Frame",
        "namespace", None,
        "resourceName", None,
        "resourceDisplayName", None,
        "template", tom(
            "type", frame_type,
            "padding", "8px 12px",
            "enableFullBleed", False,
            "isHiddenOnDesktop", False,
            "isHiddenOnMobile", False
        ),
        "style", None,
        "position2", None,
        "mobilePosition2", None,
        "mobileAppPosition", None,
        "tabIndex", None,
        "container", "",
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", screen_id,
        "boxId", None,
        "subBoxIds", None
    ))


def modal_plugin(id_, screen_id, size="medium"):
    """Build a modal frame plugin record."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", str(uuid.uuid4()),
        "_comment", None,
        "type", "frame",
        "subtype", "ModalFrameWidget",
        "namespace", None,
        "resourceName", None,
        "resourceDisplayName", None,
        "template", tom(
            "size", size,
            "hideOnEscape", True,
            "overlayInteraction", True,
            "headerPadding", "8px 12px",
            "showFooterBorder", True,
            "enableFullBleed", False,
            "isHiddenOnDesktop", False,
            "showBorder", True,
            "hidden", True,
            "showHeader", True,
            "padding", "8px 12px",
            "showOverlay", True,
            "isHiddenOnMobile", True,
            "showHeaderBorder", True,
            "footerPadding", "8px 12px",
            "showFooter", True,
            "events", []
        ),
        "style", None,
        "position2", None,
        "mobilePosition2", None,
        "mobileAppPosition", None,
        "tabIndex", None,
        "container", "",
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", screen_id,
        "boxId", None,
        "subBoxIds", None
    ))


def drawer_plugin(id_, screen_id, width="medium"):
    """Build a drawer frame plugin record."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", str(uuid.uuid4()),
        "_comment", None,
        "type", "frame",
        "subtype", "DrawerFrameWidget",
        "namespace", None,
        "resourceName", None,
        "resourceDisplayName", None,
        "template", tom(
            "width", width,
            "hideOnEscape", True,
            "overlayInteraction", True,
            "headerPadding", "8px 12px",
            "showFooterBorder", True,
            "enableFullBleed", False,
            "isHiddenOnDesktop", False,
            "showBorder", True,
            "hidden", True,
            "showHeader", True,
            "padding", "8px 12px",
            "showOverlay", True,
            "isHiddenOnMobile", True,
            "showHeaderBorder", True,
            "footerPadding", "8px 12px",
            "showFooter", True,
            "events", []
        ),
        "style", None,
        "position2", None,
        "mobilePosition2", None,
        "mobileAppPosition", None,
        "tabIndex", None,
        "container", "",
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", screen_id,
        "boxId", None,
        "subBoxIds", None
    ))


# ══════════════════════════════════════════════════════════════════════════════
# EVENT HANDLER BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def evt(event_type, src):
    """Generic event handler that runs a JavaScript src string."""
    return tmap(
        "id", str(uuid.uuid4()),
        "type", "widget",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "run",
        "pluginId", "",
        "targetId", None,
        "params", tmap("src", src)
    )


def evt_trigger_query(event_type, query_id):
    """Event handler that triggers a named query."""
    return tmap(
        "id", str(uuid.uuid4()),
        "type", "datasource",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "trigger",
        "pluginId", query_id,
        "targetId", None,
        "params", tmap()
    )


def evt_show_frame(event_type, frame_id):
    """Event handler that shows a modal/drawer."""
    return tmap(
        "id", str(uuid.uuid4()),
        "type", "widget",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "show",
        "pluginId", frame_id,
        "targetId", None,
        "params", tmap()
    )


def evt_hide_frame(event_type, frame_id):
    """Event handler that hides a modal/drawer."""
    return tmap(
        "id", str(uuid.uuid4()),
        "type", "widget",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "hide",
        "pluginId", frame_id,
        "targetId", None,
        "params", tmap()
    )


def evt_set_var(event_type, var_id, value_expr):
    """Event handler that sets a state variable."""
    return tmap(
        "id", str(uuid.uuid4()),
        "type", "state",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "setValue",
        "pluginId", var_id,
        "targetId", None,
        "params", tmap("value", value_expr)
    )


def evt_notification(event_type, notif_type="success", title="", description="", duration=4.5):
    """Event handler that shows a notification toast."""
    return tmap(
        "id", str(uuid.uuid4()),
        "type", "util",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "showNotification",
        "pluginId", "",
        "targetId", None,
        "params", tmap(
            "type", notif_type,
            "title", title,
            "description", description,
            "duration", duration
        )
    )


# ══════════════════════════════════════════════════════════════════════════════
# WIDGET TEMPLATE FACTORIES
# ══════════════════════════════════════════════════════════════════════════════

def txt_tmpl(value, overflow="scroll"):
    """TextWidget2 template."""
    return tom(
        "heightType", "auto",
        "horizontalAlign", "left",
        "hidden", False,
        "imageWidth", "fit",
        "margin", "4px 8px",
        "showInEditor", False,
        "verticalAlign", "center",
        "tooltipText", "",
        "value", value,
        "disableMarkdown", False,
        "overflowType", overflow,
        "maintainSpaceWhenHidden", False
    )


def btn_tmpl(text, events=None, variant="solid", disabled="", loading="", danger=False):
    """ButtonWidget2 template."""
    return tom(
        "heightType", "fixed",
        "horizontalAlign", "stretch",
        "clickable", False,
        "iconAfter", "",
        "submitTargetId", None,
        "hidden", False,
        "ariaLabel", "",
        "text", text,
        "margin", "4px 8px",
        "showInEditor", False,
        "tooltipText", "",
        "allowWrap", True,
        "styleVariant", "danger" if danger else variant,
        "submit", False,
        "iconBefore", "",
        "events", events or [],
        "loading", loading if loading else False,
        "disabled", disabled if disabled else False,
        "maintainSpaceWhenHidden", False
    )


def textinput_tmpl(label, placeholder, value=""):
    """TextInputWidget2 template."""
    return tom(
        "spellCheck", False,
        "readOnly", False,
        "iconAfter", "",
        "showCharacterCount", False,
        "autoComplete", False,
        "enforceMaxLength", False,
        "maxLength", None,
        "hidden", False,
        "customValidation", "",
        "patternType", "",
        "hideValidationMessage", False,
        "textBefore", "",
        "validationMessage", "",
        "margin", "4px 8px",
        "textAfter", "",
        "showInEditor", False,
        "showClear", True,
        "pattern", "",
        "tooltipText", "",
        "labelAlign", "left",
        "formDataKey", "{{ self.id }}",
        "value", value,
        "labelCaption", "",
        "labelWidth", "33",
        "label", label,
        "placeholder", placeholder,
        "labelWidthUnit", "%",
        "invalid", False,
        "events", [],
        "inputValue", "",
        "loading", False,
        "minLength", None,
        "disabled", False,
        "required", False,
        "maintainSpaceWhenHidden", False
    )


def textarea_tmpl(label, placeholder, value="", height_type="fixed"):
    """TextAreaWidget template."""
    return tom(
        "heightType", height_type,
        "spellCheck", False,
        "readOnly", False,
        "iconAfter", "",
        "showCharacterCount", False,
        "enforceMaxLength", False,
        "maxLength", None,
        "hidden", False,
        "customValidation", "",
        "hideValidationMessage", False,
        "textBefore", "",
        "validationMessage", "",
        "margin", "4px 8px",
        "textAfter", "",
        "showInEditor", False,
        "showClear", True,
        "tooltipText", "",
        "labelAlign", "left",
        "formDataKey", "{{ self.id }}",
        "value", value,
        "labelCaption", "",
        "labelWidth", "33",
        "label", label,
        "placeholder", placeholder,
        "labelWidthUnit", "%",
        "invalid", False,
        "events", [],
        "inputValue", "",
        "loading", False,
        "minLength", None,
        "disabled", False,
        "required", False,
        "maintainSpaceWhenHidden", False,
        "autoHeight", True
    )


def select_tmpl(label, values="[]", labels="[]", placeholder="Select...", events=None):
    """SelectWidget2 template."""
    return tom(
        "iconAfter", "",
        "allowDeselect", True,
        "hidden", False,
        "customValidation", "",
        "hideValidationMessage", False,
        "textBefore", "",
        "validationMessage", "",
        "margin", "4px 8px",
        "textAfter", "",
        "showInEditor", False,
        "showClear", True,
        "tooltipText", "",
        "labelAlign", "left",
        "formDataKey", "{{ self.id }}",
        "values", values,
        "labels", labels,
        "labelCaption", "",
        "labelWidth", "33",
        "label", label,
        "placeholder", placeholder,
        "labelWidthUnit", "%",
        "invalid", False,
        "events", events or [],
        "loading", False,
        "disabled", False,
        "required", False,
        "maintainSpaceWhenHidden", False
    )


def numberinput_tmpl(label, placeholder="", value="", min_val=None, max_val=None):
    """NumberInputWidget template."""
    return tom(
        "readOnly", False,
        "iconAfter", "",
        "hidden", False,
        "customValidation", "",
        "hideValidationMessage", False,
        "textBefore", "",
        "validationMessage", "",
        "margin", "4px 8px",
        "textAfter", "",
        "showInEditor", False,
        "showClear", True,
        "tooltipText", "",
        "labelAlign", "left",
        "formDataKey", "{{ self.id }}",
        "value", value,
        "labelCaption", "",
        "labelWidth", "33",
        "label", label,
        "placeholder", placeholder,
        "labelWidthUnit", "%",
        "minimum", min_val,
        "maximum", max_val,
        "invalid", False,
        "events", [],
        "loading", False,
        "disabled", False,
        "required", False,
        "maintainSpaceWhenHidden", False
    )


def container_tmpl(show_header=False, show_border=True, padding="8px"):
    """ContainerWidget2 template."""
    return tom(
        "_direction", "horizontal",
        "heightType", "auto",
        "currentViewKey", None,
        "clickable", False,
        "headerPadding", "4px 12px",
        "showFooterBorder", False,
        "enableFullBleed", False,
        "showBorder", show_border,
        "hidden", False,
        "showHeader", show_header,
        "hoistFetching", False,
        "margin", "4px 8px",
        "showInEditor", False,
        "tooltipText", "",
        "padding", padding,
        "showHeaderBorder", False,
        "showFooter", False,
        "_type", "grid",
        "events", [],
        "loading", False,
        "overflowType", "scroll",
        "maintainSpaceWhenHidden", False,
        "showBody", True,
        "style", tom("border", "surfacePrimaryBorder", "borderRadius", "8px")
    )


def table_col(key, label, fmt="string", size=100, editable=False, hidden="",
              value_override="", alignment="left"):
    """Define a table column. Returns a dict consumed by table_tmpl()."""
    return {
        "id": uuid.uuid4().hex[:5],
        "key": key, "label": label, "format": fmt,
        "size": size, "editable": "true" if editable else "",
        "hidden": hidden, "value_override": value_override,
        "alignment": alignment,
    }


def table_action(label, icon="bold/interface-edit-pencil"):
    """Define a table row action. Returns a dict consumed by table_tmpl()."""
    return {"id": uuid.uuid4().hex[:5], "label": label, "icon": icon}


def _col_map(columns, field, default=""):
    """Build a tom() from columns for a given field with a default value."""
    args = []
    for c in columns:
        args.extend([c["id"], c.get(field, default)])
    return tom(*args)


def _col_map_const(columns, value):
    """Build a tom() from columns with a constant value for all."""
    args = []
    for c in columns:
        args.extend([c["id"], value])
    return tom(*args)


def _col_map_empty_obj(columns):
    """Build a tom() from columns where each value is an empty tom()."""
    args = []
    for c in columns:
        args.extend([c["id"], tom()])
    return tom(*args)


def _action_map(actions, field, default=""):
    """Build a tom() from actions for a given field."""
    args = []
    for a in actions:
        args.extend([a["id"], a.get(field, default)])
    return tom(*args)


def table_tmpl(data, columns=None, actions=None, events=None,
               row_height="medium", server_paginated=False,
               primary_key=None, empty_message="No rows found"):
    """TableWidget2 template with proper column maps matching Retool's iOM structure."""
    cols = columns or []
    acts = actions or []
    col_ids = [c["id"] for c in cols]
    act_ids = [a["id"] for a in acts]

    # Standard toolbar buttons
    tb_ids = ["tb_f", "tb_s", "tb_d", "tb_r"]
    tb_type = tom("tb_f", "filter", "tb_s", "sort", "tb_d", "custom", "tb_r", "custom")
    tb_label = tom("tb_f", "Filter", "tb_s", "Sort", "tb_d", "Download", "tb_r", "Refresh")
    tb_icon = tom(
        "tb_f", "bold/interface-text-formatting-filter-2",
        "tb_s", "bold/interface-arrows-vertical-expand-3",
        "tb_d", "bold/interface-download-button-2",
        "tb_r", "bold/interface-arrows-round-left"
    )
    tb_hidden = tom("tb_f", "", "tb_s", "", "tb_d", "", "tb_r", "")

    args = [
        # Column maps
        "_columnIds", col_ids,
        "_columnKey", _col_map(cols, "key"),
        "_columnLabel", _col_map(cols, "label"),
        "_columnFormat", _col_map(cols, "format", "string"),
        "_columnSize", _col_map(cols, "size", 100),
        "_columnAlignment", _col_map(cols, "alignment", "left"),
        "_columnEditable", _col_map(cols, "editable", ""),
        "_columnHidden", _col_map(cols, "hidden", ""),
        "_columnValueOverride", _col_map(cols, "value_override", ""),
        "_columnTextColor", _col_map_const(cols, ""),
        "_columnBackgroundColor", _col_map_const(cols, ""),
        "_columnHeaderTextColor", _col_map_const(cols, ""),
        "_columnHeaderBackgroundColor", _col_map_const(cols, ""),
        "_columnAlternateRowBackgroundColor", _col_map_const(cols, ""),
        "_columnCaption", _col_map_const(cols, ""),
        "_columnIcon", _col_map_const(cols, ""),
        "_columnPlaceholder", _col_map_const(cols, ""),
        "_columnReferenceId", _col_map_const(cols, ""),
        "_columnTooltip", _col_map_const(cols, ""),
        "_columnCellTooltip", _col_map_const(cols, ""),
        "_columnCellTooltipMode", _col_map_const(cols, "overflow"),
        "_columnPosition", _col_map_const(cols, "center"),
        "_columnSearchMode", _col_map_const(cols, "default"),
        "_columnSortMode", _col_map_const(cols, "default"),
        "_columnSortDisabled", _col_map_const(cols, False),
        "_columnSummaryAggregationMode", _col_map_const(cols, "none"),
        "_columnGroupAggregationMode", _col_map_const(cols, "none"),
        "_columnEditableInNewRows", _col_map_const(cols, ""),
        "_columnFormatOptions", _col_map_empty_obj(cols),
        "_columnEditableOptions", _col_map_empty_obj(cols),
        "_columnOptionList", _col_map_empty_obj(cols),
        "_columnStatusIndicatorOptions", _col_map_empty_obj(cols),

        # Action maps
        "_actionIds", act_ids,
        "_actionLabel", _action_map(acts, "label"),
        "_actionIcon", _action_map(acts, "icon", "bold/interface-edit-pencil"),
        "_actionHidden", _action_map(acts, "hidden", ""),
        "_actionDisabled", _action_map(acts, "disabled", ""),
        "_actionsOverflowPosition", 2,

        # Toolbar
        "_toolbarButtonIds", tb_ids,
        "_toolbarButtonType", tb_type,
        "_toolbarButtonLabel", tb_label,
        "_toolbarButtonIcon", tb_icon,
        "_toolbarButtonHidden", tb_hidden,
        "_toolbarPosition", "bottom",

        # Row config
        "_rowHeight", row_height,
        "_rowSelection", "single",
        "_rowBackgroundColor", [],
        "_showBorder", True,
        "_showColumnBorders", False,
        "_showHeader", True,
        "_showFooter", False,
        "_showSummaryRow", False,
        "_showToolbar", True,

        # Pagination
        "_serverPaginated", server_paginated,
        "_serverPaginationType", "cursorBased",
        "_pageSize", 10,
        "_templatePageSize", 10,
        "_currentPage", 0,
        "_primaryKeyColumnId", primary_key or (col_ids[0] if col_ids else ""),

        # Selection state
        "selectedRowKey", None,
        "selectedRowKeys", [],
        "selectedRow", tom(),
        "selectedRows", [],
        "selectedSourceRow", tom(),
        "selectedSourceRows", [],
        "selectedDataIndex", None,
        "selectedDataIndexes", [],
        "selectedCell", "",
        "_selectedCell", tom(),
        "_cellSelection", "none",

        # Core props
        "data", data,
        "events", events or [],
        "emptyMessage", empty_message,
        "heightType", "auto",
        "hidden", False,
        "maintainSpaceWhenHidden", False,
        "margin", "4px 8px",
        "showInEditor", False,
        "overflowType", "scroll",
        "columnOrdering", col_ids,
        "sortArray", [],
        "filterStack", tom(),
        "searchTerm", "",
        "searchMode", "local",
        "autoColumnWidth", False,
        "caseSensitiveFiltering", False,
        "changesetArray", [],
        "changesetObject", tom(),
        "newRows", [],
        "disableEdits", False,
        "disableSave", False,

        # Misc
        "_defaultSelectedRow", tom(),
        "_defaultFilters", [],
        "_defaultSort", [],
        "_changeset", tom(),
        "_clearChangeset", False,
        "_clearChangesetOnSave", True,
        "_enableSaveActions", False,
        "_enableExpandableRows", False,
        "_expandedRows", [],
        "_expandedRowDataIndexes", [],
        "_dynamicColumnsEnabled", False,
        "_dynamicColumnSource", "",
        "_dynamicColumnSize", 100,
        "_dynamicColumnProperties", tom(),
        "_dynamicColumnFormatOptions", tom(),
        "_dynamicRowHeights", False,
        "_disabledVirtualization", False,
        "_headerTextWrap", False,
        "_isAddingNewRows", False,
        "_isSaving", False,
        "_groupByColumns", [],
        "_groupedColumnConfig", tom(),
        "_persistRowSelection", False,
        "_selectMultipleRowsOnActionClick", False,
        "_selectSingleRowsOnActionClick", False,
        "_alwaysShowRowSelectionCheckboxes", False,
        "_includeRowInChangesetArray", False,
        "_linkedFilterId", "",
        "_afterCursor", "",
        "_beforeCursor", "",
        "_nextAfterCursor", "",
        "_nextBeforeCursor", "",
        "_hasNextPage", True,
        "_limitOffsetRowCount", 0,
        "_calculatedPageSize", 10,
        "_cursorCache", tom(),
        "_virtualizeStartIndex", 0,
        "_virtualizeEndIndex", 50,
        "overflowActionsOverlayMaxHeight", 350,
        "overflowActionsOverlayMinWidth", 200,
        "pagination", True,
        "loading", False,
        "isFetching", False,
    ]
    return tom(*args)


def chart_tmpl(data, chart_type, x_axis, y_axis, title=""):
    """ChartWidget2 template."""
    return tom(
        "heightType", "fixed",
        "chartType", chart_type,
        "data", data,
        "xAxis", x_axis,
        "yAxis", [y_axis],
        "hidden", False,
        "margin", "4px 8px",
        "tooltipText", "",
        "loading", False,
        "title", title
    )


def stat_tmpl(value, caption, format_style="number"):
    """StatisticWidget2 template."""
    return tom(
        "clickable", False,
        "positiveTrend", "{{ self.value >= 0 }}",
        "signDisplay", "auto",
        "secondaryCurrency", "USD",
        "secondarySuffix", "",
        "align", "left",
        "secondaryPrefix", "",
        "secondaryEnableTrend", False,
        "secondaryDecimalPlaces", 1,
        "hidden", False,
        "showSeparators", True,
        "formattingStyle", format_style,
        "margin", "4px 8px",
        "showInEditor", False,
        "tooltipText", "",
        "currency", "USD",
        "suffix", "",
        "prefix", "",
        "value", value,
        "decimalPlaces", 0,
        "enableTrend", False,
        "caption", caption,
        "loading", False,
        "secondaryValue", None
    )


def date_tmpl(label, value="", date_format="MMM d, yyyy"):
    """DateWidget template."""
    return tom(
        "minDate", "",
        "readOnly", False,
        "iconAfter", "",
        "datePlaceholder", "MMM D, YYYY",
        "dateFormat", date_format,
        "hidden", False,
        "customValidation", "",
        "hideValidationMessage", False,
        "textBefore", "",
        "validationMessage", "",
        "margin", "4px 8px",
        "textAfter", "",
        "showInEditor", False,
        "showClear", True,
        "tooltipText", "",
        "labelAlign", "left",
        "formDataKey", "{{ self.id }}",
        "value", value,
        "labelCaption", "",
        "labelWidth", "33",
        "label", label,
        "labelWidthUnit", "%",
        "invalid", False,
        "events", [],
        "disabled", False,
        "required", False
    )


def daterange_tmpl(label, start_value="", end_value="", date_format="MMM d, yyyy"):
    """DateRangeWidget template."""
    return tom(
        "minDate", "",
        "readOnly", False,
        "dateFormat", date_format,
        "hidden", False,
        "customValidation", "",
        "hideValidationMessage", False,
        "validationMessage", "",
        "margin", "4px 8px",
        "showInEditor", False,
        "showClear", True,
        "tooltipText", "",
        "labelAlign", "left",
        "formDataKey", "{{ self.id }}",
        "startValue", start_value,
        "endValue", end_value,
        "labelCaption", "",
        "labelWidth", "33",
        "label", label,
        "labelWidthUnit", "%",
        "invalid", False,
        "events", [],
        "disabled", False,
        "required", False
    )


def multiselect_tmpl(label, values="[]", labels="[]", placeholder="Select...", events=None):
    """MultiselectWidget2 template."""
    return tom(
        "iconAfter", "",
        "hidden", False,
        "customValidation", "",
        "hideValidationMessage", False,
        "textBefore", "",
        "validationMessage", "",
        "margin", "4px 8px",
        "textAfter", "",
        "showInEditor", False,
        "showClear", True,
        "tooltipText", "",
        "labelAlign", "left",
        "formDataKey", "{{ self.id }}",
        "values", values,
        "labels", labels,
        "labelCaption", "",
        "labelWidth", "33",
        "label", label,
        "placeholder", placeholder,
        "labelWidthUnit", "%",
        "invalid", False,
        "events", events or [],
        "loading", False,
        "disabled", False,
        "required", False,
        "maintainSpaceWhenHidden", False
    )


def tabs_tmpl(tab_names):
    """TabsWidget2 template."""
    return tom(
        "heightType", "auto",
        "hidden", False,
        "margin", "4px 8px",
        "showInEditor", False,
        "tooltipText", "",
        "tabNames", tab_names,
        "events", [],
        "maintainSpaceWhenHidden", False
    )


def form_tmpl(events=None):
    """FormWidget2 template."""
    return tom(
        "heightType", "auto",
        "headerPadding", "4px 12px",
        "showFooterBorder", True,
        "enableFullBleed", False,
        "showBorder", True,
        "hidden", False,
        "showHeader", True,
        "padding", "8px 12px",
        "showHeaderBorder", True,
        "footerPadding", "8px 12px",
        "showFooter", True,
        "showBody", True,
        "events", events or [],
        "maintainSpaceWhenHidden", False
    )


# ══════════════════════════════════════════════════════════════════════════════
# QUERY TEMPLATE FACTORIES
# ══════════════════════════════════════════════════════════════════════════════

def js_tmpl(code, run_on_load=False, events=None):
    """JavascriptQuery template."""
    return tom(
        "queryRefreshTime", "",
        "allowedGroupIds", [],
        "streamResponse", False,
        "lastReceivedFromResourceAt", None,
        "isFunction", False,
        "functionParameters", None,
        "queryDisabledMessage", "",
        "successMessage", "",
        "queryDisabled", "",
        "runWhenModelUpdates", False,
        "showFailureToaster", True,
        "query", code,
        "showSuccessToaster", False,
        "runWhenPageLoads", run_on_load,
        "isFetching", False,
        "events", events or [],
        "error", None
    )


def sql_tmpl(sql, run_on_load=False, success_msg="", events=None):
    """SQL query template (for RetoolTableQuery or PostgreSQL resources)."""
    return tom(
        "queryRefreshTime", "",
        "allowedGroupIds", [],
        "streamResponse", False,
        "records", "",
        "lastReceivedFromResourceAt", None,
        "isFunction", False,
        "functionParameters", None,
        "queryDisabledMessage", "",
        "successMessage", success_msg,
        "queryDisabled", "",
        "runWhenModelUpdates", False,
        "showFailureToaster", True,
        "query", sql,
        "showSuccessToaster", True if success_msg else False,
        "runWhenPageLoads", run_on_load,
        "confirmationMessage", "",
        "requireConfirmation", False,
        "databasePasswordOverride", "",
        "events", events or [],
        "actionType", "select",
        "filterBy", [],
        "sortBy", [],
        "error", None
    )


def rest_tmpl(method, path, body="", headers="", run_on_load=False, events=None):
    """RESTQuery template."""
    return tom(
        "queryRefreshTime", "",
        "allowedGroupIds", [],
        "streamResponse", False,
        "body", body,
        "lastReceivedFromResourceAt", None,
        "isFunction", False,
        "queryDisabledMessage", "",
        "successMessage", "",
        "queryDisabled", "",
        "runWhenModelUpdates", False,
        "headers", headers,
        "showFailureToaster", True,
        "query", "",
        "showSuccessToaster", False,
        "runWhenPageLoads", run_on_load,
        "confirmationMessage", "",
        "requireConfirmation", False,
        "method", method,
        "path", path,
        "events", events or [],
        "error", None
    )


def ai_tmpl(prompt, model="gpt-4", system_prompt=""):
    """RetoolAIQuery template."""
    return tom(
        "queryRefreshTime", "",
        "allowedGroupIds", [],
        "streamResponse", False,
        "lastReceivedFromResourceAt", None,
        "isFunction", False,
        "queryDisabledMessage", "",
        "successMessage", "",
        "queryDisabled", "",
        "runWhenModelUpdates", False,
        "showFailureToaster", True,
        "showSuccessToaster", False,
        "runWhenPageLoads", False,
        "prompt", prompt,
        "model", model,
        "systemPrompt", system_prompt,
        "events", [],
        "error", None
    )


# ══════════════════════════════════════════════════════════════════════════════
# APP ASSEMBLY
# ══════════════════════════════════════════════════════════════════════════════

def build_app(plugins, theme=None):
    """
    Assemble a complete Retool appState from a list of (id, plugin_record) tuples.

    Args:
        plugins: list of (id_string, plugin_record) tuples
        theme: optional tmap of theme colors (uses Retool defaults if None)

    Returns:
        Transit record representing the full appState
    """
    flat = []
    for id_, plugin_val in plugins:
        flat.append(id_)
        flat.append(plugin_val)
    plugins_om = ["~#iOM", flat]

    default_theme = theme or tmap(
        "borderRadius", "8px",
        "primary", "#2563eb",
        "success", "#16a34a",
        "danger", "#dc2626",
        "warning", "#eab308",
        "info", "#3b82f6",
        "textDark", "#0f172a",
        "textLight", "#ffffff",
        "surfacePrimary", "#ffffff",
        "surfaceSecondary", "#f8fafc",
        "canvas", "#f1f5f9"
    )

    app_template = tmap(
        "appMaxWidth", "100%",
        "appStyles", "",
        "appTesting", None,
        "appThemeId", None,
        "appThemeModeId", None,
        "appThemeName", None,
        "createdAt", None,
        "customComponentCollections", [],
        "customDocumentTitle", "",
        "customDocumentTitleEnabled", False,
        "customShortcuts", [],
        "experimentalFeatures", tmap(
            "disableMultiplayerEditing", False,
            "multiplayerEditingEnabled", False,
            "sourceControlTemplateDehydration", False
        ),
        "folders", tlist([]),
        "formAppSettings", tmap("customRedirectUrl", ""),
        "inAppRetoolPillAppearance", "NO_OVERRIDE",
        "instrumentationEnabled", False,
        "internationalizationSettings", tmap(
            "internationalizationEnabled", False,
            "internationalizationFiles", []
        ),
        "isFetching", False,
        "isFormApp", False,
        "isGlobalWidget", False,
        "isMobileApp", False,
        "loadingIndicatorsDisabled", False,
        "markdownLinkBehavior", "auto",
        "mobileAppSettings", tmap("allowedOrientations", "all"),
        "notificationsSettings", tmap(
            "globalQueryShowFailureToast", True,
            "globalQueryShowSuccessToast", False,
            "globalQueryToastDuration", 4.5,
            "globalToastPosition", "bottomRight"
        ),
        "plugins", plugins_om,
        "preloadedAppData", tmap(),
        "releaseNotes", None,
        "screens", tlist([]),
        "selectedAccessGroup", None,
        "showEditingInterface", True,
        "theme", default_theme
    )

    return record("appTemplate", app_template)


def save_app(app_state_obj, output_path, app_name="Untitled App"):
    """
    Wrap appState in the outer Retool JSON envelope and write to file.

    Args:
        app_state_obj: Transit record from build_app()
        output_path: file path for the output JSON
        app_name: display name (used in metadata only)

    Returns:
        The output file path
    """
    app_state_str = json.dumps(app_state_obj, separators=(',', ':'))

    retool_json = {
        "uuid": str(uuid.uuid4()),
        "page": {
            "id": 999999001,
            "data": {
                "appState": app_state_str
            },
            "changesRecord": [],
            "changesRecordV2": [],
            "checksum": None,
            "multiplayerSessionId": str(uuid.uuid4()),
            "appTestingSaveId": None,
            "subflows": None,
            "isCopilotGenerated": False,
            "createdAt": "2026-01-01T00:00:00.000Z",
            "updatedAt": "2026-01-01T00:00:00.000Z",
            "pageId": 999999,
            "userId": 0
        },
        "modules": {}
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(retool_json, f, indent=2)

    print(f"Generated: {output_path}")
    print(f"  App state size: {len(app_state_str):,} bytes")
    plugin_count = len(app_state_obj[1][4][1:]) // 2  # navigate to plugins iOM
    # Find plugins in the tmap
    tmap_pairs = app_state_obj[1][4][1:]  # skip '^ '
    for i in range(0, len(tmap_pairs), 2):
        if tmap_pairs[i] == "plugins":
            iom_items = tmap_pairs[i + 1][1]
            plugin_count = len(iom_items) // 2
            break
    print(f"  Total plugins: {plugin_count}")

    return output_path
