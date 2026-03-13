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


def step4():
    """Step 3 + button that opens an EMPTY modal (no children). Tests event handlers."""
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
        # Page + frame
        ("page1", screen_plugin("page1", "Step 4 Test", "step-4-test", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),

        # Title + Add button (opens modal)
        ("titleText", widget("titleText", "TextWidget2",
            txt_tmpl("# Items"),
            pos(0, 0, 4, 6, "", "page1"),
            screen="page1")),
        ("addButton", widget("addButton", "ButtonWidget2",
            btn_tmpl("+ Add Item", events=[
                evt_show_frame("click", "addModal"),
            ]),
            pos(0, 8, 5, 2, "", "page1"),
            screen="page1")),

        # Query + Table
        ("fetchItems", query("fetchItems", "JavascriptQuery",
            js_tmpl(mock_js, run_on_load=True),
            screen="page1")),
        ("itemsTable", widget("itemsTable", "TableWidget2",
            table_tmpl("{{ fetchItems.data }}", columns=columns),
            pos(6, 0, 40, 12, "", "page1"),
            screen="page1")),

        # Empty modal — no children
        ("addModal", modal_plugin("addModal", "page1", size="medium")),
    ]
    app = build_app(plugins)
    out = os.path.join(OUTPUT_DIR, "step4.json")
    save_app(app, out, "Step 4 Test")
    return out


def step5():
    """Step 4 + state variable, event chaining, modal with children.
    Tests: state_var, evt_set_var on query success,
           modal children (header/body/footer), evt_hide_frame, evt_notification.
    """
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
        # Page + frame
        ("page1", screen_plugin("page1", "Step 5 Test", "step-5-test", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),

        # State variable — item count
        ("itemCount", state_var("itemCount", value="0")),

        # Title shows dynamic count
        ("titleText", widget("titleText", "TextWidget2",
            txt_tmpl("# Items ({{ itemCount.value }})"),
            pos(0, 0, 4, 6, "", "page1"),
            screen="page1")),

        # Add button — opens modal
        ("addButton", widget("addButton", "ButtonWidget2",
            btn_tmpl("+ Add Item", events=[
                evt_show_frame("click", "addModal"),
            ]),
            pos(0, 8, 5, 2, "", "page1"),
            screen="page1")),

        # Query: fetch items, onSuccess → set itemCount via event handler
        ("fetchItems", query("fetchItems", "JavascriptQuery",
            js_tmpl(mock_js, run_on_load=True, events=[
                evt_set_var("success", "itemCount", "{{ fetchItems.data.length }}"),
            ]),
            screen="page1")),

        # Table
        ("itemsTable", widget("itemsTable", "TableWidget2",
            table_tmpl("{{ fetchItems.data }}", columns=columns),
            pos(6, 0, 40, 12, "", "page1"),
            screen="page1")),

        # Modal frame
        ("addModal", modal_plugin("addModal", "page1", size="medium")),

        # Modal header: title
        ("modalTitle", widget("modalTitle", "TextWidget2",
            txt_tmpl("#### Add New Item"),
            pos(0, 0, 3, 12, "addModal", "page1", row_group="header"),
            screen="page1")),

        # Modal body: name input
        ("nameInput", widget("nameInput", "TextInputWidget2",
            textinput_tmpl("Name", "Enter item name"),
            pos(0, 0, 7, 6, "addModal", "page1", row_group="body"),
            screen="page1")),

        # Modal body: price input
        ("priceInput", widget("priceInput", "TextInputWidget2",
            textinput_tmpl("Price", "0.00"),
            pos(0, 6, 7, 6, "addModal", "page1", row_group="body"),
            screen="page1")),

        # Modal footer: cancel button
        ("cancelButton", widget("cancelButton", "ButtonWidget2",
            btn_tmpl("Cancel", variant="outline", events=[
                evt_hide_frame("click", "addModal"),
            ]),
            pos(0, 0, 5, 2, "addModal", "page1", row_group="footer"),
            screen="page1")),

        # Modal footer: save button (shows notification + hides modal)
        ("saveButton", widget("saveButton", "ButtonWidget2",
            btn_tmpl("Save", events=[
                evt_notification("click", "success", "Item saved", "The item was added successfully."),
                evt_hide_frame("click", "addModal"),
            ]),
            pos(0, 2, 5, 2, "addModal", "page1", row_group="footer"),
            screen="page1")),
    ]
    app = build_app(plugins)
    out = os.path.join(OUTPUT_DIR, "step5.json")
    save_app(app, out, "Step 5 Test")
    return out


