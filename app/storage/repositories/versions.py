from typing import Any

_VERSIONS: list[dict[str, Any]] = []


class VersionRepository:
    def create_version(self, version_record: dict[str, Any]) -> None:
        _VERSIONS.append(version_record)

    def list_versions(self) -> list[dict[str, Any]]:
        return list(reversed(_VERSIONS))
