#!/usr/bin/env python3
"""
Extract Transit patterns from a Retool-exported JSON file.

Parses the components example (or any Retool export) and extracts:
- Widget templates by subtype (decoded to full field names)
- Query templates by subtype
- Event handler patterns
- Position examples
- Cache key resolution map (for documentation)

Output: transit_patterns.json (structured reference for the builder library)

Usage:
    python3 tools/extract_transit_patterns.py [input_file] [output_file]

    Defaults:
        input:  apps/general references/components exmple.json
        output: tools/transit_patterns.json
"""

import json
import sys
import os


# ══════════════════════════════════════════════════════════════════════════════
# CACHE KEY RESOLVER
# ══════════════════════════════════════════════════════════════════════════════

def _is_cache_ref(s):
    return isinstance(s, str) and len(s) >= 2 and s[0] == '^' and s != "^ "


def build_cache_by_comparison(app_state):
    """
    Build cache ref -> full name mapping by comparing the first plugin
    (uses full names) with subsequent plugins (use cache refs) at matching
    structural positions.
    """
    cache = {}

    # Root: ["~#iR", rec_inner]
    # rec_inner: ["^ ", "n", "appTemplate", "v", app_tmap]
    # We know ~#iR is the record tag. First plugin uses ^0 for it.
    # So ^0 -> ~#iR (we'll verify by checking the first plugin's record tag)

    rec_inner = app_state[1]
    app_tmap = rec_inner[4]  # appTemplate value

    # Find plugins iOM
    pairs = app_tmap[1:]  # skip "^ "
    plugins_iom = None
    for i in range(0, len(pairs), 2):
        if pairs[i] == "plugins":
            plugins_iom = pairs[i + 1]
            break

    if not plugins_iom:
        return cache

    items = plugins_iom[1]
    if len(items) < 4:
        return cache

    # The FIRST plugin always uses full field names for its tmap keys
    # Subsequent plugins use cache refs for repeated keys
    # We align them by position to discover the mapping

    first_val = items[1]   # first plugin value (e.g., page1's record)
    second_val = items[3]  # second plugin value (e.g., $main's record)

    # Record tag: first_val[0] vs second_val[0]
    # Both should be ^0 (since ~#iR was used at the root level already)
    # But let's also check the root
    if _is_cache_ref(first_val[0]):
        # The record tag was already cached before plugins
        cache[first_val[0]] = "~#iR"

    # Record inner tmap keys
    first_inner = first_val[1]   # ["^ ", "n", "pluginTemplate", "v", tmap]
    second_inner = second_val[1]

    _compare_tmap_keys(first_inner, second_inner, cache)

    # Plugin tmap keys
    first_tmap = first_inner[4]   # the 'v' value = plugin tmap
    second_tmap = second_inner[4]

    _compare_tmap_keys(first_tmap, second_tmap, cache)

    # Now also process template fields from multiple plugins
    # to capture iOM keys, template-specific keys, etc.
    # We need to compare plugins of the same type
    first_type = _get_field_direct(first_tmap, "type")

    # Walk through all plugins to find template key cache refs
    for j in range(0, len(items) - 1, 2):
        plugin_val = items[j + 1]
        plugin_tmap = plugin_val[1][4]  # record inner -> v

        # Template value
        tmpl_raw = _get_field_resolved(plugin_tmap, "template", cache)
        if tmpl_raw and isinstance(tmpl_raw, list) and len(tmpl_raw) > 1:
            marker = tmpl_raw[0]
            if isinstance(marker, str) and _is_cache_ref(marker):
                # This is a cached ~#iOM or ~#iM
                if marker not in cache:
                    # We know templates use ~#iOM or ~#iM
                    cache[marker] = "~#iOM"  # Most common

            # Process iOM/iM inner keys
            if isinstance(tmpl_raw, list) and len(tmpl_raw) > 1:
                inner_items = tmpl_raw[1]
                if isinstance(inner_items, list):
                    for k in range(0, len(inner_items) - 1, 2):
                        key = inner_items[k]
                        if isinstance(key, str) and not _is_cache_ref(key):
                            # Full name key — any later plugin may use a cache ref
                            pass

        # Position value
        pos_raw = _get_field_resolved(plugin_tmap, "position2", cache)
        if pos_raw and isinstance(pos_raw, list) and len(pos_raw) > 1:
            marker = pos_raw[0]
            if isinstance(marker, str) and _is_cache_ref(marker) and marker not in cache:
                cache[marker] = "~#iR"

    # Cross-compare templates from plugins of the same subtype
    # to discover template-internal cache refs
    subtypes_seen = {}
    for j in range(0, len(items) - 1, 2):
        plugin_val = items[j + 1]
        plugin_tmap = plugin_val[1][4]
        subtype = _get_field_resolved(plugin_tmap, "subtype", cache)
        if subtype and subtype not in subtypes_seen:
            subtypes_seen[subtype] = plugin_tmap
        elif subtype and subtype in subtypes_seen:
            # Compare templates
            first_t = _get_field_resolved(subtypes_seen[subtype], "template", cache)
            second_t = _get_field_resolved(plugin_tmap, "template", cache)
            if first_t and second_t:
                _compare_iom_keys(first_t, second_t, cache)

    return cache


