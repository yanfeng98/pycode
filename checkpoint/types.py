from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MAX_SNAPSHOTS = 100


@dataclass
class FileBackup:
    backup_filename: str | None
    version: int
    backup_time: str

    def to_dict(self) -> dict:
        return {
            "backup_filename": self.backup_filename,
            "version": self.version,
            "backup_time": self.backup_time,
        }

    @classmethod
    def from_dict(cls, data: dict) -> FileBackup:
        return cls(
            backup_filename=data.get("backup_filename"),
            version=data.get("version", 0),
            backup_time=data.get("backup_time", ""),
        )


@dataclass
class Snapshot:
    id: int
    session_id: str
    created_at: str
    turn_count: int
    message_index: int
    user_prompt_preview: str
    token_snapshot: dict[str, int]
    file_backups: dict[str, FileBackup] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "created_at": self.created_at,
            "turn_count": self.turn_count,
            "message_index": self.message_index,
            "user_prompt_preview": self.user_prompt_preview,
            "token_snapshot": self.token_snapshot,
            "file_backups": {
                path: fb.to_dict() for path, fb in self.file_backups.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> Snapshot:
        backups = {}
        for path, fb_data in data.get("file_backups", {}).items():
            backups[path] = FileBackup.from_dict(fb_data)
        return cls(
            id=data["id"],
            session_id=data.get("session_id", ""),
            created_at=data.get("created_at", ""),
            turn_count=data.get("turn_count", 0),
            message_index=data.get("message_index", 0),
            user_prompt_preview=data.get("user_prompt_preview", ""),
            token_snapshot=data.get("token_snapshot", {}),
            file_backups=backups,
        )
