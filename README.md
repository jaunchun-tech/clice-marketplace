# 🧩 Clice Plugin Development & Marketplace Guide

This folder contains the **plugin authoring documentation** and **ready-to-publish marketplace templates** for [`jaunchun-tech/clice-marketplace`](https://github.com/jaunchun-tech/clice-marketplace).

> **Note:** Plugins inside `marketplace/` are **not** bundled into Clice by default. Copy or push them to `https://github.com/jaunchun-tech/clice-marketplace` to test Clice's built-in GitHub Marketplace installer!

---

## 📁 Marketplace Repository Structure

Your GitHub marketplace repository (`jaunchun-tech/clice-marketplace`) should use this exact two-folder layout:

```text
clice-marketplace/
├── plugins/
│   └── <plugin_slug>/
│       └── plugin.py          # Required: contains a ClicePlugin subclass
└── readme/
    └── <plugin_slug>/
        ├── README.md          # Shown live inside Clice's Plugins & Marketplace tab!
        └── ...                # Optional assets (screenshots, docs, etc.)
```

---

## 🛠️ How to Write a Clice Plugin

1. Create `plugins/<plugin_slug>/plugin.py`
2. Subclass `ClicePlugin` from `clice.core.plugins`
3. Return a Textual `Widget` (such as `Vertical`) from `create_widget()`
4. Add `readme/<plugin_slug>/README.md` describing what your plugin does and its keyboard shortcuts.

### Minimal Example

```python
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Static

from clice.core.plugins import ClicePlugin


class MyToolWidget(Vertical):
    BINDINGS = [
        Binding("ctrl+r", "run_action", "Run"),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal(classes="toolbar"):
            yield Static("[b #a855f7][M] My Tool[/b #a855f7]", classes="app-title")
            yield Button("Run (^R)", variant="primary", id="my-run")
        yield Input(placeholder="Type input and press Enter...", id="my-input")
        yield Static("", id="my-output", classes="metric-box")

    def on_mount(self) -> None:
        self.query_one("#my-input", Input).focus()

    def action_run_action(self) -> None:
        val = self.query_one("#my-input", Input).value
        self.query_one("#my-output", Static).update(f"Result: {val}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.action_run_action()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "my-run":
            self.action_run_action()


class MyToolPlugin(ClicePlugin):
    id = "plugin_my_tool"       # Unique ID (must start with plugin_)
    name = "My Tool"            # Display name in Sidebar & Main Menu
    icon = "[M]"                # Crisp 3-char terminal-safe icon
    description = "Short description shown on the Main Menu rectangle."
    version = "0.1.0"
    author = "Your Name"

    def create_widget(self) -> Vertical:
        return MyToolWidget()
```

### Best Practices for Pro-Grade Clice Plugins
- **Keyboard-first**: Auto-focus your primary widget in `on_mount()` and define `BINDINGS` for common actions.
- **Terminal-safe icons**: Use crisp 2–3 char badges like `[G]`, `[D]`, `[#]` so alignment is pixel-perfect on Linux, macOS, and Windows.
- **Reuse Clice CSS classes**: Use `toolbar`, `app-title`, `metric-box`, `code-area`, and `status-strip` so your plugin automatically matches all 7 Clice themes!
- **Test locally before publishing**:
  ```bash
  clice --plugins-dir marketplace/plugins
  ```

---

## 🌐 Testing with `jaunchun-tech/clice-marketplace`

1. Push `plugins/git_quick/plugin.py` and `readme/git_quick/README.md` to `https://github.com/jaunchun-tech/clice-marketplace`.
2. Open **Clice** → **Plugins & Market**.
3. Switch to the **GitHub Marketplace** tab and click **Fetch Marketplace** — Clice will list plugins from `jaunchun-tech/clice-marketplace`, show their `readme/<slug>/README.md`, and install them into `~/.clice/plugins/` in one click!
