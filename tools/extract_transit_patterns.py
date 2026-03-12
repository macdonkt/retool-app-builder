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


def _discover_type_tag_cache_refs(app_state, cache):
    """
    Discover cache refs for Transit type tags (~#iR, ~#iOM, ~#iM, ~#iL)
    by finding pairs: a full tag at one location, and a cache ref at the
    same structural role elsewhere.

    Strategy: Walk the entire structure. Collect all full type tags seen.
    For each unresolved cache ref that appears as a list marker (first
    element of a 2-element list), find which full type tag it replaces
    by checking the structure at the app level where full tags appear first.
    """
    # Step 1: Find full type tags and which cache refs follow them
    # Transit assigns a cache slot to each type tag on first encounter.
    # The NEXT time that same tag would appear, the cache ref is used instead.
    # So we find all full tags in the app-level structure, then look for
    # cache refs used in the same structural role in plugin data.

    full_tags_seen = set()  # type tags with full names found in the structure
    cache_ref_as_tags = {}  # cache_ref -> set of structural contexts

    def _scan(obj, in_plugin_data=False):
        if not isinstance(obj, list) or len(obj) == 0:
            return
        marker = obj[0]
        if isinstance(marker, str):
            if marker.startswith("~#"):
                full_tags_seen.add(marker)
            elif _is_cache_ref(marker) and marker not in cache and len(obj) == 2:
                # This is a list marker that's a cache ref
                # Record what kind of inner data it wraps
                inner = obj[1]
                if isinstance(inner, list):
                    if len(inner) == 0:
                        cache_ref_as_tags.setdefault(marker, set()).add("empty")
                    elif inner[0] == "^ ":
                        cache_ref_as_tags.setdefault(marker, set()).add("tmap")
                    elif isinstance(inner[0], list):
                        cache_ref_as_tags.setdefault(marker, set()).add("list_of_lists")
                    else:
                        cache_ref_as_tags.setdefault(marker, set()).add("flat_list")

        for item in obj:
            if isinstance(item, list):
                _scan(item)

    _scan(app_state)

    # Step 2: For unresolved cache refs acting as type tags, infer the mapping
    # ~#iR wraps a tmap (record)
    # ~#iOM / ~#iM wrap key-value pair lists (ordered maps)
    # ~#iL wraps plain lists (arrays)

    for ref, contexts in cache_ref_as_tags.items():
        if ref in cache:
            continue

        if "tmap" in contexts:
            # Wraps a tmap → must be ~#iR
            cache[ref] = "~#iR"
        elif "list_of_lists" in contexts:
            # Wraps a list of lists → must be ~#iL (list of items)
            cache[ref] = "~#iL"
        elif "flat_list" in contexts and "empty" in contexts:
            # Wraps flat lists AND empty lists — could be ~#iL or ~#iOM
            # Check if it's used where ~#iL was the original full tag
            if "~#iL" in full_tags_seen and "~#iOM" in cache.values():
                # ~#iOM is already mapped, and ~#iL was seen as full name
                # → this is likely ~#iL
                cache[ref] = "~#iL"
        elif "flat_list" in contexts:
            # Only flat lists — could be ~#iOM (k/v pairs) or ~#iL
            # If ~#iL full tag was seen but no cache ref maps to it yet,
            # this is likely ~#iL
            il_mapped = any(v == "~#iL" for v in cache.values())
            if not il_mapped and "~#iL" in full_tags_seen:
                cache[ref] = "~#iL"
        elif "empty" in contexts and len(contexts) == 1:
            # Only empty usages — check if ~#iL needs mapping
            il_mapped = any(v == "~#iL" for v in cache.values())
            if not il_mapped and "~#iL" in full_tags_seen:
                cache[ref] = "~#iL"


