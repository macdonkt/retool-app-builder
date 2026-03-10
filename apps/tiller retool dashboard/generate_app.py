#!/usr/bin/env python3
"""
Generate Tiller Finance Dashboard v2 Retool app JSON.
Run: python3 generate_app.py
Output: tiller-dashboard-v2.json
"""

import json
import uuid
import time
import os

NOW_MS = int(time.time() * 1000)
TS = f"~m{NOW_MS}"

# ── Resource UUIDs (from v1 export — user must reconnect after import) ────────
GSHEETS_RESOURCE_UUID = "f859c0ad-40a4-445b-9adb-2f3808e1013f"
GSHEETS_RESOURCE_NAME = "Google_sheets_Tiller"
RETOOL_DB_UUID = "ba116730-d6f2-40e2-9689-970c350ddffd"
RETOOL_DB_NAME = "retool_db"
CLAUDE_RESOURCE_UUID = "claude-api-resource-uuid-replace-me"
CLAUDE_RESOURCE_NAME = "claude_api"
SPREADSHEET_ID = "1fokhoSVGss2ivA_8gnuDMR_IZBOvzksnArKeFHkzQWA"

# ── Transit helpers ────────────────────────────────────────────────────────────

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
    return ["~#iL", items]

def record(name, value):
    return ["~#iR", tmap("n", name, "v", value)]

def pos(row, col, height, width, container="", screen="queryBuilderPage", row_group="body"):
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

# ── Plugin builders ────────────────────────────────────────────────────────────

def widget(id_, subtype, template, position2, container="", screen="queryBuilderPage"):
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

def query(id_, subtype, template, resource_uuid=None, resource_name=None, screen="queryBuilderPage"):
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

def state_var(id_, value="", persistence="none", screen="queryBuilderPage"):
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

def screen_plugin(id_, title, slug, order, screen_id=None):
    sid = screen_id or id_
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

def btn_tmpl(text, events=None, variant="solid", disabled="", loading="", danger=False):
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

def txt_tmpl(value, overflow="scroll"):
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

def container_tmpl(show_header=False, show_border=True, padding="8px"):
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

def textarea_tmpl(label, placeholder, value="", height_type="fixed"):
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

def textinput_tmpl(label, placeholder, value=""):
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

def table_tmpl(data, columns=None, show_search=True, show_pagination=True, show_filter=True, show_download=True):
    return tom(
        "selectedRowKey", None,
        "showPagination", show_pagination,
        "showSearch", show_search,
        "showFilter", show_filter,
        "showDownload", show_download,
        "showRefresh", True,
        "allowMultiRowSelect", False,
        "data", data,
        "columns", columns or [],
        "events", [],
        "rowHeight", "medium",
        "striped", True,
        "bordered", True,
        "loading", False,
        "hidden", False,
        "maintainSpaceWhenHidden", False
    )

def chart_tmpl(data, chart_type, x_axis, y_axis, title=""):
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

def stat_tmpl(value, caption, format_style="currency"):
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

def modal_tmpl():
    return tom(
        "size", "medium",
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
    )

def date_tmpl(label, value=""):
    return tom(
        "minDate", "",
        "readOnly", False,
        "iconAfter", "",
        "datePlaceholder", "MMM D, YYYY",
        "dateFormat", "MMM d, yyyy",
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

# ── Event handler helper ───────────────────────────────────────────────────────

def evt(event_type, src):
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

# ── SQL Query template helper ──────────────────────────────────────────────────

def sql_tmpl(sql, run_on_load=False, success_msg="", events=None):
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

def js_tmpl(code, run_on_load=False, events=None):
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

def rest_tmpl(method, path, body, headers="", run_on_load=False, events=None):
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

def gsheets_tmpl(spreadsheet_id, sheet_name, run_on_load=False):
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
        "showSuccessToaster", False,
        "runWhenPageLoads", run_on_load,
        "actionType", "read",
        "spreadsheetId", spreadsheet_id,
        "sheetName", sheet_name,
        "servedFromCache", False,
        "events", []
    )

# ═════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPT for Claude
# ═════════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = (
    "You are a PostgreSQL SQL expert. The user has a table called `transactions` "
    "with these columns: date (DATE), description (TEXT), category (TEXT), "
    "amount (NUMERIC, negative=expense positive=income), account (TEXT), "
    "account_number (TEXT), institution (TEXT), month (TEXT), week (TEXT), "
    "transaction_id (TEXT), check_number (TEXT), full_description (TEXT), "
    "labels (TEXT), hide (BOOLEAN). "
    "Return ONLY a JSON object with two fields: "
    '\"sql\": a valid PostgreSQL SELECT query, '
    '\"explanation\": a plain English explanation of what the query does. '
    "No markdown, no code blocks, just raw JSON."
)

