"""Sample Marketplace Plugin: Git Quick Status & Log Viewer.

Push `plugins/git_quick/plugin.py` and `readme/git_quick/README.md` to
https://github.com/jaunchun-tech/clice-marketplace to test Clice's Marketplace!
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

from clice.core.plugins import ClicePlugin


class GitQuickWidget(Vertical):
    """Displays `git status -sb` and recent commits for the current directory."""

    BINDINGS = [
        Binding("r", "refresh_git", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal(classes="toolbar"):
            yield Static("[b #f97316][G] Git Quick (Plugin)[/b #f97316]", classes="app-title")
            yield Button("Refresh (R)", variant="primary", id="gitq-refresh")
        yield Static("", id="gitq-output", classes="metric-box")

    def on_mount(self) -> None:
        self._refresh()

    def action_refresh_git(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        out = self.query_one("#gitq-output", Static)
        try:
            st = subprocess.run(
                ["git", "status", "-sb"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5,
            )
            lg = subprocess.run(
                ["git", "log", "-n", "10", "--oneline"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
                timeout=5,
            )
            if st.returncode != 0:
                out.update(f"[yellow]Not a git repository:[/yellow] {Path.cwd()}")
                return
            out.update(
                f"[b]Repository:[/b] {Path.cwd()}\n\n"
                f"[b cyan]Status:[/b cyan]\n{st.stdout.strip()}\n\n"
                f"[b green]Recent Commits:[/b green]\n{lg.stdout.strip() or '(no commits yet)'}"
            )
        except Exception as exc:
            out.update(f"[red]Git error: {exc}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "gitq-refresh":
            self._refresh()


class GitQuickPlugin(ClicePlugin):
    id = "plugin_git_quick"
    name = "Git Quick"
    icon = "[G]"
    description = "Quick git status & commit log viewer for the current directory."
    version = "0.2.0"
    author = "Clice Marketplace"

    def create_widget(self) -> Vertical:
        return GitQuickWidget()
