#!/usr/bin/env python3
"""
Compare Transit-encoded Retool JSON structures between a known-working
reference export and our builder output.
"""

import json
import sys
from collections import OrderedDict

REF_PATH = "/Users/kevin/Documents/Agentic workflows/Retool Builder/apps/general references/components example.json"
BUILDER_PATH = "/Users/kevin/Documents/Agentic workflows/Retool Builder/apps/Time on site 2/step5.json"


def load_app_state(path):
    """Load file, parse outer JSON, then parse appState string."""
    with open(path, "r") as f:
        outer = json.load(f)
    app_state_str = outer["page"]["data"]["appState"]
    return json.loads(app_state_str)


def decode_transit(node, cache=None, depth=0):
    """
    Recursively decode Transit-encoded JSON into plain Python dicts/lists.
    Handles:
      ~#iR  -> tagged record (has n=name, v=value)
      ~#iOM -> ordered map (alternating key/value list)
      ~#iL  -> transit list
      ~#iM  -> transit map
      "^ "  -> cache-reset marker for map keys
      ^N    -> cache reference
    """
    if cache is None:
        cache = []

    if isinstance(node, str):
        return node

    if isinstance(node, (int, float, bool)) or node is None:
        return node

    if isinstance(node, list):
        if len(node) == 0:
            return []

        # Check for tagged types
        if isinstance(node[0], str):
            tag = node[0]

            if tag == "~#iR":
                # Tagged record: ["~#iR", ["^ ", "n", name, "v", value]]
                inner = node[1]
                decoded_inner = decode_transit_map(inner, cache, depth)
                return {"__type": "iR", **decoded_inner}

            elif tag == "~#iOM":
                # Ordered map: ["~#iOM", [k1, v1, k2, v2, ...]]
                inner = node[1]
                return decode_transit_ordered_map(inner, cache, depth)

            elif tag == "~#iL":
                # Transit list
                inner = node[1]
                return {"__type": "iL", "items": [decode_transit(item, cache, depth+1) for item in inner]}

            elif tag == "~#iM":
                inner = node[1]
                return decode_transit_map(inner, cache, depth)

        # Plain array
        return [decode_transit(item, cache, depth+1) for item in node]

    if isinstance(node, dict):
        result = {}
        for k, v in node.items():
            result[k] = decode_transit(v, cache, depth+1)
        return result

    return node


def decode_transit_map(arr, cache, depth):
    """Decode a transit map array: ["^ ", key, val, key, val, ...]"""
    result = OrderedDict()
    if not isinstance(arr, list):
        return arr

    i = 0
    if len(arr) > 0 and arr[0] == "^ ":
        i = 1  # skip cache reset marker

    while i < len(arr) - 1:
        key = arr[i]
        val = arr[i + 1]

        # Resolve cache references for keys
        if isinstance(key, str) and key.startswith("^") and len(key) > 1 and key != "^ ":
            key = resolve_cache(key, cache)
        elif isinstance(key, str) and not key.startswith("~"):
            # Add to cache
            cache.append(key)

        result[key] = decode_transit(val, cache, depth+1)
        i += 2

    return dict(result)


def decode_transit_ordered_map(arr, cache, depth):
    """Decode ordered map: [k1, v1, k2, v2, ...]"""
    result = OrderedDict()
    if not isinstance(arr, list):
        return arr

    i = 0
    while i < len(arr) - 1:
        key = arr[i]
        val = arr[i + 1]

        if isinstance(key, str) and key.startswith("^") and len(key) > 1:
            key = resolve_cache(key, cache)
        elif isinstance(key, str) and not key.startswith("~"):
            cache.append(key)

        result[key] = decode_transit(val, cache, depth+1)
        i += 2

    return {"__type": "iOM", **dict(result)}


def resolve_cache(ref, cache):
    """Resolve a cache reference like ^0, ^1, ^1A, etc."""
    code = ref[1:]

    CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-"

    if len(code) == 1:
        idx = CHARS.index(code)
    elif len(code) == 2:
        idx = CHARS.index(code[0]) * len(CHARS) + CHARS.index(code[1])
    else:
        idx = 0
        for c in code:
            idx = idx * len(CHARS) + CHARS.index(c)

    if idx < len(cache):
        return cache[idx]
    else:
        return f"UNRESOLVED:{ref}"


