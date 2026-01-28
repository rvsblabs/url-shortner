"""Pydantic models for shortcuts."""

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, HttpUrl


class ShortcutType(str, Enum):
    url = "url"
    file = "file"


class Shortcut(BaseModel):
    name: str
    url: str
    type: ShortcutType = ShortcutType.url
    tags: list[str] = []
    created_at: datetime = None  # type: ignore[assignment]

    def model_post_init(self, __context: object) -> None:
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
