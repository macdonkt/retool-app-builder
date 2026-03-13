#!/usr/bin/env python3
"""
Retool Transit Core Library — Slim Primitives Only

Provides Transit encoding primitives, positioning, plugin builders, event helpers,
and app envelope functions. NO widget/query template factories.

For widget/query field structures, read transit_patterns.json and copy the exact
fields from the golden reference, modifying only what needs to differ.

Usage:
    from tools.retool_core import *

    # Read transit_patterns.json for the exact ButtonWidget2 template fields
    # Copy those fields into a tmap(), changing only text, events, etc.

    plugins = [
        ("page1", screen_plugin("page1", "My App", "my-app", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),
        ("title", widget("title", "TextWidget2",
            tom("heightType", "auto", "value", "# Hello", ...all fields from reference...),
            pos(0, 0, 4, 12, "$main", "page1"),
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
    """Transit map: ["^ ", k1, v1, k2, v2, ...]
    Decodes to a plain JS Object {}. Does NOT have .get() method."""
    result = ["^ "]
    for i in range(0, len(args), 2):
        result.append(args[i])
        result.append(args[i + 1])
    return result


def tom(*args):
    """Transit ordered map: ["~#iOM", [k1, v1, k2, v2, ...]]
    Decodes to OrderedMap. HAS .get() method.
    REQUIRED for: event handlers, template fields that Retool calls .get() on."""
    flat = []
    for i in range(0, len(args), 2):
        flat.append(args[i])
        flat.append(args[i + 1])
    return ["~#iOM", flat]


def tlist(items):
    """Transit list: ["~#iL", [...]]
    Decodes to Transit List with .toArray() method.
    REQUIRED for: _columnIds, _actionIds, _toolbarButtonIds, _groupByColumns, events."""
    return ["~#iL", items]


def record(name, value):
    """Transit record: ["~#iR", ["^ ", "n", name, "v", value]]"""
    return ["~#iR", tmap("n", name, "v", value)]


# ══════════════════════════════════════════════════════════════════════════════
# POSITION BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def pos(row, col, height, width, container="", screen="page1", row_group="body"):
    """Build a position2 record for grid placement.

    container: For widgets on the main page, use "" (empty string).
               For widgets inside a modal/drawer/container, pass the parent frame ID
               — it goes into 'subcontainer', NOT 'container'.
    """
    return record("position2", tmap(
        "type", "grid",
        "container", "",
        "rowGroup", row_group,
        "subcontainer", container,
        "row", row,
        "col", col,
        "height", height,
        "width", width,
        "tabNum", 0,
        "stackPosition", None
    ))


# ══════════════════════════════════════════════════════════════════════════════
# PLUGIN BUILDERS (generic wrappers — no template logic)
# ══════════════════════════════════════════════════════════════════════════════

def widget(id_, subtype, template, position2, container="", screen="page1"):
    """Build a widget plugin record.

    template: a tom() with ALL fields from transit_patterns.json for this subtype.
    position2: from pos() helper.
    """
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
        "style", tom(),
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


def query(id_, subtype, template, resource_uuid=None, resource_name=None, screen=None):
    """Build a query (datasource) plugin record.

    template: a tom() with ALL fields from transit_patterns.json for this subtype.
    For JS queries: resource_uuid auto-set to "JavascriptQuery".
    For SQL queries: pass resource_uuid=<DB UUID>, resource_name="retool_db".
    screen=None for global queries, screen="page1" for page-scoped.
    """
    if subtype == "JavascriptQuery" and resource_uuid is None:
        resource_uuid = "JavascriptQuery"
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", None,
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
        "container", "",
        "createdAt", TS,
        "updatedAt", TS,
        "folder", "",
        "presetName", None,
        "screen", screen,
        "boxId", None,
        "subBoxIds", None
    ))


def state_var(id_, value="", screen=None):
    """Build a state variable plugin record.
    screen=None for global, screen="page1" for page-scoped."""
    return record("pluginTemplate", tmap(
        "id", id_,
        "uuid", None,
        "_comment", None,
        "type", "state",
        "subtype", "State",
        "namespace", None,
        "resourceName", None,
        "resourceDisplayName", None,
        "template", tom("value", value),
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
    """Build a frame plugin record (main content frame)."""
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
        "style", tom(),
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
            "events", tlist([])
        ),
        "style", tom(),
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
            "events", tlist([])
        ),
        "style", tom(),
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
# EVENT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def evt(event_type, src):
    """Generic event handler that runs a JavaScript src string."""
    return tom(
        "id", str(uuid.uuid4()),
        "type", "widget",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "run",
        "pluginId", "",
        "targetId", None,
        "params", tom("src", src)
    )


def evt_trigger_query(event_type, query_id):
    """Event handler that triggers a named query."""
    return tom(
        "id", str(uuid.uuid4()),
        "type", "datasource",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "trigger",
        "pluginId", query_id,
        "targetId", None,
        "params", tom()
    )


def evt_show_frame(event_type, frame_id):
    """Event handler that shows a modal/drawer."""
    return tom(
        "id", str(uuid.uuid4()),
        "type", "widget",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "show",
        "pluginId", frame_id,
        "targetId", None,
        "params", tom()
    )


def evt_hide_frame(event_type, frame_id):
    """Event handler that hides a modal/drawer."""
    return tom(
        "id", str(uuid.uuid4()),
        "type", "widget",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "hide",
        "pluginId", frame_id,
        "targetId", None,
        "params", tom()
    )


def evt_set_var(event_type, var_id, value_expr):
    """Event handler that sets a state variable."""
    return tom(
        "id", str(uuid.uuid4()),
        "type", "state",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "setValue",
        "pluginId", var_id,
        "targetId", None,
        "params", tom("value", value_expr)
    )


def evt_notification(event_type, notif_type="success", title="", description="", duration=4.5):
    """Event handler that shows a notification toast."""
    return tom(
        "id", str(uuid.uuid4()),
        "type", "util",
        "waitMs", "0",
        "waitType", "debounce",
        "event", event_type,
        "method", "showNotification",
        "pluginId", "",
        "targetId", None,
        "params", tom(
            "options", tom(
                "notificationType", notif_type,
                "title", title,
                "description", description,
                "duration", duration
            )
        )
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
    screen_ids = []
    for id_, plugin_val in plugins:
        flat.append(id_)
        flat.append(plugin_val)
        # Detect screen plugins to derive rootScreen and pageCodeFolders
        try:
            plugin_tmap = plugin_val[1][4]  # navigate into record -> tmap
            pairs = plugin_tmap[1:]  # skip "^ "
            for i in range(0, len(pairs), 2):
                if pairs[i] == "type" and pairs[i + 1] == "screen":
                    screen_ids.append(id_)
                    break
        except (IndexError, TypeError):
            pass
    plugins_om = ["~#iOM", flat]

    root_screen = screen_ids[0] if screen_ids else "page1"

    # Build pageCodeFolders: tmap with each screen -> empty list
    pcf_args = []
    for sid in screen_ids:
        pcf_args.extend([sid, []])
    page_code_folders = tmap(*pcf_args) if pcf_args else tmap("page1", [])

    app_template = tmap(
        "agentEvals", tmap(),
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
        "mobileOfflineAssets", [],
        "multiScreenMobileApp", False,
        "notificationsSettings", tmap(
            "globalQueryShowFailureToast", True,
            "globalQueryShowSuccessToast", False,
            "globalQueryToastDuration", 4.5,
            "globalToastPosition", "bottomRight"
        ),
        "pageCodeFolders", page_code_folders,
        "pageLoadValueOverrides", tlist([]),
        "persistUrlParams", False,
        "plugins", plugins_om,
        "preloadedAppJSLinks", [],
        "preloadedAppJavaScript", None,
        "queryStatusVisibility", False,
        "responsiveLayoutDisabled", False,
        "rootScreen", root_screen,
        "savePlatform", "web",
        "serializedLayout", None,
        "shortlink", None,
        "testEntities", [],
        "tests", [],
        "urlFragmentDefinitions", tlist([]),
        "version", "3.355.0"
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
    # Find plugin count
    tmap_pairs = app_state_obj[1][4][1:]  # skip '^ '
    plugin_count = 0
    for i in range(0, len(tmap_pairs), 2):
        if tmap_pairs[i] == "plugins":
            iom_items = tmap_pairs[i + 1][1]
            plugin_count = len(iom_items) // 2
            break
    print(f"  Total plugins: {plugin_count}")

    return output_path
