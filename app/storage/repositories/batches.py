from typing import Any

_BATCHES: dict[str, dict[str, Any]] = {}


class BatchRepository:
    def create_batch(self, batch_record: dict[str, Any]) -> None:
        _BATCHES[batch_record["batch_id"]] = batch_record

    def get_batch_by_id(self, batch_id: str) -> dict[str, Any] | None:
        return _BATCHES.get(batch_id)

    def list_batches(self) -> list[dict[str, Any]]:
        return sorted(
            _BATCHES.values(),
            key=lambda item: item["created_at"],
            reverse=True,
        )