def step6():
    """Step 5 + SQL query (Retool DB). Tests sql_tmpl() structure alongside JS mock.

    The SQL query uses a placeholder resource UUID. After import:
    1. Open the fetchItemsSQL query in Retool
    2. Change the resource to your Retool DB
    3. Create the 'items' table using mock_data.sql
    4. Run the query to verify
    """
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
        # Page + frame
        ("page1", screen_plugin("page1", "Step 6 Test", "step-6-test", 0)),
        ("$main", frame_plugin("$main", "page1", "main")),

        # State variable — item count
        ("itemCount", state_var("itemCount", value="0")),

        # Title shows dynamic count
        ("titleText", widget("titleText", "TextWidget2",
            txt_tmpl("# Items ({{ itemCount.value }})"),
            pos(0, 0, 4, 6, "", "page1"),
            screen="page1")),

        # Add button — opens modal
        ("addButton", widget("addButton", "ButtonWidget2",
            btn_tmpl("+ Add Item", events=[
                evt_show_frame("click", "addModal"),
            ]),
            pos(0, 8, 5, 2, "", "page1"),
            screen="page1")),

        # JS mock query (still drives the table as fallback)
        ("fetchItems", query("fetchItems", "JavascriptQuery",
            js_tmpl(mock_js, run_on_load=True, events=[
                evt_set_var("success", "itemCount", "{{ fetchItems.data.length }}"),
            ]),
            screen="page1")),

        # SQL query — placeholder UUID, not run on load
        # After import: change resource to your Retool DB, then enable run on load
        ("fetchItemsSQL", query("fetchItemsSQL", "SqlQueryUnified",
            sql_tmpl("SELECT id, name, price FROM items ORDER BY id",
                     run_on_load=False),
            resource_uuid="REPLACE-WITH-YOUR-RETOOL-DB-UUID",
            resource_name="retool_db",
            screen="page1")),

        # Table (uses JS mock for now)
        ("itemsTable", widget("itemsTable", "TableWidget2",
            table_tmpl("{{ fetchItems.data }}", columns=columns),
            pos(6, 0, 40, 12, "", "page1"),
            screen="page1")),

        # Modal frame
        ("addModal", modal_plugin("addModal", "page1", size="medium")),

        # Modal header: title
        ("modalTitle", widget("modalTitle", "TextWidget2",
            txt_tmpl("#### Add New Item"),
            pos(0, 0, 3, 12, "addModal", "page1", row_group="header"),
            screen="page1")),

        # Modal body: name input
        ("nameInput", widget("nameInput", "TextInputWidget2",
            textinput_tmpl("Name", "Enter item name"),
            pos(0, 0, 7, 6, "addModal", "page1", row_group="body"),
            screen="page1")),

        # Modal body: price input
        ("priceInput", widget("priceInput", "TextInputWidget2",
            textinput_tmpl("Price", "0.00"),
            pos(0, 6, 7, 6, "addModal", "page1", row_group="body"),
            screen="page1")),

        # Modal footer: cancel button
        ("cancelButton", widget("cancelButton", "ButtonWidget2",
            btn_tmpl("Cancel", variant="outline", events=[
                evt_hide_frame("click", "addModal"),
            ]),
            pos(0, 0, 5, 2, "addModal", "page1", row_group="footer"),
            screen="page1")),

        # Modal footer: save button
        ("saveButton", widget("saveButton", "ButtonWidget2",
            btn_tmpl("Save", events=[
                evt_notification("click", "success", "Item saved", "The item was added successfully."),
                evt_hide_frame("click", "addModal"),
            ]),
            pos(0, 2, 5, 2, "addModal", "page1", row_group="footer"),
            screen="page1")),
    ]
    app = build_app(plugins)
    out = os.path.join(OUTPUT_DIR, "step6.json")
    save_app(app, out, "Step 6 Test")
    return out


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "1"
    steps = {"1": step1, "2": step2, "3": step3, "4": step4, "5": step5, "6": step6}
    if step in steps:
        path = steps[step]()
        print(f"\nBuilt step {step}: {path}")
    else:
        print(f"Unknown step: {step}. Available: {', '.join(sorted(steps.keys()))}")
