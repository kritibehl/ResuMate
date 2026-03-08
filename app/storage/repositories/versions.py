from app.schemas.domain import VersionRecord


class VersionRepository:
    def __init__(self) -> None:
        self._versions: dict[str, dict] = {}

    def create_version(self, version: VersionRecord) -> None:
        self._versions[version.version_id] = version.model_dump(mode="json")

    def list_versions(self) -> list[dict]:
        return list(self._versions.values())
