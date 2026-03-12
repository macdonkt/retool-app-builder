#!/usr/bin/env python3
"""
Incremental Retool app builder — one step at a time.
Each step adds one feature, generating stepN.json.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from tools.retool_builder import *

OUTPUT_DIR = os.path.dirname(__file__)


def step1():
    """Bare minimum: page + main frame + 1 text widget."""
    plugins = [
        ("page1", screen_plugin("page1", "Step 1 Test", "step-1-test", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),
        ("helloText", widget("helloText", "TextWidget2",
            txt_tmpl("# Hello World"),
            pos(0, 0, 4, 6, "", "page1"),
            screen="page1")),
    ]
    app = build_app(plugins)
    out = os.path.join(OUTPUT_DIR, "step1.json")
    save_app(app, out, "Step 1 Test")
    return out


def step2():
    """Step 1 + a table with static inline data."""
    columns = [
        table_col("id", "ID", fmt="decimal", size=60, alignment="right"),
        table_col("name", "Name", fmt="string", size=200),
        table_col("price", "Price", fmt="decimal", size=100, alignment="right"),
    ]

    static_data = '[{"id":1,"name":"Wireless Mouse","price":29.99},{"id":2,"name":"USB-C Hub","price":49.99},{"id":3,"name":"Standing Desk Mat","price":39.99}]'

    plugins = [
        ("page1", screen_plugin("page1", "Step 2 Test", "step-2-test", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),
        ("helloText", widget("helloText", "TextWidget2",
            txt_tmpl("# Hello World"),
            pos(0, 0, 4, 6, "", "page1"),
            screen="page1")),
        ("itemsTable", widget("itemsTable", "TableWidget2",
            table_tmpl(static_data, columns=columns),
            pos(5, 0, 40, 12, "", "page1"),
            screen="page1")),
    ]
    app = build_app(plugins)
    out = os.path.join(OUTPUT_DIR, "step2.json")
    save_app(app, out, "Step 2 Test")
    return out


def step3():
    """Step 2 but table data comes from a JS query."""
    columns = [
        table_col("id", "ID", fmt="decimal", size=60, alignment="right"),
        table_col("name", "Name", fmt="string", size=200),
        table_col("price", "Price", fmt="decimal", size=100, alignment="right"),
    ]

    mock_js = """return [
  {id: 1, name: "Wireless Mouse", price: 29.99},
  {id: 2, name: "USB-C Hub", price: 49.99},
  {id: 3, name: "Standing Desk Mat", price: 39.99},
  {id: 4, name: "Mechanical Keyboard", price: 89.99},
  {id: 5, name: "Monitor Light Bar", price: 34.99}
]"""

    plugins = [
        ("page1", screen_plugin("page1", "Step 3 Test", "step-3-test", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),
        ("helloText", widget("helloText", "TextWidget2",
            txt_tmpl("# Items (from JS query)"),
            pos(0, 0, 4, 8, "", "page1"),
            screen="page1")),
        ("fetchItems", query("fetchItems", "JavascriptQuery",
            js_tmpl(mock_js, run_on_load=True),
            screen="page1")),
        ("itemsTable", widget("itemsTable", "TableWidget2",
            table_tmpl("{{ fetchItems.data }}", columns=columns),
            pos(5, 0, 40, 12, "", "page1"),
            screen="page1")),
    ]
    app = build_app(plugins)
    out = os.path.join(OUTPUT_DIR, "step3.json")
    save_app(app, out, "Step 3 Test")
    return out


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "1"
    steps = {"1": step1, "2": step2, "3": step3}
    if step in steps:
        path = steps[step]()
        print(f"\nBuilt step {step}: {path}")
    else:
        print(f"Unknown step: {step}. Available: {', '.join(sorted(steps.keys()))}")