REFINE_SYSTEM_PROMPT = (
    "You are a PostgreSQL SQL expert. The user will give you an existing SQL query "
    "and instructions to refine it. The `transactions` table has columns: "
    "date (DATE), description (TEXT), category (TEXT), amount (NUMERIC), "
    "account (TEXT), account_number (TEXT), institution (TEXT), month (TEXT), "
    "week (TEXT), transaction_id (TEXT), check_number (TEXT), full_description (TEXT), "
    "labels (TEXT), hide (BOOLEAN). "
    "Return ONLY a JSON object with two fields: "
    '\"sql\": the refined PostgreSQL SELECT query, '
    '\"explanation\": a plain English explanation. '
    "No markdown, no code blocks, just raw JSON."
)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1: QUERY BUILDER — STATE VARIABLES
# ═════════════════════════════════════════════════════════════════════════════

P1 = "queryBuilderPage"
P2 = "summaryPage"

state_vars = [
    ("currentSQL",
     state_var("currentSQL", "SELECT * FROM transactions ORDER BY date DESC LIMIT 100", "none", P1)),
    ("sqlExplanation",
     state_var("sqlExplanation", "", "none", P1)),
    ("lastSyncTime",
     state_var("lastSyncTime", "", "localStorage", P1)),
    ("syncStatus",
     state_var("syncStatus", "Ready to sync", "none", P1)),
]

# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1: QUERIES
# ═════════════════════════════════════════════════════════════════════════════

