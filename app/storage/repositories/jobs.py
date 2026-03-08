from typing import Any

from app.storage.db import get_jobs_collection


class JobRepository:
    def __init__(self) -> None:
        self.collection = get_jobs_collection()

    def create_job(self, job_record: dict[str, Any]) -> None:
        self.collection.insert_one(job_record)

    def get_job_by_id(self, job_id: str) -> dict[str, Any] | None:
        return self.collection.find_one({"job_id": job_id}, {"_id": 0})