def _compare_tmap_keys(first, second, cache):
    """Compare two tmaps at the same positions to discover cache mappings."""
    if not isinstance(first, list) or not isinstance(second, list):
        return
    if first[0] != "^ " or second[0] != "^ ":
        return

    p1 = first[1:]
    p2 = second[1:]

    for i in range(0, min(len(p1), len(p2)) - 1, 2):
        k1 = p1[i]
        k2 = p2[i]
        if isinstance(k1, str) and not _is_cache_ref(k1):
            if isinstance(k2, str) and _is_cache_ref(k2):
                cache[k2] = k1


def _compare_iom_keys(first, second, cache):
    """Compare two iOM structures to discover key cache mappings."""
    if not isinstance(first, list) or not isinstance(second, list):
        return
    if len(first) < 2 or len(second) < 2:
        return

    items1 = first[1] if isinstance(first[1], list) else []
    items2 = second[1] if isinstance(second[1], list) else []

    for i in range(0, min(len(items1), len(items2)) - 1, 2):
        k1 = items1[i]
        k2 = items2[i]
        if isinstance(k1, str) and not _is_cache_ref(k1):
            if isinstance(k2, str) and _is_cache_ref(k2):
                cache[k2] = k1


def _get_field_direct(tmap_list, field_name):
    """Get a field from a tmap using only full field names (no cache resolution)."""
    if not isinstance(tmap_list, list):
        return None
    start = 1 if tmap_list[0] == "^ " else 0
    for i in range(start, len(tmap_list) - 1, 2):
        if tmap_list[i] == field_name:
            return tmap_list[i + 1]
    return None


def _get_field_resolved(tmap_list, field_name, cache):
    """Get a field from a tmap, resolving cache keys."""
    if not isinstance(tmap_list, list):
        return None
    start = 1 if isinstance(tmap_list[0], str) and tmap_list[0] == "^ " else 0
    for i in range(start, len(tmap_list) - 1, 2):
        key = tmap_list[i]
        resolved = cache.get(key, key) if _is_cache_ref(key) else key
        if resolved == field_name:
            return tmap_list[i + 1]
    return None


def decode_structure(obj, cache):
    """Recursively decode Transit structure, resolving all cache keys."""
    if not isinstance(obj, list) or len(obj) == 0:
        return obj

    marker = obj[0]
    if isinstance(marker, str):
        resolved = cache.get(marker, marker) if _is_cache_ref(marker) else marker
    else:
        resolved = marker

    if resolved == "^ ":
        result = {}
        pairs = obj[1:]
        for i in range(0, len(pairs) - 1, 2):
            key = pairs[i]
            if isinstance(key, str):
                key = cache.get(key, key) if _is_cache_ref(key) else key
            result[key] = decode_structure(pairs[i + 1], cache)
        return result

    if resolved in ("~#iOM", "~#iM"):
        items = obj[1] if len(obj) > 1 and isinstance(obj[1], list) else []
        result = {}
        for i in range(0, len(items) - 1, 2):
            key = items[i]
            if isinstance(key, str):
                key = cache.get(key, key) if _is_cache_ref(key) else key
            result[key] = decode_structure(items[i + 1], cache)
        return result

    if resolved == "~#iR":
        return decode_structure(obj[1], cache) if len(obj) > 1 else {}

    if resolved == "~#iL":
        items = obj[1] if len(obj) > 1 and isinstance(obj[1], list) else []
        return [decode_structure(item, cache) for item in items]

    # Unknown list — decode each element
    return [decode_structure(item, cache) for item in obj]


# ══════════════════════════════════════════════════════════════════════════════
# EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