queries_p1 = [

    # 1. Fetch from Google Sheets
    ("fetchTransactions",
     query("fetchTransactions", "GoogleSheetsQuery",
           gsheets_tmpl(SPREADSHEET_ID, "Transactions", run_on_load=False),
           GSHEETS_RESOURCE_UUID, GSHEETS_RESOURCE_NAME, P1)),

    # 2. Upsert transactions into Retool DB
    ("upsertTransactions",
     query("upsertTransactions", "SqlQueryUnified",
           sql_tmpl(
               """INSERT INTO transactions (
  date, description, category, amount, account, account_number,
  institution, month, week, transaction_id, check_number,
  full_description, labels, hide, synced_at
) VALUES
{{ fetchTransactions.data.map(r => `(
  '${(r['Date'] || '').replace(/'/g,"''")}',
  '${(r['Description'] || '').replace(/'/g,"''")}',
  '${(r['Category'] || '').replace(/'/g,"''")}',
  ${parseFloat(r['Amount']) || 0},
  '${(r['Account'] || '').replace(/'/g,"''")}',
  '${(r['Account #'] || '').replace(/'/g,"''")}',
  '${(r['Institution'] || '').replace(/'/g,"''")}',
  '${(r['Month'] || '').replace(/'/g,"''")}',
  '${(r['Week'] || '').replace(/'/g,"''")}',
  '${(r['Transaction ID'] || '').replace(/'/g,"''")}',
  '${(r['Check Number'] || '').replace(/'/g,"''")}',
  '${(r['Full Description'] || '').replace(/'/g,"''")}',
  '${(r['Labels'] || '').replace(/'/g,"''")}',
  ${r['Hide'] === 'TRUE' || r['Hide'] === true ? 'true' : 'false'},
  NOW()
)`).join(',\\n') }}
ON CONFLICT (transaction_id) DO UPDATE SET
  date = EXCLUDED.date,
  description = EXCLUDED.description,
  category = EXCLUDED.category,
  amount = EXCLUDED.amount,
  account = EXCLUDED.account,
  account_number = EXCLUDED.account_number,
  institution = EXCLUDED.institution,
  month = EXCLUDED.month,
  week = EXCLUDED.week,
  check_number = EXCLUDED.check_number,
  full_description = EXCLUDED.full_description,
  labels = EXCLUDED.labels,
  hide = EXCLUDED.hide,
  synced_at = NOW()""",
               run_on_load=False,
               success_msg="Sync complete"
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P1)),

    # 3. Sync orchestrator JS
    ("syncToRetoolDB",
     query("syncToRetoolDB", "JavascriptQuery",
           js_tmpl(
               """syncStatus.setValue('Fetching from Google Sheets...');
const sheetData = await fetchTransactions.trigger();
const rows = sheetData || [];
if (!rows.length) {
  syncStatus.setValue('No rows returned from Google Sheets.');
  return { synced: 0 };
}
syncStatus.setValue(`Upserting ${rows.length} rows into Retool DB...`);
await upsertTransactions.trigger();
const now = new Date().toLocaleString();
lastSyncTime.setValue(now);
syncStatus.setValue(`Synced ${rows.length} rows at ${now}`);
utils.showNotification({ title: 'Sync complete', description: `${rows.length} rows upserted`, notificationType: 'success', duration: 4 });
return { synced: rows.length };""",
               run_on_load=False,
               events=[evt("success", "loadSavedViews.trigger()")]
           ),
           None, None, P1)),

    # 4. Load saved views from DB
    ("loadSavedViews",
     query("loadSavedViews", "SqlQueryUnified",
           sql_tmpl("SELECT * FROM saved_views ORDER BY created_at DESC",
                    run_on_load=True),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P1)),

    # 5. Save view to DB
    ("saveViewQuery",
     query("saveViewQuery", "SqlQueryUnified",
           sql_tmpl(
               """INSERT INTO saved_views (name, sql, description)
VALUES ('{{ viewNameInput.value }}', '{{ currentSQL.value.replace(/'/g, "''") }}', '{{ viewDescriptionInput.value.replace(/'/g, "''") }}')
ON CONFLICT (name) DO UPDATE SET
  sql = EXCLUDED.sql,
  description = EXCLUDED.description""",
               run_on_load=False,
               success_msg="View saved",
               events=[evt("success", "loadSavedViews.trigger(); saveViewModal.hide();")]
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P1)),

    # 6. Delete view
    ("deleteViewQuery",
     query("deleteViewQuery", "SqlQueryUnified",
           sql_tmpl(
               "DELETE FROM saved_views WHERE id = {{ savedViewsTable.selectedRow.id }}",
               run_on_load=False,
               success_msg="View deleted",
               events=[evt("success", "loadSavedViews.trigger()")]
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P1)),

    # 7. Load selected view into state
    ("loadViewQuery",
     query("loadViewQuery", "JavascriptQuery",
           js_tmpl(
               """const row = savedViewsTable.selectedRow;
if (!row || !row.sql) throw new Error('No view selected — click a row in the Saved Views table.');
currentSQL.setValue(row.sql);
sqlExplanation.setValue(row.description || '');
utils.showNotification({ title: 'View loaded', description: row.name, notificationType: 'success', duration: 3 });
return row;"""
           ),
           None, None, P1)),

    # 8. Run query results
    ("queryResults",
     query("queryResults", "SqlQueryUnified",
           sql_tmpl("{{ currentSQL.value }}", run_on_load=False),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P1)),

    # 9. Generate SQL via Claude REST
    ("generateSQL",
     query("generateSQL", "RESTQuery",
           rest_tmpl(
               "POST",
               "/v1/messages",
               json.dumps({
                   "model": "claude-sonnet-4-6",
                   "max_tokens": 1024,
                   "system": SYSTEM_PROMPT,
                   "messages": [{"role": "user", "content": "{{ naturalLanguageInput.value }}"}]
               }),
               json.dumps([
                   {"key": "x-api-key", "value": "{{ anthropic_api_key.value }}"},
                   {"key": "anthropic-version", "value": "2023-06-01"},
                   {"key": "content-type", "value": "application/json"}
               ]),
               run_on_load=False,
               events=[evt("success", "parseGeneratedSQL.trigger()"),
                       evt("error", "utils.showNotification({ title: 'Claude API error', description: generateSQL.error?.message || 'Unknown error', notificationType: 'error' })")]
           ),
           CLAUDE_RESOURCE_UUID, CLAUDE_RESOURCE_NAME, P1)),

    # 10. Parse generated SQL response
    ("parseGeneratedSQL",
     query("parseGeneratedSQL", "JavascriptQuery",
           js_tmpl(
               """const raw = generateSQL.data?.content?.[0]?.text || '';
let parsed;
try {
  parsed = JSON.parse(raw);
} catch(e) {
  // try extracting JSON from text
  const match = raw.match(/\\{[\\s\\S]*\\}/);
  if (!match) throw new Error('Could not parse Claude response: ' + raw.substring(0, 200));
  parsed = JSON.parse(match[0]);
}
if (!parsed.sql) throw new Error('No sql field in response');
currentSQL.setValue(parsed.sql);
sqlExplanation.setValue(parsed.explanation || '');
return parsed;"""
           ),
           None, None, P1)),

    # 11. Refine SQL via Claude REST
    ("refineSQL",
     query("refineSQL", "RESTQuery",
           rest_tmpl(
               "POST",
               "/v1/messages",
               json.dumps({
                   "model": "claude-sonnet-4-6",
                   "max_tokens": 1024,
                   "system": REFINE_SYSTEM_PROMPT,
                   "messages": [{"role": "user", "content": "Existing SQL:\\n{{ currentSQL.value }}\\n\\nRefinement instructions:\\n{{ refinementInput.value }}"}]
               }),
               json.dumps([
                   {"key": "x-api-key", "value": "{{ anthropic_api_key.value }}"},
                   {"key": "anthropic-version", "value": "2023-06-01"},
                   {"key": "content-type", "value": "application/json"}
               ]),
               run_on_load=False,
               events=[evt("success", "parseRefinedSQL.trigger()"),
                       evt("error", "utils.showNotification({ title: 'Refine error', description: refineSQL.error?.message || 'Unknown error', notificationType: 'error' })")]
           ),
           CLAUDE_RESOURCE_UUID, CLAUDE_RESOURCE_NAME, P1)),

    # 12. Parse refined SQL response
    ("parseRefinedSQL",
     query("parseRefinedSQL", "JavascriptQuery",
           js_tmpl(
               """const raw = refineSQL.data?.content?.[0]?.text || '';
let parsed;
try {
  parsed = JSON.parse(raw);
} catch(e) {
  const match = raw.match(/\\{[\\s\\S]*\\}/);
  if (!match) throw new Error('Could not parse Claude response: ' + raw.substring(0, 200));
  parsed = JSON.parse(match[0]);
}
if (!parsed.sql) throw new Error('No sql field in response');
currentSQL.setValue(parsed.sql);
sqlExplanation.setValue(parsed.explanation || '');
return parsed;"""
           ),
           None, None, P1)),

    # 13. API key state variable (as a var on P1)
    ("anthropic_api_key",
     state_var("anthropic_api_key", "", "localStorage", P1)),
]

# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1: WIDGETS
# ═════════════════════════════════════════════════════════════════════════════

# Layout:
# row 0-5:   App title + nav button
# row 6-16:  Sync controls bar
# row 18-95: Three columns [left 0-2=w3] [center 3-8=w6] [right 9-11=w3]
# row 97-160: Results area

widgets_p1 = [

    # ── App Title ────────────────────────────────────────────────────────────
    ("appTitle",
     widget("appTitle", "TextWidget2",
            txt_tmpl("# Transaction Query Builder"),
            pos(0, 0, 6, 8, "", P1), "", P1)),

    # Nav to summary page
    ("navToSummaryBtn",
     widget("navToSummaryBtn", "ButtonWidget2",
            btn_tmpl("Summary & Charts", events=[
                evt("click", "utils.openPage('summaryPage', {})")
            ], variant="outline"),
            pos(0, 9, 5, 3, "", P1), "", P1)),

    # ── Sync Controls Bar ────────────────────────────────────────────────────
    ("syncControlsContainer",
     widget("syncControlsContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(7, 0, 11, 12, "", P1), "", P1)),

    ("syncNowButton",
     widget("syncNowButton", "ButtonWidget2",
            btn_tmpl("Sync from Google Sheets", events=[
                evt("click", "syncToRetoolDB.trigger()")
            ]),
            pos(1, 0, 5, 3, "syncControlsContainer", P1),
            "syncControlsContainer", P1)),

    ("apiKeyInput",
     widget("apiKeyInput", "TextInputWidget2",
            textinput_tmpl("Anthropic API Key", "sk-ant-...", "{{ anthropic_api_key.value }}"),
            pos(1, 3, 5, 4, "syncControlsContainer", P1),
            "syncControlsContainer", P1)),

    ("saveApiKeyBtn",
     widget("saveApiKeyBtn", "ButtonWidget2",
            btn_tmpl("Save Key", events=[
                evt("click", "anthropic_api_key.setValue(apiKeyInput.value); utils.showNotification({ title: 'API key saved', notificationType: 'success', duration: 2 })")
            ], variant="outline"),
            pos(1, 7, 5, 2, "syncControlsContainer", P1),
            "syncControlsContainer", P1)),

    ("lastSyncTimeText",
     widget("lastSyncTimeText", "TextWidget2",
            txt_tmpl("**Last synced:** {{ lastSyncTime.value || 'Never' }}"),
            pos(6, 0, 4, 5, "syncControlsContainer", P1),
            "syncControlsContainer", P1)),

    ("syncStatusText",
     widget("syncStatusText", "TextWidget2",
            txt_tmpl("{{ syncStatus.value }}"),
            pos(6, 5, 4, 7, "syncControlsContainer", P1),
            "syncControlsContainer", P1)),

    # ── Left Sidebar: Saved Views ────────────────────────────────────────────
    ("leftSidebarContainer",
     widget("leftSidebarContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(20, 0, 80, 3, "", P1), "", P1)),

    ("savedViewsTitle",
     widget("savedViewsTitle", "TextWidget2",
            txt_tmpl("#### Saved Views"),
            pos(0, 0, 4, 12, "leftSidebarContainer", P1),
            "leftSidebarContainer", P1)),

    ("savedViewsTable",
     widget("savedViewsTable", "TableWidget2",
            table_tmpl(
                "{{ loadSavedViews.data }}",
                columns=[
                    tmap("id", "name", "label", "Name", "dataIndex", "name", "hidden", False),
                    tmap("id", "description", "label", "Description", "dataIndex", "description", "hidden", False),
                ],
                show_search=True,
                show_pagination=False,
                show_filter=False,
                show_download=False
            ),
            pos(5, 0, 40, 12, "leftSidebarContainer", P1),
            "leftSidebarContainer", P1)),

    ("loadViewButton",
     widget("loadViewButton", "ButtonWidget2",
            btn_tmpl("Load Selected View", events=[
                evt("click", "loadViewQuery.trigger()")
            ]),
            pos(46, 0, 5, 12, "leftSidebarContainer", P1),
            "leftSidebarContainer", P1)),

    ("saveViewButton",
     widget("saveViewButton", "ButtonWidget2",
            btn_tmpl("Save Current View", events=[
                evt("click", "saveViewModal.show()")
            ], variant="outline"),
            pos(52, 0, 5, 12, "leftSidebarContainer", P1),
            "leftSidebarContainer", P1)),

    ("deleteViewButton",
     widget("deleteViewButton", "ButtonWidget2",
            btn_tmpl("Delete View", events=[
                evt("click", "deleteViewQuery.trigger()")
            ], danger=True),
            pos(58, 0, 5, 12, "leftSidebarContainer", P1),
            "leftSidebarContainer", P1)),

    # ── Center: Query Builder ────────────────────────────────────────────────
    ("centerQueryContainer",
     widget("centerQueryContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(20, 3, 80, 6, "", P1), "", P1)),

    ("queryBuilderTitle",
     widget("queryBuilderTitle", "TextWidget2",
            txt_tmpl("#### Query Builder"),
            pos(0, 0, 4, 12, "centerQueryContainer", P1),
            "centerQueryContainer", P1)),

    ("naturalLanguageInput",
     widget("naturalLanguageInput", "TextAreaWidget",
            textarea_tmpl("Natural Language", "Describe what you want to see, e.g. 'Show me all expenses over $100 last month grouped by category'"),
            pos(5, 0, 8, 12, "centerQueryContainer", P1),
            "centerQueryContainer", P1)),

    ("generateSQLButton",
     widget("generateSQLButton", "ButtonWidget2",
            btn_tmpl("Generate SQL with AI", events=[
                evt("click", "generateSQL.trigger()")
            ]),
            pos(14, 0, 5, 6, "centerQueryContainer", P1),
            "centerQueryContainer", P1)),

    ("runQueryButton",
     widget("runQueryButton", "ButtonWidget2",
            btn_tmpl("Run Query", events=[
                evt("click", "queryResults.trigger()")
            ]),
            pos(14, 6, 5, 6, "centerQueryContainer", P1),
            "centerQueryContainer", P1)),

    ("sqlTextArea",
     widget("sqlTextArea", "TextAreaWidget",
            textarea_tmpl("SQL", "SQL query will appear here...", "{{ currentSQL.value }}"),
            pos(20, 0, 14, 12, "centerQueryContainer", P1),
            "centerQueryContainer", P1)),

    ("explanationText",
     widget("explanationText", "TextWidget2",
            txt_tmpl("{{ sqlExplanation.value ? '**Explanation:** ' + sqlExplanation.value : '_AI explanation will appear here_' }}"),
            pos(35, 0, 6, 12, "centerQueryContainer", P1),
            "centerQueryContainer", P1)),

    ("updateSQLButton",
     widget("updateSQLButton", "ButtonWidget2",
            btn_tmpl("Apply Edited SQL", events=[
                evt("click", "currentSQL.setValue(sqlTextArea.value)")
            ], variant="outline"),
            pos(42, 0, 5, 12, "centerQueryContainer", P1),
            "centerQueryContainer", P1)),

    # ── Right Sidebar: AI Refinement ────────────────────────────────────────
    ("rightSidebarContainer",
     widget("rightSidebarContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(20, 9, 80, 3, "", P1), "", P1)),

    ("aiRefinementTitle",
     widget("aiRefinementTitle", "TextWidget2",
            txt_tmpl("#### AI Refinement"),
            pos(0, 0, 4, 12, "rightSidebarContainer", P1),
            "rightSidebarContainer", P1)),

    ("refinementInstructions",
     widget("refinementInstructions", "TextWidget2",
            txt_tmpl("_Describe how to change the current SQL query:_"),
            pos(5, 0, 4, 12, "rightSidebarContainer", P1),
            "rightSidebarContainer", P1)),

    ("refinementInput",
     widget("refinementInput", "TextAreaWidget",
            textarea_tmpl("", "e.g. 'Also group by account', 'Limit to last 30 days', 'Sort by amount descending'"),
            pos(10, 0, 15, 12, "rightSidebarContainer", P1),
            "rightSidebarContainer", P1)),

    ("refineButton",
     widget("refineButton", "ButtonWidget2",
            btn_tmpl("Refine with AI", events=[
                evt("click", "refineSQL.trigger()")
            ]),
            pos(26, 0, 5, 12, "rightSidebarContainer", P1),
            "rightSidebarContainer", P1)),

    # ── Results ──────────────────────────────────────────────────────────────
    ("resultsContainer",
     widget("resultsContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(102, 0, 70, 12, "", P1), "", P1)),

    ("resultsHeader",
     widget("resultsHeader", "TextWidget2",
            txt_tmpl("#### Results"),
            pos(0, 0, 4, 8, "resultsContainer", P1),
            "resultsContainer", P1)),

    ("rowCountText",
     widget("rowCountText", "TextWidget2",
            txt_tmpl("{{ queryResults.data ? queryResults.data.length + ' rows' : '' }}"),
            pos(0, 8, 4, 4, "resultsContainer", P1),
            "resultsContainer", P1)),

    ("resultsTable",
     widget("resultsTable", "TableWidget2",
            table_tmpl(
                "{{ queryResults.data }}",
                show_search=True,
                show_pagination=True,
                show_filter=True,
                show_download=True
            ),
            pos(5, 0, 60, 12, "resultsContainer", P1),
            "resultsContainer", P1)),

    # ── Save View Modal ───────────────────────────────────────────────────────
    ("saveViewModal",
     widget("saveViewModal", "ModalFrameWidget",
            modal_tmpl(),
            pos(0, 0, 0, 12, "", P1), "", P1)),

    ("saveViewModalTitle",
     widget("saveViewModalTitle", "TextWidget2",
            txt_tmpl("#### Save Current View"),
            pos(0, 0, 4, 12, "saveViewModal", P1),
            "saveViewModal", P1)),

    ("viewNameInput",
     widget("viewNameInput", "TextInputWidget2",
            textinput_tmpl("View Name", "e.g. Monthly Groceries"),
            pos(5, 0, 5, 12, "saveViewModal", P1),
            "saveViewModal", P1)),

    ("viewDescriptionInput",
     widget("viewDescriptionInput", "TextAreaWidget",
            textarea_tmpl("Description (optional)", "Describe what this view shows..."),
            pos(11, 0, 8, 12, "saveViewModal", P1),
            "saveViewModal", P1)),

    ("cancelSaveButton",
     widget("cancelSaveButton", "ButtonWidget2",
            btn_tmpl("Cancel", events=[
                evt("click", "saveViewModal.hide()")
            ], variant="outline"),
            pos(20, 0, 5, 6, "saveViewModal", P1),
            "saveViewModal", P1)),

    ("saveViewSubmitButton",
     widget("saveViewSubmitButton", "ButtonWidget2",
            btn_tmpl("Save View", events=[
                evt("click", "saveViewQuery.trigger()")
            ]),
            pos(20, 6, 5, 6, "saveViewModal", P1),
            "saveViewModal", P1)),
]

# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2: SUMMARY — QUERIES
# ═════════════════════════════════════════════════════════════════════════════

queries_p2 = [

    ("spendingByCategory",
     query("spendingByCategory", "SqlQueryUnified",
           sql_tmpl(
               """SELECT category, ROUND(ABS(SUM(amount))::numeric, 2) AS total_spent, COUNT(*) AS num_transactions
FROM transactions
WHERE amount < 0
  AND date >= '{{ startDateFilter.value || '2020-01-01' }}'
  AND date <= '{{ endDateFilter.value || NOW() }}'
  AND hide = false
GROUP BY category
ORDER BY total_spent DESC""",
               run_on_load=True
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P2)),

    ("monthlyTrend",
     query("monthlyTrend", "SqlQueryUnified",
           sql_tmpl(
               """SELECT
  TO_CHAR(DATE_TRUNC('month', date), 'YYYY-MM') AS month_label,
  ROUND(ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END))::numeric, 2) AS expenses,
  ROUND(SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END)::numeric, 2) AS income
FROM transactions
WHERE date >= '{{ startDateFilter.value || '2020-01-01' }}'
  AND date <= '{{ endDateFilter.value || NOW() }}'
  AND hide = false
GROUP BY DATE_TRUNC('month', date)
ORDER BY DATE_TRUNC('month', date)""",
               run_on_load=True
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P2)),

    ("topMerchants",
     query("topMerchants", "SqlQueryUnified",
           sql_tmpl(
               """SELECT description, COUNT(*) AS num_transactions,
  ROUND(ABS(SUM(amount))::numeric, 2) AS total_spent
FROM transactions
WHERE amount < 0
  AND date >= '{{ startDateFilter.value || '2020-01-01' }}'
  AND date <= '{{ endDateFilter.value || NOW() }}'
  AND hide = false
GROUP BY description
ORDER BY total_spent DESC
LIMIT 20""",
               run_on_load=True
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P2)),

    ("incomeVsExpenses",
     query("incomeVsExpenses", "SqlQueryUnified",
           sql_tmpl(
               """SELECT
  ROUND(SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END)::numeric, 2) AS total_income,
  ROUND(ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END))::numeric, 2) AS total_expenses,
  ROUND(SUM(amount)::numeric, 2) AS net
FROM transactions
WHERE date >= '{{ startDateFilter.value || '2020-01-01' }}'
  AND date <= '{{ endDateFilter.value || NOW() }}'
  AND hide = false""",
               run_on_load=True
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P2)),

    ("spendingByInstitution",
     query("spendingByInstitution", "SqlQueryUnified",
           sql_tmpl(
               """SELECT institution, ROUND(ABS(SUM(amount))::numeric, 2) AS total_spent
FROM transactions
WHERE amount < 0
  AND date >= '{{ startDateFilter.value || '2020-01-01' }}'
  AND date <= '{{ endDateFilter.value || NOW() }}'
  AND hide = false
GROUP BY institution
ORDER BY total_spent DESC""",
               run_on_load=True
           ),
           RETOOL_DB_UUID, RETOOL_DB_NAME, P2)),
]

# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2: WIDGETS
# ═════════════════════════════════════════════════════════════════════════════

widgets_p2 = [

    # Title + nav
    ("summaryTitle",
     widget("summaryTitle", "TextWidget2",
            txt_tmpl("# Summary & Charts"),
            pos(0, 0, 6, 8, "", P2), "", P2)),

    ("navToQueryBtn",
     widget("navToQueryBtn", "ButtonWidget2",
            btn_tmpl("Query Builder", events=[
                evt("click", "utils.openPage('queryBuilderPage', {})")
            ], variant="outline"),
            pos(0, 9, 5, 3, "", P2), "", P2)),

    # Date filter bar
    ("dateFilterContainer",
     widget("dateFilterContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(7, 0, 11, 12, "", P2), "", P2)),

    ("startDateFilter",
     widget("startDateFilter", "DateWidget",
            date_tmpl("From", "{{ new Date(new Date().setFullYear(new Date().getFullYear() - 1)) }}"),
            pos(1, 0, 5, 3, "dateFilterContainer", P2),
            "dateFilterContainer", P2)),

    ("endDateFilter",
     widget("endDateFilter", "DateWidget",
            date_tmpl("To", "{{ new Date() }}"),
            pos(1, 3, 5, 3, "dateFilterContainer", P2),
            "dateFilterContainer", P2)),

    ("applyFiltersBtn",
     widget("applyFiltersBtn", "ButtonWidget2",
            btn_tmpl("Apply Date Filter", events=[
                evt("click", "spendingByCategory.trigger(); monthlyTrend.trigger(); topMerchants.trigger(); incomeVsExpenses.trigger(); spendingByInstitution.trigger()")
            ]),
            pos(1, 6, 5, 3, "dateFilterContainer", P2),
            "dateFilterContainer", P2)),

    # Stat cards
    ("statsContainer",
     widget("statsContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=False, padding="4px"),
            pos(20, 0, 14, 12, "", P2), "", P2)),

    ("totalIncomeWidget",
     widget("totalIncomeWidget", "StatisticWidget2",
            stat_tmpl(
                "{{ incomeVsExpenses.data?.[0]?.total_income || 0 }}",
                "Total Income"
            ),
            pos(0, 0, 12, 4, "statsContainer", P2),
            "statsContainer", P2)),

    ("totalExpensesWidget",
     widget("totalExpensesWidget", "StatisticWidget2",
            stat_tmpl(
                "{{ incomeVsExpenses.data?.[0]?.total_expenses || 0 }}",
                "Total Expenses"
            ),
            pos(0, 4, 12, 4, "statsContainer", P2),
            "statsContainer", P2)),

    ("netWidget",
     widget("netWidget", "StatisticWidget2",
            stat_tmpl(
                "{{ incomeVsExpenses.data?.[0]?.net || 0 }}",
                "Net"
            ),
            pos(0, 8, 12, 4, "statsContainer", P2),
            "statsContainer", P2)),

    # Spending by category (bar chart)
    ("categoryChartContainer",
     widget("categoryChartContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(36, 0, 50, 6, "", P2), "", P2)),

    ("categoryChartTitle",
     widget("categoryChartTitle", "TextWidget2",
            txt_tmpl("#### Spending by Category"),
            pos(0, 0, 4, 12, "categoryChartContainer", P2),
            "categoryChartContainer", P2)),

    ("categoryChart",
     widget("categoryChart", "ChartWidget2",
            chart_tmpl(
                "{{ spendingByCategory.data }}",
                "bar",
                "category",
                "total_spent"
            ),
            pos(5, 0, 40, 12, "categoryChartContainer", P2),
            "categoryChartContainer", P2)),

    # Monthly trend (line chart)
    ("monthlyTrendContainer",
     widget("monthlyTrendContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(36, 6, 50, 6, "", P2), "", P2)),

    ("monthlyTrendTitle",
     widget("monthlyTrendTitle", "TextWidget2",
            txt_tmpl("#### Monthly Spending Trend"),
            pos(0, 0, 4, 12, "monthlyTrendContainer", P2),
            "monthlyTrendContainer", P2)),

    ("monthlyTrendChart",
     widget("monthlyTrendChart", "ChartWidget2",
            chart_tmpl(
                "{{ monthlyTrend.data }}",
                "line",
                "month_label",
                "expenses"
            ),
            pos(5, 0, 40, 12, "monthlyTrendContainer", P2),
            "monthlyTrendContainer", P2)),

    # Top merchants table
    ("topMerchantsContainer",
     widget("topMerchantsContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(88, 0, 55, 6, "", P2), "", P2)),

    ("topMerchantsTitle",
     widget("topMerchantsTitle", "TextWidget2",
            txt_tmpl("#### Top 20 Merchants"),
            pos(0, 0, 4, 12, "topMerchantsContainer", P2),
            "topMerchantsContainer", P2)),

    ("topMerchantsTable",
     widget("topMerchantsTable", "TableWidget2",
            table_tmpl("{{ topMerchants.data }}", show_filter=False, show_download=True),
            pos(5, 0, 45, 12, "topMerchantsContainer", P2),
            "topMerchantsContainer", P2)),

    # By institution bar chart
    ("institutionChartContainer",
     widget("institutionChartContainer", "ContainerWidget2",
            container_tmpl(show_header=False, show_border=True, padding="8px"),
            pos(88, 6, 55, 6, "", P2), "", P2)),

    ("institutionChartTitle",
     widget("institutionChartTitle", "TextWidget2",
            txt_tmpl("#### Spending by Institution"),
            pos(0, 0, 4, 12, "institutionChartContainer", P2),
            "institutionChartContainer", P2)),

    ("institutionChart",
     widget("institutionChart", "ChartWidget2",
            chart_tmpl(
                "{{ spendingByInstitution.data }}",
                "bar",
                "institution",
                "total_spent"
            ),
            pos(5, 0, 40, 12, "institutionChartContainer", P2),
            "institutionChartContainer", P2)),
]

# ═════════════════════════════════════════════════════════════════════════════
# SCREENS & FRAMES
# ═════════════════════════════════════════════════════════════════════════════

screens_and_frames = [
    (P1, screen_plugin(P1, "Query Builder", "query-builder", 0)),
    (P1 + "_main", frame_plugin(P1 + "_main", P1, "main")),
    (P2, screen_plugin(P2, "Summary & Charts", "summary", 1)),
    (P2 + "_main", frame_plugin(P2 + "_main", P2, "main")),
]

# ═════════════════════════════════════════════════════════════════════════════
# ASSEMBLE APP STATE
# ═════════════════════════════════════════════════════════════════════════════

def build_plugins_om():
    """Build the ordered map of all plugins."""
    all_plugins = (
        screens_and_frames
        + [(k, v) for k, v in state_vars]
        + [(k, v) for k, v in queries_p1]
        + [(k, v) for k, v in widgets_p1]
        + [(k, v) for k, v in queries_p2]
        + [(k, v) for k, v in widgets_p2]
    )
    flat = []
    for id_, plugin_val in all_plugins:
        flat.append(id_)
        flat.append(plugin_val)
    return ["~#iOM", flat]

def build_app_state():
    plugins_om = build_plugins_om()

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
        "theme", tmap(
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
    )

    return record("appTemplate", app_template)

def main():
    app_state_obj = build_app_state()
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
            "createdAt": "2026-03-07T00:00:00.000Z",
            "updatedAt": "2026-03-07T00:00:00.000Z",
            "pageId": 999999,
            "userId": 0
        },
        "modules": {}
    }

    out_path = os.path.join(os.path.dirname(__file__), "tiller-dashboard-v2.json")
    with open(out_path, "w") as f:
        json.dump(retool_json, f, indent=2)

    print(f"✓ Generated: {out_path}")
    print(f"  App state size: {len(app_state_str):,} bytes")
    print(f"  Total plugins: {len(screens_and_frames) + len(state_vars) + len(queries_p1) + len(widgets_p1) + len(queries_p2) + len(widgets_p2)}")

if __name__ == "__main__":
    main()