def _discover_position_keys(items, cache):
    """
    Discover cache refs for position2 sub-fields (rowGroup, subcontainer,
    height, width, tabNum, stackPosition) by comparing position2 data from
    the first widget that uses full names vs later widgets that use cache refs.
    """
    first_pos_keys = None
    for j in range(0, len(items) - 1, 2):
        plugin_val = items[j + 1]
        if not isinstance(plugin_val, list) or len(plugin_val) < 2:
            continue
        plugin_tmap = plugin_val[1][4]
        pos_raw = _get_field_resolved(plugin_tmap, "position2", cache)
        if not pos_raw or not isinstance(pos_raw, list) or len(pos_raw) < 2:
            continue

        # position2 is ["^0", ["^ ", "n", "position2", "v", inner_tmap]]
        # inner_tmap is ["^ ", key, val, key, val, ...]
        inner = pos_raw
        if isinstance(inner[0], str) and (inner[0] == "~#iR" or cache.get(inner[0]) == "~#iR"):
            inner = inner[1]
        if not isinstance(inner, list) or inner[0] != "^ ":
            continue

        # Get the 'v' value from the record inner
        v_val = None
        pairs = inner[1:]
        for pi in range(0, len(pairs) - 1, 2):
            k = pairs[pi]
            rk = cache.get(k, k) if _is_cache_ref(k) else k
            if rk in ("v", "position2"):
                # Sometimes 'n' key = 'position2', 'v' key = the actual data
                v_val = pairs[pi + 1]
                break

        if v_val is None or not isinstance(v_val, list) or v_val[0] != "^ ":
            continue

        pos_pairs = v_val[1:]
        # Check if this uses full names (no cache refs as keys)
        has_full_names = any(
            isinstance(pos_pairs[i], str) and not _is_cache_ref(pos_pairs[i])
            and pos_pairs[i] not in ("type", "container")  # skip already-known keys
            for i in range(0, len(pos_pairs) - 1, 2)
        )

        if has_full_names and first_pos_keys is None:
            first_pos_keys = pos_pairs
        elif first_pos_keys is not None:
            # Compare this one with first to find cache mappings
            for ki in range(0, min(len(first_pos_keys), len(pos_pairs)) - 1, 2):
                k1 = first_pos_keys[ki]
                k2 = pos_pairs[ki]
                if isinstance(k1, str) and not _is_cache_ref(k1):
                    if isinstance(k2, str) and _is_cache_ref(k2) and k2 not in cache:
                        cache[k2] = k1
            break  # One comparison is enough


