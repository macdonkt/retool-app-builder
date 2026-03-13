#!/usr/bin/env python3
"""
Test Build 1: Reference-Driven approach
Components: page + frame + TextWidget2 + ButtonWidget2

All template fields are copied from transit_patterns.json (golden reference),
with only text/value/events modified.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from tools.retool_core import *


def build():
    plugins = [
        # ── Screen ──
        ("page1", screen_plugin("page1", "Test Build 1", "test-build-1", 0)),

        # ── Main Frame ──
        ("$main", frame_plugin("$main", "page1", "main")),

        # ── TextWidget2 ──
        # ALL fields copied from transit_patterns.json TextWidget2 template
        # Only changed: value
        ("titleText", widget("titleText", "TextWidget2",
            tom(
                "heightType", "auto",
                "horizontalAlign", "left",
                "hidden", False,
                "imageWidth", "fit",
                "margin", "4px 8px",
                "showInEditor", False,
                "verticalAlign", "center",
                "tooltipText", "",
                "value", "# Reference-Driven Build Test",   # ← CHANGED
                "disableMarkdown", False,
                "overflowType", "scroll",
                "maintainSpaceWhenHidden", False,
                "events", tlist([]),                         # ← tlist, not plain []
            ),
            pos(0, 0, 6, 8, "", "page1"),
            screen="page1")),

        # ── ButtonWidget2 ──
        # ALL fields copied from transit_patterns.json ButtonWidget2 template
        # Only changed: text, events
        ("testButton", widget("testButton", "ButtonWidget2",
            tom(
                "heightType", "fixed",
                "horizontalAlign", "stretch",
                "clickable", False,
                "iconAfter", "",
                "submitTargetId", None,
                "hidden", False,
                "ariaLabel", "",
                "text", "Click Me",                          # ← CHANGED
                "margin", "4px 8px",
                "showInEditor", False,
                "tooltipText", "",
                "allowWrap", True,
                "styleVariant", "solid",
                "submit", False,
                "iconBefore", "",
                "events", tlist([                            # ← CHANGED (tlist, not plain [])
                    evt_notification("click", "success", "It works!", "Reference-driven build successful"),
                ]),
                "loading", False,
                "loaderPosition", "auto",
                "disabled", False,
                "maintainSpaceWhenHidden", False,
            ),
            pos(0, 8, 5, 2, "", "page1"),
            screen="page1")),
    ]

    app = build_app(plugins)
    out = os.path.join(os.path.dirname(__file__), "test1.json")
    save_app(app, out, "Test Build 1")
    return out


if __name__ == "__main__":
    build()
