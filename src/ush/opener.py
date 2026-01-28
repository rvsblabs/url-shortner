"""Opens shortcuts. Currently supports URLs; extensible for files later."""

import webbrowser

from .models import Shortcut, ShortcutType


def open_shortcut(shortcut: Shortcut) -> None:
    if shortcut.type == ShortcutType.url:
        url = shortcut.url
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        webbrowser.open(url)
    else:
        raise NotImplementedError(f"Opening type '{shortcut.type}' is not yet supported")
