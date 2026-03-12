#!/usr/bin/env python3
"""
CRUD Dashboard Test App — validates the full Retool builder pipeline.

Generates a complete Item Manager app with:
- Table with proper column maps, search, pagination
- Add/Edit modal with form inputs
- Delete confirmation modal
- State variables for selection tracking
- Query chaining (submit -> refresh -> notify)

Usage:
    python3 "apps/Time on site 2/build_crud_test.py"
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from tools.retool_builder import *

# ══════════════════════════════════════════════════════════════════════════════
# MOCK DATA
# ══════════════════════════════════════════════════════════════════════════════

FETCH_ITEMS_JS = """
return [
  {id: 1, name: "Widget A", category: "Electronics", price: 29.99, stock: 150, created_at: "2025-01-15"},
  {id: 2, name: "Gadget B", category: "Electronics", price: 49.99, stock: 75, created_at: "2025-02-20"},
  {id: 3, name: "Tool C", category: "Hardware", price: 15.50, stock: 200, created_at: "2025-03-10"},
  {id: 4, name: "Part D", category: "Hardware", price: 8.99, stock: 500, created_at: "2025-04-05"},
  {id: 5, name: "Supply E", category: "Office", price: 12.00, stock: 300, created_at: "2025-05-18"},
  {id: 6, name: "Device F", category: "Electronics", price: 99.99, stock: 25, created_at: "2025-06-22"},
  {id: 7, name: "Material G", category: "Raw", price: 5.75, stock: 1000, created_at: "2025-07-30"},
  {id: 8, name: "Component H", category: "Hardware", price: 22.50, stock: 120, created_at: "2025-08-14"},
];
""".strip()

SAVE_ITEM_JS = """
// Delegates to create or update based on isEditing state
if (isEditing.value) {
  const row = selectedRow.value;
  console.log("Updating item:", row.id, {
    name: nameInput.value,
    category: categorySelect.value,
    price: priceInput.value,
    stock: stockInput.value
  });
  return {success: true, action: "updated", id: row.id};
} else {
  console.log("Creating new item:", {
    name: nameInput.value,
    category: categorySelect.value,
    price: priceInput.value,
    stock: stockInput.value
  });
  return {success: true, action: "created", id: Date.now()};
}
""".strip()

DELETE_ITEM_JS = """
const row = selectedRow.value;
console.log("Deleting item:", row.id, row.name);
return {success: true, action: "deleted", id: row.id};
""".strip()

# ══════════════════════════════════════════════════════════════════════════════
# TABLE COLUMNS & ACTIONS
# ══════════════════════════════════════════════════════════════════════════════

columns = [
    table_col("id", "ID", fmt="decimal", size=60, alignment="center"),
    table_col("name", "Name", fmt="string", size=200),
    table_col("category", "Category", fmt="tag", size=120),
    table_col("price", "Price", fmt="decimal", size=100, alignment="right"),
    table_col("stock", "Stock", fmt="decimal", size=80, alignment="right"),
    table_col("created_at", "Created", fmt="date", size=120),
]

edit_action = table_action("Edit", icon="bold/interface-edit-pencil")
delete_action = table_action("Delete", icon="bold/interface-delete-bin-2")

# ══════════════════════════════════════════════════════════════════════════════
# EVENT HANDLERS
# ══════════════════════════════════════════════════════════════════════════════

# Save query: onSuccess -> refresh table + hide modal + notify
save_events = [
    evt_trigger_query("success", "fetchItems"),
    evt_hide_frame("success", "addEditModal"),
    evt_notification("success", "success", "Success",
                     "{{ saveItem.data.action === 'created' ? 'Item created' : 'Item updated' }}"),
    evt_notification("failure", "error", "Error", "Failed to save item"),
]

# Delete query: onSuccess -> refresh table + hide modal + notify
delete_events = [
    evt_trigger_query("success", "fetchItems"),
    evt_hide_frame("success", "deleteModal"),
    evt_notification("success", "success", "Deleted", "Item deleted successfully"),
    evt_notification("failure", "error", "Error", "Failed to delete item"),
]

# Add button: set isEditing=false, show modal
add_btn_events = [
    evt_set_var("click", "isEditing", "false"),
    evt_show_frame("click", "addEditModal"),
]

# Table Edit action: set selectedRow, set isEditing=true, show modal
table_edit_events = [
    evt_set_var("clickAction", "selectedRow", "{{ itemsTable.selectedRow }}"),
    evt_set_var("clickAction", "isEditing", "true"),
    evt_show_frame("clickAction", "addEditModal"),
]

# Table Delete action: set selectedRow, show delete modal
table_delete_events = [
    evt_set_var("clickAction", "selectedRow", "{{ itemsTable.selectedRow }}"),
    evt_show_frame("clickAction", "deleteModal"),
]

# Combine table events (both actions fire on clickAction, targeted by actionId)
# In Retool, action clicks on the table use the clickAction event
table_events = table_edit_events + table_delete_events

# ══════════════════════════════════════════════════════════════════════════════
# PLUGINS
# ══════════════════════════════════════════════════════════════════════════════

plugins = [
    # --- Structure ---
    ("page1", screen_plugin("page1", "Item Manager", "item-manager", 0)),
    ("$main", frame_plugin("$main", "page1", "main")),
    ("addEditModal", modal_plugin("addEditModal", "page1", size="medium")),
    ("deleteModal", modal_plugin("deleteModal", "page1", size="small")),

    # --- State Variables ---
    ("selectedRow", state_var("selectedRow", "{}", screen="page1")),
    ("isEditing", state_var("isEditing", "false", screen="page1")),

    # --- Queries ---
    ("fetchItems", query("fetchItems", "JavascriptQuery",
        js_tmpl(FETCH_ITEMS_JS, run_on_load=True),
        screen="page1")),

    ("saveItem", query("saveItem", "JavascriptQuery",
        js_tmpl(SAVE_ITEM_JS, events=save_events),
        screen="page1")),

    ("deleteItem", query("deleteItem", "JavascriptQuery",
        js_tmpl(DELETE_ITEM_JS, events=delete_events),
        screen="page1")),

    # --- Main Page Widgets ---
    ("appTitle", widget("appTitle", "TextWidget2",
        txt_tmpl("# Item Manager"),
        pos(0, 0, 4, 8, "$main", "page1"),
        screen="page1")),

    ("appSubtitle", widget("appSubtitle", "TextWidget2",
        txt_tmpl("CRUD Dashboard Test"),
        pos(0, 8, 4, 4, "$main", "page1"),
        screen="page1")),

    ("controlsBar", widget("controlsBar", "ContainerWidget2",
        container_tmpl(show_border=False, padding="0px"),
        pos(5, 0, 7, 12, "$main", "page1"),
        screen="page1")),

    ("searchInput", widget("searchInput", "TextInputWidget2",
        textinput_tmpl("", "Search items..."),
        pos(0, 0, 5, 5, "controlsBar", "page1"),
        screen="page1")),

    ("addButton", widget("addButton", "ButtonWidget2",
        btn_tmpl("+ Add Item", events=add_btn_events),
        pos(0, 8, 5, 2, "controlsBar", "page1"),
        screen="page1")),

    ("refreshButton", widget("refreshButton", "ButtonWidget2",
        btn_tmpl("Refresh", events=[evt_trigger_query("click", "fetchItems")]),
        pos(0, 10, 5, 2, "controlsBar", "page1"),
        screen="page1")),

    ("itemsTable", widget("itemsTable", "TableWidget2",
        table_tmpl(
            data="{{ fetchItems.data }}",
            columns=columns,
            actions=[edit_action, delete_action],
            events=table_events,
        ),
        pos(13, 0, 50, 12, "$main", "page1"),
        screen="page1")),

    # --- Add/Edit Modal: Header ---
    ("modalTitle", widget("modalTitle", "TextWidget2",
        txt_tmpl("{{ isEditing.value ? '#### Edit Item' : '#### Add New Item' }}"),
        pos(0, 0, 3, 12, "addEditModal", "page1", row_group="header"),
        screen="page1")),

    # --- Add/Edit Modal: Body ---
    ("nameInput", widget("nameInput", "TextInputWidget2",
        textinput_tmpl("Name", "Enter item name",
                       value="{{ isEditing.value ? selectedRow.value.name : '' }}"),
        pos(0, 0, 5, 12, "addEditModal", "page1"),
        screen="page1")),

    ("categorySelect", widget("categorySelect", "SelectWidget2",
        select_tmpl("Category",
                    values='["Electronics", "Hardware", "Office", "Raw"]',
                    labels='["Electronics", "Hardware", "Office", "Raw"]',
                    placeholder="Select category..."),
        pos(6, 0, 5, 6, "addEditModal", "page1"),
        screen="page1")),

    ("priceInput", widget("priceInput", "NumberInputWidget",
        numberinput_tmpl("Price", placeholder="0.00",
                         value="{{ isEditing.value ? selectedRow.value.price : '' }}",
                         min_val=0),
        pos(6, 6, 5, 6, "addEditModal", "page1"),
        screen="page1")),

    ("stockInput", widget("stockInput", "NumberInputWidget",
        numberinput_tmpl("Stock", placeholder="0",
                         value="{{ isEditing.value ? selectedRow.value.stock : '' }}",
                         min_val=0),
        pos(12, 0, 5, 6, "addEditModal", "page1"),
        screen="page1")),

    # --- Add/Edit Modal: Footer ---
    ("cancelBtn", widget("cancelBtn", "ButtonWidget2",
        btn_tmpl("Cancel", events=[evt_hide_frame("click", "addEditModal")],
                 variant="outline"),
        pos(0, 0, 5, 2, "addEditModal", "page1", row_group="footer"),
        screen="page1")),

    ("saveBtn", widget("saveBtn", "ButtonWidget2",
        btn_tmpl("{{ isEditing.value ? 'Update' : 'Create' }}",
                 events=[evt_trigger_query("click", "saveItem")]),
        pos(0, 2, 5, 2, "addEditModal", "page1", row_group="footer"),
        screen="page1")),

    # --- Delete Modal: Header ---
    ("deleteTitle", widget("deleteTitle", "TextWidget2",
        txt_tmpl("#### Confirm Delete"),
        pos(0, 0, 3, 12, "deleteModal", "page1", row_group="header"),
        screen="page1")),

    # --- Delete Modal: Body ---
    ("deleteMsg", widget("deleteMsg", "TextWidget2",
        txt_tmpl("Are you sure you want to delete **{{ selectedRow.value.name }}**? This action cannot be undone."),
        pos(0, 0, 5, 12, "deleteModal", "page1"),
        screen="page1")),

    # --- Delete Modal: Footer ---
    ("delCancelBtn", widget("delCancelBtn", "ButtonWidget2",
        btn_tmpl("Cancel", events=[evt_hide_frame("click", "deleteModal")],
                 variant="outline"),
        pos(0, 0, 5, 2, "deleteModal", "page1", row_group="footer"),
        screen="page1")),

    ("delConfirmBtn", widget("delConfirmBtn", "ButtonWidget2",
        btn_tmpl("Delete", events=[evt_trigger_query("click", "deleteItem")],
                 danger=True),
        pos(0, 2, 5, 2, "deleteModal", "page1", row_group="footer"),
        screen="page1")),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = build_app(plugins)
    output = os.path.join(os.path.dirname(__file__), "crud-dashboard.json")
    save_app(app, output, "CRUD Dashboard")
