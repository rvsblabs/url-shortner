"""Click-based CLI for ush."""

import click

from .models import Shortcut
from .opener import open_shortcut
from .store import ShortcutStore

store = ShortcutStore()


class ShortcutGroup(click.Group):
    """Custom group that treats unknown commands as shortcut names to open."""

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        # Try built-in commands first
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return rv
        # Treat as a shortcut name
        @click.command(name=cmd_name, hidden=True)
        @click.pass_context
        def open_cmd(ctx: click.Context) -> None:
            shortcut = store.get(cmd_name)
            if shortcut is None:
                click.echo(f"Shortcut '{cmd_name}' not found.", err=True)
                raise SystemExit(1)
            open_shortcut(shortcut)
            click.echo(f"Opening {shortcut.url}")

        return open_cmd


@click.group(cls=ShortcutGroup)
def cli() -> None:
    """USH - URL Shortcut Handler."""


@cli.command()
@click.argument("name")
@click.argument("url")
def add(name: str, url: str) -> None:
    """Add a new shortcut."""
    try:
        store.add(Shortcut(name=name, url=url))
        click.echo(f"Added '{name}' -> {url}")
    except ValueError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)


@cli.command()
@click.argument("name")
def remove(name: str) -> None:
    """Remove a shortcut."""
    try:
        store.remove(name)
        click.echo(f"Removed '{name}'")
    except KeyError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)


@cli.command()
@click.argument("name")
@click.argument("url")
def update(name: str, url: str) -> None:
    """Update a shortcut's URL."""
    try:
        store.update(name, url)
        click.echo(f"Updated '{name}' -> {url}")
    except KeyError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)


@cli.command("list")
def list_shortcuts() -> None:
    """List all shortcuts."""
    shortcuts = store.list()
    if not shortcuts:
        click.echo("No shortcuts yet.")
        return
    for s in shortcuts:
        click.echo(f"  {s.name}  ->  {s.url}")