def build_cache_by_comparison(app_state):
    """
    Build cache ref -> full name mapping using multiple strategies:

    1. Positional comparison: Compare first vs second plugins at matching
       positions to discover plugin-level field cache refs.
    2. Structural inference: Scan entire structure for unresolved cache refs
       and infer their Transit type based on the shape of data they wrap.
    3. Position sub-key discovery: Compare position2 data across widgets
       to find cache refs for position fields (rowGroup, height, width, etc).
    """
    cache = {}

    rec_inner = app_state[1]
    app_tmap = rec_inner[4]

    pairs = app_tmap[1:]
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

    # --- Strategy 1: Positional comparison of plugins ---

    first_val = items[1]
    second_val = items[3]

    if _is_cache_ref(first_val[0]):
        cache[first_val[0]] = "~#iR"

    first_inner = first_val[1]
    second_inner = second_val[1]
    _compare_tmap_keys(first_inner, second_inner, cache)

    first_tmap = first_inner[4]
    second_tmap = second_inner[4]
    _compare_tmap_keys(first_tmap, second_tmap, cache)

    # Walk plugins to discover template/position type tags
    for j in range(0, len(items) - 1, 2):
        plugin_val = items[j + 1]
        plugin_tmap = plugin_val[1][4]

        tmpl_raw = _get_field_resolved(plugin_tmap, "template", cache)
        if tmpl_raw and isinstance(tmpl_raw, list) and len(tmpl_raw) > 1:
            marker = tmpl_raw[0]
            if isinstance(marker, str) and _is_cache_ref(marker):
                if marker not in cache:
                    cache[marker] = "~#iOM"

        pos_raw = _get_field_resolved(plugin_tmap, "position2", cache)
        if pos_raw and isinstance(pos_raw, list) and len(pos_raw) > 1:
            marker = pos_raw[0]
            if isinstance(marker, str) and _is_cache_ref(marker) and marker not in cache:
                cache[marker] = "~#iR"

    # Cross-compare templates from plugins of the same subtype
    subtypes_seen = {}
    for j in range(0, len(items) - 1, 2):
        plugin_val = items[j + 1]
        plugin_tmap = plugin_val[1][4]
        subtype = _get_field_resolved(plugin_tmap, "subtype", cache)
        if subtype and subtype not in subtypes_seen:
            subtypes_seen[subtype] = plugin_tmap
        elif subtype and subtype in subtypes_seen:
            first_t = _get_field_resolved(subtypes_seen[subtype], "template", cache)
            second_t = _get_field_resolved(plugin_tmap, "template", cache)
            if first_t and second_t:
                _compare_iom_keys(first_t, second_t, cache)

    # --- Strategy 2: Structural inference for type tags ---
    # Scan the ENTIRE structure to infer Transit type tags for any remaining
    # unresolved cache refs (e.g., ^A -> ~#iL)
    _discover_type_tag_cache_refs(app_state, cache)

    # --- Strategy 3: Position sub-key discovery ---
    _discover_position_keys(items, cache)

    # --- Strategy 4: App-level field name discovery ---
    # Some field names (like 'createdAt') are cached at the app level before
    # plugins. Find them by comparing the first plugin's tmap against the
    # app-level tmap keys.
    first_plugin_tmap = first_tmap
    start = 1 if first_plugin_tmap[0] == "^ " else 0
    for ki in range(start, len(first_plugin_tmap) - 1, 2):
        key = first_plugin_tmap[ki]
        if _is_cache_ref(key) and key not in cache:
            # This cache ref in the FIRST plugin means it was cached before
            # plugins. Check app-level tmap for matching field names.
            # The value next to this key might give us a hint about the field
            val = first_plugin_tmap[ki + 1]
            # Check if adjacent keys (before/after) in the first plugin are
            # known, and use them to narrow down the app-level field name
            prev_key = None
            next_key = None
            if ki >= start + 2:
                pk = first_plugin_tmap[ki - 2]
                prev_key = cache.get(pk, pk) if _is_cache_ref(pk) else pk
            if ki + 2 < len(first_plugin_tmap):
                nk = first_plugin_tmap[ki + 2]
                next_key = cache.get(nk, nk) if _is_cache_ref(nk) else nk

            # For 'createdAt': it appears between 'container' and 'updatedAt'
            # We know container and updatedAt, so we can search the first
            # plugin's full-name counterpart.
            # Since the first plugin already uses the cache ref, we need
            # another approach: check what full-name strings appear in the
            # app-level structure that aren't in our cache values yet.
            cached_values = set(cache.values())
            app_keys = set()
            for ai in range(0, len(pairs), 2):
                ak = pairs[ai]
                if isinstance(ak, str) and not _is_cache_ref(ak):
                    app_keys.add(ak)
            # Also check rec_inner keys
            ri_pairs = rec_inner[1:]
            for ai in range(0, len(ri_pairs) - 1, 2):
                ak = ri_pairs[ai]
                if isinstance(ak, str) and not _is_cache_ref(ak):
                    app_keys.add(ak)

            # Strings cached at app level but not yet in our cache
            uncovered = app_keys - cached_values
            # If value is a timestamp (~m...), it's likely 'createdAt'
            if isinstance(val, str) and val.startswith("~m"):
                if "createdAt" in uncovered:
                    cache[key] = "createdAt"

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

        # Helper to extract event handlers from a decoded template dict
        def _collect_events(tmpl, source_id, source_subtype, source_type):
            if not isinstance(tmpl, dict):
                return
            # Widget events: template.events = list of handler dicts
            if "events" in tmpl:
                events = tmpl["events"]
                if isinstance(events, list):
                    for ev in events:
                        if isinstance(ev, dict) and len(ev) > 0:
                            event_patterns.append({
                                "source_id": source_id,
                                "source_type": source_type,
                                "source_subtype": source_subtype,
                                "event": ev
                            })
            # Query event handlers: onSuccess, onFailure, etc.
            for handler_key in ("changeQuery", "successQuery", "failureQuery"):
                if handler_key in tmpl:
                    handler = tmpl[handler_key]
                    if isinstance(handler, dict) and len(handler) > 0:
                        event_patterns.append({
                            "source_id": source_id,
                            "source_type": source_type,
                            "source_subtype": source_subtype,
                            "handler_type": handler_key,
                            "event": handler
                        })
            # Also check for event handler arrays in query templates
            for handler_key in ("onSuccessEventHandlers", "onFailureEventHandlers"):
                if handler_key in tmpl:
                    handlers = tmpl[handler_key]
                    if isinstance(handlers, list):
                        for h in handlers:
                            if isinstance(h, dict) and len(h) > 0:
                                event_patterns.append({
                                    "source_id": source_id,
                                    "source_type": source_type,
                                    "source_subtype": source_subtype,
                                    "handler_type": handler_key,
                                    "event": h
                                })

        if plugin_type == "widget":
            if plugin_subtype and plugin_subtype not in widget_templates:
                widget_templates[plugin_subtype] = {
                    "example_id": plugin_id,
                    "template": template,
                    "position": position
                }
            _collect_events(template, plugin_id, plugin_subtype, "widget")
            if position and plugin_subtype not in position_examples:
                position_examples[plugin_subtype] = position

        elif plugin_type == "datasource":
            if plugin_subtype and plugin_subtype not in query_templates:
                query_templates[plugin_subtype] = {
                    "example_id": plugin_id,
                    "template": template,
                    "resource_name": _get_field_resolved(plugin_tmap, "resourceDisplayName", cache)
                }
            _collect_events(template, plugin_id, plugin_subtype, "datasource")

        elif plugin_type == "state":
            screen = _get_field_resolved(plugin_tmap, "screen", cache)
            state_templates[plugin_id] = {
                "subtype": plugin_subtype,
                "template": template,
                "screen": screen  # None = global, "page1" = page-scoped
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
            "state_variables": len(state_templates),
            "event_patterns_found": len(event_patterns),
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
        print(f"  State variables: {result['_meta']['state_variables']}")
        print(f"  Cache keys:      {result['_meta']['cache_keys_discovered']}")
        print(f"  Event patterns:  {len(result['event_patterns'])}")


if __name__ == "__main__":
    main()
