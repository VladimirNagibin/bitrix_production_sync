from typing import Any

from pydantic import BaseModel


class BitrixWebhookAuth(BaseModel):  # type: ignore[misc]
    domain: str
    client_endpoint: str
    server_endpoint: str
    member_id: str
    application_token: str


class BitrixWebhookPayload(BaseModel):  # type: ignore[misc]
    event: str
    event_handler_id: str
    data: dict[str, Any]
    ts: str
    auth: BitrixWebhookAuth

    @property
    def entity_id(self) -> int | None:
        """Извлекает ID сделки из данных"""
        try:
            return int(self.data.get("FIELDS", {}).get("ID", 0))
        except (ValueError, TypeError):
            return None

    @property
    def entity_type_id(self) -> int | None:
        """Извлекает ID сделки из данных"""
        try:
            return int(self.data.get("FIELDS", {}).get("ENTITY_TYPE_ID", 0))
        except (ValueError, TypeError):
            return None
