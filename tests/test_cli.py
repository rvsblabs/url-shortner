"""Tests for ush CLI."""

from pathlib import Path

from click.testing import CliRunner

from ush.cli import cli
from ush.store import ShortcutStore


def _make_store(tmp_path: Path) -> ShortcutStore:
    """Create a store using a temp path."""
    return ShortcutStore(path=tmp_path / "shortcuts.json")


def _patched_cli(runner: CliRunner, tmp_path: Path, args: list[str]):
    """Run CLI with a temp store."""
    import ush.cli as cli_mod

    original = cli_mod.store
    cli_mod.store = _make_store(tmp_path)
    try:
        return runner.invoke(cli, args)
    finally:
        cli_mod.store = original


def test_list_empty(tmp_path):
    runner = CliRunner()
    result = _patched_cli(runner, tmp_path, ["list"])
    assert result.exit_code == 0
    assert "No shortcuts yet." in result.output


def test_add_and_list(tmp_path):
    runner = CliRunner()
    result = _patched_cli(runner, tmp_path, ["add", "test/", "https://example.com"])
    assert result.exit_code == 0
    assert "Added" in result.output

    result = _patched_cli(runner, tmp_path, ["list"])
    assert result.exit_code == 0
    assert "test/" in result.output
    assert "https://example.com" in result.output


def test_add_duplicate(tmp_path):
    runner = CliRunner()
    _patched_cli(runner, tmp_path, ["add", "dup/", "https://example.com"])
    result = _patched_cli(runner, tmp_path, ["add", "dup/", "https://other.com"])
    assert result.exit_code != 0
    assert "already exists" in result.output


def test_remove(tmp_path):
    runner = CliRunner()
    _patched_cli(runner, tmp_path, ["add", "rm/", "https://example.com"])
    result = _patched_cli(runner, tmp_path, ["remove", "rm/"])
    assert result.exit_code == 0
    assert "Removed" in result.output

    result = _patched_cli(runner, tmp_path, ["list"])
    assert "No shortcuts yet." in result.output


def test_remove_nonexistent(tmp_path):
    runner = CliRunner()
    result = _patched_cli(runner, tmp_path, ["remove", "nope/"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_update(tmp_path):
    runner = CliRunner()
    _patched_cli(runner, tmp_path, ["add", "u/", "https://old.com"])
    result = _patched_cli(runner, tmp_path, ["update", "u/", "https://new.com"])
    assert result.exit_code == 0
    assert "Updated" in result.output

    result = _patched_cli(runner, tmp_path, ["list"])
    assert "https://new.com" in result.output


def test_open_nonexistent(tmp_path):
    runner = CliRunner()
    result = _patched_cli(runner, tmp_path, ["nope/"])
    assert result.exit_code != 0
    assert "not found" in result.output
