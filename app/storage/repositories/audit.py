from typing import Any

_AUDIT_EVENTS: list[dict[str, Any]] = []


class AuditRepository:
    def create_event(self, event: dict[str, Any]) -> None:
        _AUDIT_EVENTS.append(event)

    def list_events(self) -> list[dict[str, Any]]:
        return list(reversed(_AUDIT_EVENTS))
