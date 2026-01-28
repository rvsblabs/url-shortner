"""JSON-based shortcut storage at ~/.ush/shortcuts.json."""

import json
from pathlib import Path

from .models import Shortcut

DEFAULT_PATH = Path.home() / ".ush" / "shortcuts.json"


class ShortcutStore:
    def __init__(self, path: Path = DEFAULT_PATH):
        self.path = path

    def _load(self) -> dict[str, Shortcut]:
        if not self.path.exists():
            return {}
        data = json.loads(self.path.read_text())
        return {name: Shortcut.model_validate(s) for name, s in data.items()}

    def _save(self, shortcuts: dict[str, Shortcut]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {name: s.model_dump(mode="json") for name, s in shortcuts.items()}
        self.path.write_text(json.dumps(data, indent=2) + "\n")

    def list(self) -> list[Shortcut]:
        return list(self._load().values())

    def get(self, name: str) -> Shortcut | None:
        return self._load().get(name)

    def add(self, shortcut: Shortcut) -> None:
        shortcuts = self._load()
        if shortcut.name in shortcuts:
            raise ValueError(f"Shortcut '{shortcut.name}' already exists")
        shortcuts[shortcut.name] = shortcut
        self._save(shortcuts)

    def remove(self, name: str) -> None:
        shortcuts = self._load()
        if name not in shortcuts:
            raise KeyError(f"Shortcut '{name}' not found")
        del shortcuts[name]
        self._save(shortcuts)

    def update(self, name: str, url: str) -> None:
        shortcuts = self._load()
        if name not in shortcuts:
            raise KeyError(f"Shortcut '{name}' not found")
        shortcuts[name].url = url
        self._save(shortcuts)
