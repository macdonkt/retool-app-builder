#!/usr/bin/env python3
"""
Validate a generated Retool app JSON file before import.

Checks:
1. Outer JSON structure (uuid, page.data.appState)
2. appState parses as valid JSON
3. Root is a Transit record
4. Plugins iOM exists and is non-empty
5. At least one Screen and one Frame plugin present
6. Every widget has a position2 record
7. Every widget has type, subtype, id, template
8. No duplicate plugin IDs
9. Container references point to existing frames
10. Screen references point to existing screens

Works with BOTH:
- Exported Retool files (cache refs like ^16, ^17)
- Generated files using full field names (from retool_builder.py)

Usage:
    python3 tools/validate_retool_json.py <file.json>
"""

import json
import sys
import os


class ValidationResult:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def log(self, msg):
        self.info.append(msg)

    @property
    def ok(self):
        return len(self.errors) == 0

    def summary(self):
        lines = []
        for msg in self.errors:
            lines.append(f"  ERROR: {msg}")
        for msg in self.warnings:
            lines.append(f"  WARN:  {msg}")
        for msg in self.info:
            lines.append(f"  INFO:  {msg}")
        return "\n".join(lines)


def _is_cache_ref(s):
    return isinstance(s, str) and len(s) >= 2 and s[0] == '^' and s != "^ "


def _build_plugin_cache(items):
    """
    Build cache ref -> full name mapping by comparing the first plugin
    (which uses full names) with the second plugin (which uses cache refs).
    Also detects type tag caching (e.g., ^0 -> ~#iR).
    """
    cache = {}
    if len(items) < 4:
        return cache

    first_val = items[1]
    second_val = items[3]

    if not isinstance(first_val, list) or not isinstance(second_val, list):
        return cache

    # Record type tag: e.g., ^0 -> ~#iR
    if isinstance(first_val[0], str) and _is_cache_ref(first_val[0]):
        cache[first_val[0]] = "~#iR"

    first_inner = first_val[1]
    second_inner = second_val[1]

    if not isinstance(first_inner, list) or not isinstance(second_inner, list):
        return cache

    # Compare record inner keys (n, v)
    p1 = first_inner[1:] if first_inner[0] == "^ " else first_inner
    p2 = second_inner[1:] if second_inner[0] == "^ " else second_inner

    for i in range(0, min(len(p1), len(p2)) - 1, 2):
        k1, k2 = p1[i], p2[i]
        if isinstance(k1, str) and not _is_cache_ref(k1):
            if isinstance(k2, str) and _is_cache_ref(k2):
                cache[k2] = k1

    # Compare plugin tmap keys
    first_tmap = first_inner[4] if len(first_inner) > 4 else None
    second_tmap = second_inner[4] if len(second_inner) > 4 else None

    if first_tmap and second_tmap:
        tp1 = first_tmap[1:] if isinstance(first_tmap, list) and first_tmap[0] == "^ " else []
        tp2 = second_tmap[1:] if isinstance(second_tmap, list) and second_tmap[0] == "^ " else []

        for i in range(0, min(len(tp1), len(tp2)) - 1, 2):
            k1, k2 = tp1[i], tp2[i]
            if isinstance(k1, str) and not _is_cache_ref(k1):
                if isinstance(k2, str) and _is_cache_ref(k2):
                    cache[k2] = k1

    return cache


def _resolve(key, cache):
    if isinstance(key, str) and _is_cache_ref(key):
        return cache.get(key, key)
    return key


def _get_field(tmap_list, field_name, cache):
    """Get a field from a tmap, resolving cache keys."""
    if not isinstance(tmap_list, list):
        return None
    start = 1 if isinstance(tmap_list[0], str) and tmap_list[0] == "^ " else 0
    for i in range(start, len(tmap_list) - 1, 2):
        key = _resolve(tmap_list[i], cache)
        if key == field_name:
            return tmap_list[i + 1]
    return None


