import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from monday_sdk import MondayClient

from notifier.base import Notifier


class MondayNotifier(Notifier):
    def __init__(self, config: dict[str, Any]) -> None:
        self.monday = MondayClient(token=config["token"])
        self.message_format = "dict"
        try:
            self.board_id = config["board_id"]
            self.group_id = config["group_id"]
        except Exception:
            print(f"⚠️ Failed to parse board_id or group_id")


    def send(self, title: str, body: dict, attachments: Sequence[Path] | None = None) -> bool:
        str_attachments = [str(path) for path in attachments] if attachments else None

        if str_attachments:
            for service in self.apprise.servers:
                if not service.attachment_support:
                    print(f"⚠️ Warning: {service.url()} does not support attachments. They will be ignored.")

        release = body["release"]
        repo_id = body["repo_id"]
        title =  f"New Release for {repo_id}: {release.tag}"

        self.monday.items.create_item(
            board_id=self.board_id,
            group_id=self.group_id,
            item_name=title,
        )

        return bool(True)