def find_plugin(decoded, plugin_id):
    """Find a plugin by id in the decoded appState."""
    # Navigate: iR -> v -> plugins -> find by id
    v = decoded.get("v", decoded)
    plugins = v.get("plugins", {})

    # plugins is an iOM with plugin ids as keys
    if isinstance(plugins, dict):
        if plugin_id in plugins:
            return plugins[plugin_id]

    return None


def find_plugins_with_type(decoded, subtype):
    """Find all plugins with a given subtype."""
    v = decoded.get("v", decoded)
    plugins = v.get("plugins", {})
    results = []

    if isinstance(plugins, dict):
        for pid, pdata in plugins.items():
            if pid.startswith("__"):
                continue
            if isinstance(pdata, dict):
                pv = pdata.get("v", pdata)
                if pv.get("subtype") == subtype:
                    results.append((pid, pdata))

    return results


def print_dict_comparison(label, d1, d2, indent=0):
    """Compare two dicts field by field, printing differences."""
    prefix = "  " * indent

    if not isinstance(d1, dict) or not isinstance(d2, dict):
        if d1 != d2:
            print(f"{prefix}VALUE DIFFERS:")
            print(f"{prefix}  REF:     {json.dumps(d1, default=str)[:200]}")
            print(f"{prefix}  BUILDER: {json.dumps(d2, default=str)[:200]}")
        return

    all_keys = list(dict.fromkeys(list(d1.keys()) + list(d2.keys())))

    for key in all_keys:
        if key.startswith("__"):
            # Compare type tags
            if key == "__type":
                if d1.get(key) != d2.get(key):
                    print(f"{prefix}TYPE TAG DIFFERS: REF={d1.get(key)} BUILDER={d2.get(key)}")
            continue

        in1 = key in d1
        in2 = key in d2

        if in1 and not in2:
            val = d1[key]
            if isinstance(val, dict):
                print(f"{prefix}MISSING IN BUILDER: '{key}' = {{...}}")
            else:
                print(f"{prefix}MISSING IN BUILDER: '{key}' = {json.dumps(val, default=str)[:150]}")
        elif in2 and not in1:
            val = d2[key]
            if isinstance(val, dict):
                print(f"{prefix}EXTRA IN BUILDER: '{key}' = {{...}}")
            else:
                print(f"{prefix}EXTRA IN BUILDER: '{key}' = {json.dumps(val, default=str)[:150]}")
        else:
            v1 = d1[key]
            v2 = d2[key]
            if isinstance(v1, dict) and isinstance(v2, dict):
                subdiffs = get_diff_count(v1, v2)
                if subdiffs > 0:
                    print(f"{prefix}'{key}': ({subdiffs} differences)")
                    print_dict_comparison(key, v1, v2, indent + 1)
            elif isinstance(v1, list) and isinstance(v2, list):
                if v1 != v2:
                    print(f"{prefix}'{key}' DIFFERS:")
                    print(f"{prefix}  REF:     {json.dumps(v1, default=str)[:200]}")
                    print(f"{prefix}  BUILDER: {json.dumps(v2, default=str)[:200]}")
            elif v1 != v2:
                print(f"{prefix}'{key}' DIFFERS:")
                print(f"{prefix}  REF:     {json.dumps(v1, default=str)[:150]}")
                print(f"{prefix}  BUILDER: {json.dumps(v2, default=str)[:150]}")


def get_diff_count(d1, d2):
    """Count differences between two dicts."""
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        return 0 if d1 == d2 else 1
    count = 0
    all_keys = set(list(d1.keys()) + list(d2.keys())) - {"__type"}
    for key in all_keys:
        if key.startswith("__"):
            continue
        if key not in d1 or key not in d2:
            count += 1
        elif isinstance(d1[key], dict) and isinstance(d2[key], dict):
            count += get_diff_count(d1[key], d2[key])
        elif d1[key] != d2[key]:
            count += 1
    return count


