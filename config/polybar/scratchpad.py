#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = str(Path(__file__).resolve())

ICONS = {
    "firefox": ("🌐", "Firefox"),
    "chromium": ("🌐", "Chromium"),
    "chrome": ("🌐", "Chrome"),
    "terminator": ("⌨", "Terminal"),
    "gnome-terminal": ("⌨", "Terminal"),
    "kitty": ("⌨", "Terminal"),
    "thunar": ("📁", "Files"),
    "nautilus": ("📁", "Files"),
    "telegram": ("💬", "Telegram"),
    "code": ("⌨", "VS Code"),
    "discord": ("💬", "Discord"),
}


def get_tree():
    result = subprocess.run(
        ["i3-msg", "-t", "get_tree"],
        capture_output=True,
        text=True,
        check=True,
        timeout=3,
    )
    return json.loads(result.stdout)


def children(node):
    return node.get("nodes", []) + node.get("floating_nodes", [])


def walk(node):
    yield node
    for child in children(node):
        yield from walk(child)


def hidden_windows():
    tree = get_tree()

    scratch = next(
        (
            node for node in walk(tree)
            if node.get("type") == "workspace"
            and node.get("name") == "__i3_scratch"
        ),
        None,
    )

    if scratch is None:
        return []

    windows = []

    # Only count actual application windows.
    for container in children(scratch):
        leaf = next(
            (
                node for node in walk(container)
                if node.get("window") is not None
            ),
            None,
        )

        if leaf is None:
            continue

        props = leaf.get("window_properties") or {}
        app_class = props.get("class") or props.get("instance") or ""
        title = leaf.get("name") or app_class or "Window"

        icon, label = ("▣", app_class or "Window")

        for key, value in ICONS.items():
            if key in app_class.lower():
                icon, label = value
                break

        windows.append({
            "id": leaf["id"],
            "icon": icon,
            "label": label,
            "title": title,
        })

    return windows


def restore(window_id):
    ids = {str(w["id"]) for w in hidden_windows()}

    if window_id not in ids:
        return

    # Show the selected window, then return it to tiling.
    command = (
        f"[con_id={window_id}] scratchpad show; "
        f"[con_id={window_id}] floating disable"
    )

    subprocess.run(["i3-msg", command], check=False)


def show_menu():
    windows = hidden_windows()

    if not windows:
        return

    choices = [
        f"{i + 1}. {w['icon']} {w['label']} — {w['title'][:65]}"
        for i, w in enumerate(windows)
    ]

    result = subprocess.run(
        ["rofi", "-dmenu", "-i", "-p", "Hidden windows"],
        input="\n".join(choices) + "\n",
        capture_output=True,
        text=True,
    )

    selection = result.stdout.strip()

    if result.returncode == 0 and selection in choices:
        index = choices.index(selection)
        restore(str(windows[index]["id"]))


def show_bar():
    windows = hidden_windows()

    if not windows:
        print("")
        return

    items = []

    for window in windows:
        command = f"python3 {SCRIPT} restore {window['id']}"
        label = f"{window['icon']} {window['label']}"

        items.append(f"%{{A1:{command}:}}{label}%{{A}}")

    print("  ".join(items))


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 3 and sys.argv[1] == "restore":
            restore(sys.argv[2])
        elif len(sys.argv) >= 2 and sys.argv[1] == "menu":
            show_menu()
        else:
            show_bar()
    except Exception as exc:
        print(f"Scratchpad error: {exc}", file=sys.stderr)
        if len(sys.argv) == 1:
            print("")