def extract_patterns(input_path):
    """Extract all Transit patterns from a Retool export file."""

    with open(input_path) as f:
        outer = json.load(f)

    app_state = json.loads(outer["page"]["data"]["appState"])

    # Build cache mapping
    cache = build_cache_by_comparison(app_state)
    print(f"Discovered {len(cache)} cache key mappings")

    # Navigate to plugins
    rec_inner = app_state[1]
    app_tmap = rec_inner[4]
    pairs = app_tmap[1:]

    plugins_iom = None
    for i in range(0, len(pairs), 2):
        if pairs[i] == "plugins":
            plugins_iom = pairs[i + 1]
            break

    if not plugins_iom:
        print("ERROR: Could not find plugins iOM")
        return None

    items = plugins_iom[1]
    plugin_count = len(items) // 2
    print(f"Found {plugin_count} plugins")

    # Extract patterns
    widget_templates = {}
    query_templates = {}
    state_templates = {}
    frame_templates = {}
    screen_templates = {}
    event_patterns = []
    position_examples = {}

    for j in range(0, len(items), 2):
        plugin_id = items[j]
        plugin_raw = items[j + 1]

        if not isinstance(plugin_raw, list) or len(plugin_raw) < 2:
            continue
        rec_inner = plugin_raw[1]
        if not isinstance(rec_inner, list) or len(rec_inner) < 5:
            continue

        plugin_tmap = rec_inner[4]  # always at position 4: ["^ ", n_key, name, v_key, VALUE]
        if not isinstance(plugin_tmap, list):
            continue

        plugin_type = _get_field_resolved(plugin_tmap, "type", cache)
        plugin_subtype = _get_field_resolved(plugin_tmap, "subtype", cache)
        template_raw = _get_field_resolved(plugin_tmap, "template", cache)
        position_raw = _get_field_resolved(plugin_tmap, "position2", cache)

        # Decode to readable dicts
        template = decode_structure(template_raw, cache) if template_raw else {}
        position = decode_structure(position_raw, cache) if position_raw else None

        if plugin_type == "widget":
            if plugin_subtype and plugin_subtype not in widget_templates:
                widget_templates[plugin_subtype] = {
                    "example_id": plugin_id,
                    "template": template,
                    "position": position
                }
            # Collect event patterns
            if isinstance(template, dict) and "events" in template:
                events = template["events"]
                if isinstance(events, list):
                    for ev in events:
                        if isinstance(ev, dict) and len(ev) > 0:
                            event_patterns.append({
                                "source_widget": plugin_id,
                                "source_subtype": plugin_subtype,
                                "event": ev
                            })
            if position and plugin_subtype not in position_examples:
                position_examples[plugin_subtype] = position

        elif plugin_type == "datasource":
            if plugin_subtype and plugin_subtype not in query_templates:
                query_templates[plugin_subtype] = {
                    "example_id": plugin_id,
                    "template": template,
                    "resource_name": _get_field_resolved(plugin_tmap, "resourceDisplayName", cache)
                }

        elif plugin_type == "state":
            if plugin_subtype and plugin_subtype not in state_templates:
                state_templates[plugin_subtype] = {
                    "example_id": plugin_id,
                    "template": template
                }

        elif plugin_type == "frame":
            frame_templates[plugin_id] = {
                "subtype": plugin_subtype,
                "template": template
            }

        elif plugin_type == "screen":
            screen_templates[plugin_id] = {
                "subtype": plugin_subtype,
                "template": template
            }

    # Build sorted cache key map
    cache_key_map = dict(sorted(cache.items()))

    result = {
        "_meta": {
            "source_file": os.path.basename(input_path),
            "total_plugins": plugin_count,
            "widget_subtypes": len(widget_templates),
            "query_subtypes": len(query_templates),
            "state_subtypes": len(state_templates),
            "cache_keys_discovered": len(cache_key_map),
            "note": "Cache keys are POSITIONAL and specific to this file. Do NOT hardcode them. Use full field names in the builder library instead."
        },
        "cache_key_map": cache_key_map,
        "widget_templates": widget_templates,
        "query_templates": query_templates,
        "state_templates": state_templates,
        "frame_templates": frame_templates,
        "screen_templates": screen_templates,
        "event_patterns": event_patterns,
        "position_examples": position_examples
    }

    return result


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    input_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        project_root, "apps", "general references", "components exmple.json"
    )
    output_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        script_dir, "transit_patterns.json"
    )

    if not os.path.exists(input_path):
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    print(f"Extracting patterns from: {input_path}")
    result = extract_patterns(input_path)

    if result:
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nOutput written to: {output_path}")
        print(f"  Widget subtypes: {result['_meta']['widget_subtypes']}")
        print(f"  Query subtypes:  {result['_meta']['query_subtypes']}")
        print(f"  Cache keys:      {result['_meta']['cache_keys_discovered']}")
        print(f"  Event patterns:  {len(result['event_patterns'])}")


if __name__ == "__main__":
    main()
