# USH - URL Shortcut Handler

A Python CLI tool for managing URL shortcuts in the terminal. Quickly save, list, and open frequently used URLs.

## Installation

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

```bash
# Add a shortcut
ush add italgo/ https://introtoalgo.com/abc

# List all shortcuts
ush list

# Open a shortcut in the browser
ush italgo/

# Update a shortcut's URL
ush update italgo/ https://new-url.com

# Remove a shortcut
ush remove italgo/
```

## Storage

Shortcuts are stored as JSON at `~/.ush/shortcuts.json`.

## Development

```bash
uv run pytest
```