def extract_structure_only(d, max_depth=3, depth=0):
    """Extract just the structural keys (no values) for comparison."""
    if not isinstance(d, dict) or depth >= max_depth:
        return type(d).__name__
    result = {}
    for k, v in d.items():
        if k.startswith("__"):
            result[k] = v
        else:
            result[k] = extract_structure_only(v, max_depth, depth+1)
    return result


def main():
    print("=" * 80)
    print("LOADING FILES...")
    print("=" * 80)

    ref_raw = load_app_state(REF_PATH)
    builder_raw = load_app_state(BUILDER_PATH)

    print("\nDecoding reference (with cache)...")
    ref_cache = []
    ref = decode_transit(ref_raw, ref_cache)

    print("Decoding builder...")
    builder_cache = []
    builder = decode_transit(builder_raw, builder_cache)

    ref_v = ref.get("v", ref)
    builder_v = builder.get("v", builder)

    # =====================================================================
    # 1. STATE VARIABLE COMPARISON
    # =====================================================================
    print("\n" + "=" * 80)
    print("1. STATE VARIABLE (StateSlot) COMPARISON")
    print("=" * 80)

    ref_states = find_plugins_with_type(ref, "StateSlot")
    print(f"\nReference has {len(ref_states)} StateSlot(s)")

    builder_itemcount = find_plugin(builder, "itemCount")

    if ref_states:
        ref_state_id, ref_state = ref_states[0]
        print(f"Using reference StateSlot: '{ref_state_id}'")
        print(f"\n--- Reference StateSlot '{ref_state_id}' FULL structure ---")
        print(json.dumps(ref_state, indent=2, default=str)[:3000])
        print(f"\n--- Builder 'itemCount' FULL structure ---")
        print(json.dumps(builder_itemcount, indent=2, default=str)[:3000])

        print(f"\n--- DIFFERENCES ---")
        # Compare the 'v' (value) part
        ref_sv = ref_state.get("v", ref_state)
        builder_sv = builder_itemcount.get("v", builder_itemcount)
        print_dict_comparison("StateSlot", ref_sv, builder_sv)
    else:
        print("No StateSlot found in reference!")

    # =====================================================================
    # 2. WIDGETS INSIDE MODAL
    # =====================================================================
    print("\n" + "=" * 80)
    print("2. WIDGETS INSIDE MODAL COMPARISON")
    print("=" * 80)

    # Find modalTitle1 and modalCloseButton1 in reference
    ref_modal_title = find_plugin(ref, "modalTitle1")
    ref_modal_close = find_plugin(ref, "modalCloseButton1")

    builder_modal_title = find_plugin(builder, "modalTitle")
    builder_cancel = find_plugin(builder, "cancelButton")

    # Also find the modal frames themselves
    ref_modal_frame = find_plugin(ref, "modalFrame1")
    builder_modal_frame = find_plugin(builder, "addModal")

    print(f"\nReference modalTitle1 found: {ref_modal_title is not None}")
    print(f"Reference modalCloseButton1 found: {ref_modal_close is not None}")
    print(f"Reference modalFrame1 found: {ref_modal_frame is not None}")

    if ref_modal_title is None:
        # Try to find any widget with container = modalFrame1
        print("\nSearching for widgets inside modal frames in reference...")
        ref_plugins = ref_v.get("plugins", {})
        for pid, pdata in ref_plugins.items():
            if pid.startswith("__"):
                continue
            if isinstance(pdata, dict):
                pv = pdata.get("v", pdata)
                container = pv.get("container")
                if container and "modal" in str(container).lower():
                    print(f"  Found '{pid}' in container '{container}', subtype={pv.get('subtype')}")

    # Compare modal frames
    if ref_modal_frame and builder_modal_frame:
        print(f"\n--- MODAL FRAME COMPARISON ---")
        ref_mfv = ref_modal_frame.get("v", ref_modal_frame)
        builder_mfv = builder_modal_frame.get("v", builder_modal_frame)
        print_dict_comparison("ModalFrame", ref_mfv, builder_mfv)

    # Compare modal title widgets
    if ref_modal_title and builder_modal_title:
        print(f"\n--- MODAL TITLE WIDGET COMPARISON ---")
        ref_mtv = ref_modal_title.get("v", ref_modal_title)
        builder_mtv = builder_modal_title.get("v", builder_modal_title)

        print(f"\nKey fields comparison:")
        for field in ["container", "type", "subtype"]:
            rv = ref_mtv.get(field)
            bv = builder_mtv.get(field)
            print(f"  {field}: REF={rv} BUILDER={bv} {'OK' if rv == bv else 'DIFFERS!'}")

        # Deep compare position2
        ref_pos = ref_mtv.get("position2", {})
        builder_pos = builder_mtv.get("position2", {})
        print(f"\nposition2 comparison:")
        ref_posv = ref_pos.get("v", ref_pos) if isinstance(ref_pos, dict) else ref_pos
        builder_posv = builder_pos.get("v", builder_pos) if isinstance(builder_pos, dict) else builder_pos
        print(f"  REF:     {json.dumps(ref_posv, default=str)}")
        print(f"  BUILDER: {json.dumps(builder_posv, default=str)}")
        if ref_posv != builder_posv:
            print("  DIFFERENCES:")
            print_dict_comparison("position2", ref_posv, builder_posv, indent=2)

        print(f"\nFull differences:")
        print_dict_comparison("modalTitle", ref_mtv, builder_mtv)

    # Compare close/cancel buttons
    if ref_modal_close and builder_cancel:
        print(f"\n--- MODAL CLOSE/CANCEL BUTTON COMPARISON ---")
        ref_cbv = ref_modal_close.get("v", ref_modal_close)
        builder_cbv = builder_cancel.get("v", builder_cancel)

        print(f"\nKey fields comparison:")
        for field in ["container", "type", "subtype"]:
            rv = ref_cbv.get(field)
            bv = builder_cbv.get(field)
            print(f"  {field}: REF={rv} BUILDER={bv} {'OK' if rv == bv else 'DIFFERS!'}")

        ref_pos = ref_cbv.get("position2", {})
        builder_pos = builder_cbv.get("position2", {})
        print(f"\nposition2 comparison:")
        ref_posv = ref_pos.get("v", ref_pos) if isinstance(ref_pos, dict) else ref_pos
        builder_posv = builder_pos.get("v", builder_pos) if isinstance(builder_pos, dict) else builder_pos
        print(f"  REF:     {json.dumps(ref_posv, default=str)}")
        print(f"  BUILDER: {json.dumps(builder_posv, default=str)}")

        print(f"\nFull differences:")
        print_dict_comparison("closeButton", ref_cbv, builder_cbv)

    # =====================================================================
    # 3. QUERY EVENT HANDLERS
    # =====================================================================
    print("\n" + "=" * 80)
    print("3. QUERY EVENT HANDLER COMPARISON")
    print("=" * 80)

    # Find queries with events in reference
    ref_queries = find_plugins_with_type(ref, "JavascriptQuery")
    ref_queries += find_plugins_with_type(ref, "RESTQuery")
    ref_queries += find_plugins_with_type(ref, "SqlQuery")
    ref_queries += find_plugins_with_type(ref, "RetoolDatabaseQuery")

    print(f"\nReference has {len(ref_queries)} queries")

    ref_query_with_events = None
    for qid, qdata in ref_queries:
        qv = qdata.get("v", qdata)
        template = qv.get("template", {})
        events = template.get("events")
        if events:
            items = events.get("items", []) if isinstance(events, dict) else events
            if isinstance(items, list) and len(items) > 0:
                ref_query_with_events = (qid, qdata)
                print(f"Found query with events: '{qid}'")
                print(f"  Events: {json.dumps(events, indent=2, default=str)[:1000]}")
                break

    builder_fetch = find_plugin(builder, "fetchItems")
    if builder_fetch:
        bfv = builder_fetch.get("v", builder_fetch)
        b_template = bfv.get("template", {})
        b_events = b_template.get("events")
        print(f"\nBuilder fetchItems events:")
        print(f"  {json.dumps(b_events, indent=2, default=str)[:1000]}")

    if ref_query_with_events and builder_fetch:
        print(f"\n--- EVENT STRUCTURE COMPARISON ---")
        ref_qv = ref_query_with_events[1].get("v", ref_query_with_events[1])
        ref_tmpl = ref_qv.get("template", {})
        ref_events = ref_tmpl.get("events")

        builder_qv = builder_fetch.get("v", builder_fetch)
        builder_tmpl = builder_qv.get("template", {})
        builder_events = builder_tmpl.get("events")

        print(f"\nRef events type tag: {ref_events.get('__type') if isinstance(ref_events, dict) else type(ref_events)}")
        print(f"Builder events type tag: {builder_events.get('__type') if isinstance(builder_events, dict) else type(builder_events)}")

        # Extract individual event objects
        ref_evt_items = ref_events.get("items", []) if isinstance(ref_events, dict) else ref_events
        builder_evt_items = builder_events.get("items", []) if isinstance(builder_events, dict) else builder_events

        if ref_evt_items and builder_evt_items:
            ref_evt = ref_evt_items[0] if isinstance(ref_evt_items, list) else ref_evt_items
            builder_evt = builder_evt_items[0] if isinstance(builder_evt_items, list) else builder_evt_items

            print(f"\nFirst event comparison:")
            print(f"  Ref event keys: {sorted([k for k in ref_evt.keys() if not k.startswith('__')]) if isinstance(ref_evt, dict) else 'N/A'}")
            print(f"  Builder event keys: {sorted([k for k in builder_evt.keys() if not k.startswith('__')]) if isinstance(builder_evt, dict) else 'N/A'}")

            print_dict_comparison("event", ref_evt, builder_evt)

    # =====================================================================
    # 4. PLUGINS iOM STRUCTURE
    # =====================================================================
    print("\n" + "=" * 80)
    print("4. PLUGINS MAP (iOM) STRUCTURE COMPARISON")
    print("=" * 80)

    ref_plugins = ref_v.get("plugins", {})
    builder_plugins = builder_v.get("plugins", {})

    print(f"\nReference plugins __type: {ref_plugins.get('__type', 'NOT SET')}")
    print(f"Builder plugins __type: {builder_plugins.get('__type', 'NOT SET')}")

    ref_plugin_ids = [k for k in ref_plugins.keys() if not k.startswith("__")]
    builder_plugin_ids = [k for k in builder_plugins.keys() if not k.startswith("__")]

    print(f"\nReference plugin count: {len(ref_plugin_ids)}")
    print(f"Builder plugin count: {len(builder_plugin_ids)}")

    print(f"\nReference plugin IDs (first 20): {ref_plugin_ids[:20]}")
    print(f"Builder plugin IDs: {builder_plugin_ids}")

    # Check the structure of the first few plugins in each
    print(f"\n--- Plugin record wrapper structure ---")
    for source_name, plugins, ids in [("Reference", ref_plugins, ref_plugin_ids[:3]),
                                       ("Builder", builder_plugins, builder_plugin_ids[:3])]:
        for pid in ids:
            p = plugins[pid]
            if isinstance(p, dict):
                top_keys = [k for k in p.keys()]
                has_type = "__type" in p
                ptype = p.get("__type", "none")
                has_n = "n" in p
                has_v = "v" in p
                print(f"  {source_name} '{pid}': __type={ptype}, has n={has_n}, has v={has_v}, top_keys={top_keys[:5]}")
                if has_v:
                    v = p["v"]
                    if isinstance(v, dict):
                        v_keys = sorted([k for k in v.keys() if not k.startswith("__")])[:10]
                        print(f"    v keys (first 10): {v_keys}")

    # =====================================================================
    # 5. TOP-LEVEL appTemplate FIELDS
    # =====================================================================
    print("\n" + "=" * 80)
    print("5. TOP-LEVEL appTemplate FIELD COMPARISON")
    print("=" * 80)

    ref_top_keys = sorted([k for k in ref_v.keys() if not k.startswith("__")])
    builder_top_keys = sorted([k for k in builder_v.keys() if not k.startswith("__")])

    only_in_ref = set(ref_top_keys) - set(builder_top_keys)
    only_in_builder = set(builder_top_keys) - set(ref_top_keys)

    if only_in_ref:
        print(f"\nFields ONLY in reference: {sorted(only_in_ref)}")
    if only_in_builder:
        print(f"\nFields ONLY in builder: {sorted(only_in_builder)}")
    if not only_in_ref and not only_in_builder:
        print(f"\nAll top-level fields match!")

    # Compare values of shared fields (excluding plugins which we already compared)
    print(f"\nShared field value differences:")
    for key in sorted(set(ref_top_keys) & set(builder_top_keys)):
        if key in ("plugins",):
            continue
        rv = ref_v.get(key)
        bv = builder_v.get(key)
        if rv != bv:
            rv_str = json.dumps(rv, default=str)[:100]
            bv_str = json.dumps(bv, default=str)[:100]
            print(f"  '{key}':")
            print(f"    REF:     {rv_str}")
            print(f"    BUILDER: {bv_str}")

    # =====================================================================
    # 6. DETAILED: Template field comparison for similar widgets
    # =====================================================================
    print("\n" + "=" * 80)
    print("6. TEMPLATE FIELD COMPARISON - TextWidget2")
    print("=" * 80)

    ref_texts = find_plugins_with_type(ref, "TextWidget2")
    builder_texts = find_plugins_with_type(builder, "TextWidget2")

    if ref_texts and builder_texts:
        ref_tid, ref_text = ref_texts[0]
        builder_tid, builder_text = builder_texts[0]

        ref_tv = ref_text.get("v", ref_text)
        builder_tv = builder_text.get("v", builder_text)

        ref_tmpl = ref_tv.get("template", {})
        builder_tmpl = builder_tv.get("template", {})

        ref_tmpl_keys = sorted([k for k in ref_tmpl.keys() if not k.startswith("__")])
        builder_tmpl_keys = sorted([k for k in builder_tmpl.keys() if not k.startswith("__")])

        only_ref = set(ref_tmpl_keys) - set(builder_tmpl_keys)
        only_builder = set(builder_tmpl_keys) - set(ref_tmpl_keys)

        print(f"\nComparing ref '{ref_tid}' vs builder '{builder_tid}'")
        print(f"Ref template has {len(ref_tmpl_keys)} fields")
        print(f"Builder template has {len(builder_tmpl_keys)} fields")

        if only_ref:
            print(f"\nTemplate fields ONLY in reference: {sorted(only_ref)}")
            for k in sorted(only_ref):
                print(f"  {k} = {json.dumps(ref_tmpl[k], default=str)[:100]}")
        if only_builder:
            print(f"\nTemplate fields ONLY in builder: {sorted(only_builder)}")
            for k in sorted(only_builder):
                print(f"  {k} = {json.dumps(builder_tmpl[k], default=str)[:100]}")

    # =====================================================================
    # 7. DETAILED: Template field comparison for ButtonWidget2
    # =====================================================================
    print("\n" + "=" * 80)
    print("7. TEMPLATE FIELD COMPARISON - ButtonWidget2")
    print("=" * 80)

    ref_btns = find_plugins_with_type(ref, "ButtonWidget2")
    builder_btns = find_plugins_with_type(builder, "ButtonWidget2")

    if ref_btns and builder_btns:
        ref_bid, ref_btn = ref_btns[0]
        builder_bid, builder_btn = builder_btns[0]

        ref_bv = ref_btn.get("v", ref_btn)
        builder_bv = builder_btn.get("v", builder_btn)

        ref_tmpl = ref_bv.get("template", {})
        builder_tmpl = builder_bv.get("template", {})

        ref_tmpl_keys = sorted([k for k in ref_tmpl.keys() if not k.startswith("__")])
        builder_tmpl_keys = sorted([k for k in builder_tmpl.keys() if not k.startswith("__")])

        only_ref = set(ref_tmpl_keys) - set(builder_tmpl_keys)
        only_builder = set(builder_tmpl_keys) - set(ref_tmpl_keys)

        print(f"\nComparing ref '{ref_bid}' vs builder '{builder_bid}'")
        print(f"Ref template has {len(ref_tmpl_keys)} fields")
        print(f"Builder template has {len(builder_tmpl_keys)} fields")

        if only_ref:
            print(f"\nTemplate fields ONLY in reference: {sorted(only_ref)}")
            for k in sorted(only_ref):
                print(f"  {k} = {json.dumps(ref_tmpl[k], default=str)[:100]}")
        if only_builder:
            print(f"\nTemplate fields ONLY in builder: {sorted(only_builder)}")

    # =====================================================================
    # 8. DETAILED: JavascriptQuery template fields
    # =====================================================================
    print("\n" + "=" * 80)
    print("8. TEMPLATE FIELD COMPARISON - JavascriptQuery")
    print("=" * 80)

    ref_js = find_plugins_with_type(ref, "JavascriptQuery")
    builder_js = find_plugins_with_type(builder, "JavascriptQuery")

    if ref_js and builder_js:
        ref_jid, ref_jq = ref_js[0]
        builder_jid, builder_jq = builder_js[0]

        ref_jv = ref_jq.get("v", ref_jq)
        builder_jv = builder_jq.get("v", builder_jq)

        ref_tmpl = ref_jv.get("template", {})
        builder_tmpl = builder_jv.get("template", {})

        ref_tmpl_keys = sorted([k for k in ref_tmpl.keys() if not k.startswith("__")])
        builder_tmpl_keys = sorted([k for k in builder_tmpl.keys() if not k.startswith("__")])

        only_ref = set(ref_tmpl_keys) - set(builder_tmpl_keys)
        only_builder = set(builder_tmpl_keys) - set(ref_tmpl_keys)

        print(f"\nComparing ref '{ref_jid}' vs builder '{builder_jid}'")
        print(f"Ref template has {len(ref_tmpl_keys)} fields")
        print(f"Builder template has {len(builder_tmpl_keys)} fields")

        if only_ref:
            print(f"\nTemplate fields ONLY in reference: {sorted(only_ref)}")
            for k in sorted(only_ref):
                v = ref_tmpl[k]
                print(f"  {k} = {json.dumps(v, default=str)[:100]}")
        if only_builder:
            print(f"\nTemplate fields ONLY in builder: {sorted(only_builder)}")
            for k in sorted(only_builder):
                v = builder_tmpl[k]
                print(f"  {k} = {json.dumps(v, default=str)[:100]}")

    # =====================================================================
    # 9. RAW TRANSIT STRUCTURE - check iR/iOM wrapping
    # =====================================================================
    print("\n" + "=" * 80)
    print("9. RAW TRANSIT TAG CHECK - iR wrapping for plugins")
    print("=" * 80)

    # Check what the raw transit looks like for a plugin entry
    # We need to look at the raw JSON, not decoded
    ref_plugins_raw = ref_v.get("plugins", {})
    builder_plugins_raw = builder_v.get("plugins", {})

    for source, plugins, name in [(ref_plugins_raw, ref_plugin_ids[:2], "Reference"),
                                   (builder_plugins_raw, builder_plugin_ids[:2], "Builder")]:
        for pid in plugins:
            p = plugins[pid]
            if isinstance(p, dict):
                print(f"\n{name} '{pid}':")
                print(f"  Wrapper __type: {p.get('__type', 'NONE')}")
                print(f"  'n' value: {p.get('n', 'MISSING')}")
                if "v" in p:
                    v = p["v"]
                    print(f"  'v' is dict: {isinstance(v, dict)}")
                    print(f"  'v' has __type: {v.get('__type', 'NONE') if isinstance(v, dict) else 'N/A'}")

    # =====================================================================
    # 10. Check style field structure
    # =====================================================================
    print("\n" + "=" * 80)
    print("10. STYLE FIELD STRUCTURE")
    print("=" * 80)

    for source, plugins, ids, name in [(ref_plugins, ref_plugin_ids, ref_plugin_ids[:5], "Reference"),
                                        (builder_plugins, builder_plugin_ids, builder_plugin_ids[:5], "Builder")]:
        for pid in ids:
            p = plugins[pid]
            if isinstance(p, dict):
                pv = p.get("v", p)
                style = pv.get("style")
                if style is not None:
                    style_type = style.get("__type", "NONE") if isinstance(style, dict) else type(style).__name__
                    print(f"  {name} '{pid}' style __type: {style_type}, value: {json.dumps(style, default=str)[:80]}")


if __name__ == "__main__":
    main()
