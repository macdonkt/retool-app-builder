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


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else "1"
    steps = {"1": step1}
    if step in steps:
        path = steps[step]()
        print(f"\nBuilt step {step}: {path}")
    else:
        print(f"Unknown step: {step}. Available: {', '.join(sorted(steps.keys()))}")