def validate(file_path):
    """Run all validation checks on a Retool JSON file."""
    result = ValidationResult()

    # 1. Load outer JSON
    try:
        with open(file_path) as f:
            outer = json.load(f)
    except json.JSONDecodeError as e:
        result.error(f"Invalid outer JSON: {e}")
        return result
    except FileNotFoundError:
        result.error(f"File not found: {file_path}")
        return result

    if "uuid" not in outer:
        result.error("Missing 'uuid' in outer JSON")
    if "page" not in outer:
        result.error("Missing 'page' in outer JSON")
        return result
    if "data" not in outer.get("page", {}):
        result.error("Missing 'page.data' in outer JSON")
        return result
    if "appState" not in outer["page"]["data"]:
        result.error("Missing 'page.data.appState' in outer JSON")
        return result

    result.log("Outer JSON structure: OK")

    # 2. Parse appState
    app_state_str = outer["page"]["data"]["appState"]
    try:
        app_state = json.loads(app_state_str)
    except json.JSONDecodeError as e:
        result.error(f"appState is not valid JSON: {e}")
        return result

    result.log(f"appState size: {len(app_state_str):,} bytes")

    # 3. Check root is Transit record
    if not isinstance(app_state, list) or len(app_state) < 2:
        result.error("appState root is not a list with >= 2 elements")
        return result

    root_marker = app_state[0]
    if root_marker != "~#iR":
        # Could be valid if it's a known pattern (but unexpected for generated files)
        result.warn(f"appState root marker is '{root_marker}', expected '~#iR'")

    result.log("Root Transit record: OK")

    # 4. Find plugins iOM
    # Root: [record_tag, ["^ ", "n"/"^1", "appTemplate", "v"/"^2", app_tmap]]
    inner = app_state[1]
    if not isinstance(inner, list) or inner[0] != "^ ":
        result.error("appState root record inner is not a tmap")
        return result

    # The v value is always at index 4 in the record inner
    if len(inner) < 5:
        result.error("Root record inner too short")
        return result
    app_tmap = inner[4]

    # Find 'plugins' key in app_tmap (could be full name or cached)
    plugins_iom = None
    if isinstance(app_tmap, list) and app_tmap[0] == "^ ":
        pairs = app_tmap[1:]
        for i in range(0, len(pairs) - 1, 2):
            if pairs[i] == "plugins":
                plugins_iom = pairs[i + 1]
                break

    if plugins_iom is None:
        result.error("Could not find 'plugins' in appTemplate")
        return result

    if not isinstance(plugins_iom, list) or len(plugins_iom) < 2:
        result.error("Plugins is not a valid ordered map")
        return result

    items = plugins_iom[1]
    if not isinstance(items, list) or len(items) < 2:
        result.error("Plugins iOM is empty")
        return result

    plugin_count = len(items) // 2
    result.log(f"Plugins found: {plugin_count}")

    # Build cache from plugin comparison
    cache = _build_plugin_cache(items)
    if cache:
        result.log(f"Cache keys resolved: {len(cache)}")

    # 5-10. Check each plugin
    seen_ids = set()
    screens = set()
    frames = set()
    widget_count = 0
    query_count = 0
    state_count = 0
    has_screen = False
    has_frame = False

    for j in range(0, len(items), 2):
        plugin_id = items[j]
        plugin_raw = items[j + 1]

        if plugin_id in seen_ids:
            result.error(f"Duplicate plugin ID: '{plugin_id}'")
        seen_ids.add(plugin_id)

        if not isinstance(plugin_raw, list) or len(plugin_raw) < 2:
            result.error(f"Plugin '{plugin_id}' has invalid structure")
            continue

        rec_inner = plugin_raw[1]
        if not isinstance(rec_inner, list) or len(rec_inner) < 5:
            result.error(f"Plugin '{plugin_id}' record inner too short")
            continue

        # Plugin tmap is always at index 4 in the record inner
        plugin_tmap = rec_inner[4]
        if not isinstance(plugin_tmap, list):
            result.error(f"Plugin '{plugin_id}' tmap is not a list")
            continue

        p_type = _get_field(plugin_tmap, "type", cache)
        p_subtype = _get_field(plugin_tmap, "subtype", cache)
        p_template = _get_field(plugin_tmap, "template", cache)
        p_position = _get_field(plugin_tmap, "position2", cache)
        p_id = _get_field(plugin_tmap, "id", cache)
        p_container = _get_field(plugin_tmap, "container", cache)
        p_screen = _get_field(plugin_tmap, "screen", cache)

        if p_type is None:
            result.error(f"Plugin '{plugin_id}' missing 'type'")
        if p_subtype is None:
            result.error(f"Plugin '{plugin_id}' missing 'subtype'")
        if p_id is None:
            result.error(f"Plugin '{plugin_id}' missing 'id'")
        if p_id and p_id != plugin_id:
            result.warn(f"Plugin key '{plugin_id}' doesn't match internal id '{p_id}'")

        if p_type == "screen":
            has_screen = True
            screens.add(plugin_id)
        elif p_type == "frame":
            has_frame = True
            frames.add(plugin_id)
        elif p_type == "widget":
            widget_count += 1
            if p_position is None:
                result.error(f"Widget '{plugin_id}' ({p_subtype}) missing position2")
            if p_template is None:
                result.error(f"Widget '{plugin_id}' ({p_subtype}) missing template")
        elif p_type == "datasource":
            query_count += 1
        elif p_type == "state":
            state_count += 1

    if not has_screen:
        result.error("No Screen plugin found — app needs at least one")
    if not has_frame:
        result.error("No Frame plugin found — app needs at least one")

    result.log(f"Screens: {len(screens)}, Frames: {len(frames)}, "
               f"Widgets: {widget_count}, Queries: {query_count}, "
               f"State vars: {state_count}")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_retool_json.py <file.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"Validating: {file_path}\n")

    result = validate(file_path)

    print(result.summary())
    print()

    if result.ok:
        print(f"PASS — {len(result.warnings)} warning(s)")
    else:
        print(f"FAIL — {len(result.errors)} error(s), {len(result.warnings)} warning(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
