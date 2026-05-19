from threading import Lock

from app.schemas import JobResult, JobStatus


class JobStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._jobs: dict[str, JobResult] = {}

    def create(self, job: JobResult) -> JobResult:
        with self._lock:
            self._jobs[job.job_id] = job
        return job

    def update(self, job_id: str, **changes: object) -> JobResult:
        with self._lock:
            current = self._jobs[job_id]
            updated = current.model_copy(update=changes)
            self._jobs[job_id] = updated
        return updated

    def get(self, job_id: str) -> JobResult | None:
        with self._lock:
            return self._jobs.get(job_id)

    def fail(self, job_id: str, message: str) -> JobResult:
        return self.update(job_id, status=JobStatus.failed, message=message)


store = JobStore()
