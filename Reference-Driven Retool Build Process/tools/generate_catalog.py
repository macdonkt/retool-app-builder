#!/usr/bin/env python3
"""
Generate refs/widget_catalog.md from transit_patterns.json.

This creates a human-readable index of all widget types, query types,
and event patterns available in the golden reference. Use it for quick
lookup — but always read transit_patterns.json for the full field structure
when building components.

Usage:
    python3 tools/generate_catalog.py
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PATTERNS_PATH = os.path.join(SCRIPT_DIR, "transit_patterns.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "refs", "widget_catalog.md")

# Fields that are typically customized (vs left as defaults)
KEY_FIELDS = {
    "text", "value", "label", "placeholder", "data", "events", "hidden",
    "disabled", "src", "options", "values", "defaultValue", "columnOrdering",
    "_columnIds", "selectedRowKey", "query", "runWhenModelUpdates",
    "runWhenPageLoads", "showSuccessToaster", "showFailureToaster",
    "queryTimeout", "confirmMessage", "notificationDuration",
    "enableTransformer", "transformer", "importedQueryInputs",
}


def classify_field(key, value):
    """Classify a field as key-configurable, structural, or default."""
    if key in KEY_FIELDS:
        return "key"
    if isinstance(value, (dict, list)) and len(str(value)) > 100:
        return "complex"
    return "default"


def format_value_preview(value):
    """Short preview of a field's default value."""
    if value is None:
        return "`null`"
    if isinstance(value, bool):
        return f"`{str(value).lower()}`"
    if isinstance(value, str):
        if len(value) > 40:
            return f'`"{value[:37]}..."`'
        return f'`"{value}"`'
    if isinstance(value, (int, float)):
        return f"`{value}`"
    if isinstance(value, list):
        return f"`[{len(value)} items]`"
    if isinstance(value, dict):
        return f"`{{...{len(value)} keys}}`"
    return f"`{type(value).__name__}`"


def main():
    with open(PATTERNS_PATH) as f:
        data = json.load(f)

    lines = []
    lines.append("# Widget & Query Catalog")
    lines.append("")
    lines.append("Auto-generated from `transit_patterns.json`. Use this for quick lookup.")
    lines.append("**For the full field structure, always read transit_patterns.json directly.**")
    lines.append("")
    lines.append(f"- **{len(data['widget_templates'])} widget types**")
    lines.append(f"- **{len(data['query_templates'])} query types**")
    lines.append(f"- **{len(data.get('state_templates', {}))} state templates**")
    lines.append(f"- **{len(data.get('frame_templates', {}))} frame templates**")
    lines.append(f"- **{len(data.get('event_patterns', []))} event patterns**")
    lines.append("")

    # ── Widget Templates ──
    lines.append("---")
    lines.append("## Widget Types")
    lines.append("")

    for subtype, info in sorted(data["widget_templates"].items()):
        template = info.get("template", {})
        total = len(template)
        key_fields = [k for k in template if k in KEY_FIELDS]
        example_id = info.get("example_id", "?")

        lines.append(f"### {subtype}")
        lines.append(f"- Example ID: `{example_id}`")
        lines.append(f"- Total fields: **{total}**")

        if key_fields:
            lines.append(f"- Key configurable fields: {', '.join(f'`{k}`' for k in key_fields)}")

        # Show key fields with their defaults
        if key_fields:
            lines.append("")
            lines.append("| Field | Default |")
            lines.append("|-------|---------|")
            for k in key_fields:
                lines.append(f"| `{k}` | {format_value_preview(template[k])} |")

        lines.append("")

    # ── Query Templates ──
    lines.append("---")
    lines.append("## Query Types")
    lines.append("")

    for subtype, info in sorted(data["query_templates"].items()):
        template = info.get("template", {})
        total = len(template)
        example_id = info.get("example_id", "?")

        lines.append(f"### {subtype}")
        lines.append(f"- Example ID: `{example_id}`")
        lines.append(f"- Total fields: **{total}**")

        # Show all fields for queries (they're fewer and all important)
        key_q_fields = [k for k in template if k in KEY_FIELDS or k in {
            "query", "src", "runWhenModelUpdates", "runWhenPageLoads",
            "showSuccessToaster", "showFailureToaster", "queryTimeout",
            "enableTransformer", "transformer", "importedQueryInputs",
            "resourceTypeOverride", "confirmMessage",
        }]
        if key_q_fields:
            lines.append("")
            lines.append("| Field | Default |")
            lines.append("|-------|---------|")
            for k in key_q_fields:
                lines.append(f"| `{k}` | {format_value_preview(template.get(k))} |")

        lines.append("")

    # ── Frame Templates ──
    lines.append("---")
    lines.append("## Frame Types")
    lines.append("")

    for subtype, info in sorted(data.get("frame_templates", {}).items()):
        template = info.get("template", {})
        total = len(template)
        lines.append(f"### {subtype}")
        lines.append(f"- Total fields: **{total}**")
        lines.append(f"- Fields: {', '.join(f'`{k}`' for k in template.keys())}")
        lines.append("")

    # ── Event Patterns ──
    lines.append("---")
    lines.append("## Event Patterns")
    lines.append("")
    lines.append("These are real event handler structures extracted from the components example.")
    lines.append("Each event uses `tom()` (ordered map) encoding — NEVER `tmap()`.")
    lines.append("")

    event_patterns = data.get("event_patterns", [])
    if isinstance(event_patterns, list):
        # Group by event type
        by_event = {}
        for ep in event_patterns:
            if isinstance(ep, dict):
                evt_name = ep.get("event", "unknown")
                method = ep.get("method", "?")
                key = f"{evt_name} → {method}"
                if key not in by_event:
                    by_event[key] = ep

        lines.append(f"**{len(by_event)} unique event patterns:**")
        lines.append("")
        lines.append("| Event | Method | Type | Plugin ID |")
        lines.append("|-------|--------|------|-----------|")
        for key, ep in sorted(by_event.items()):
            lines.append(f"| `{ep.get('event', '?')}` | `{ep.get('method', '?')}` | `{ep.get('type', '?')}` | `{ep.get('pluginId', '')}` |")
        lines.append("")

    # ── State Templates ──
    if data.get("state_templates"):
        lines.append("---")
        lines.append("## State Variable Templates")
        lines.append("")
        for name, info in data["state_templates"].items():
            lines.append(f"- **{name}**: `{info.get('template', {})}`")
        lines.append("")

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated: {OUTPUT_PATH}")
    print(f"  Widget types: {len(data['widget_templates'])}")
    print(f"  Query types: {len(data['query_templates'])}")


if __name__ == "__main__":
    main()
