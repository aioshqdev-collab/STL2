from enum import Enum
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.remote_ai import fetch_ai_job, submit_ai_reconstruction


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class ConversionSettings(BaseModel):
    depth_mm: float = Field(default=22, ge=1, le=80)
    base_mm: float = Field(default=2.5, ge=0.4, le=20)
    smoothing: int = Field(default=2, ge=0, le=12)
    contrast: float = Field(default=1.2, ge=0.2, le=4)
    threshold: float = Field(default=8, ge=0, le=90)
    invert: bool = False
    ai_mode: bool = False


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str
    remote_job: dict | None = None


class PrintabilityReport(BaseModel):
    non_manifold_edges: int = 0
    thin_wall_count: int = 0
    floating_shells: int = 0
    broken_normals: int = 0
    printable_score: int = 92


app = FastAPI(title="STLForge API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/convert", response_model=JobResponse)
async def convert_image(file: UploadFile = File(...), settings: ConversionSettings = ConversionSettings()) -> JobResponse:
    if file.content_type not in {"image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Only JPG and JPEG uploads are supported.")

    job_id = str(uuid4())
    if settings.ai_mode:
        try:
            remote_job = await submit_ai_reconstruction(file)
        except Exception as exc:
            raise HTTPException(status_code=502, detail=f"AI service is unavailable: {exc}") from exc
        return JobResponse(
            job_id=remote_job.get("job_id", job_id),
            status=JobStatus(remote_job.get("status", JobStatus.queued)),
            message=remote_job.get("message", "Queued for GPU AI reconstruction."),
            remote_job=remote_job,
        )
    else:
        message = "Queued for free height-map STL generation."

    # Production wiring:
    # 1. Store upload in S3 or Cloudflare R2.
    # 2. Write job metadata to PostgreSQL.
    # 3. Push job_id and settings into Redis.
    # 4. Worker generates STL and analysis report, then stores output URL.
    return JobResponse(job_id=job_id, status=JobStatus.queued, message=message)


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str) -> JobResponse:
    return JobResponse(job_id=job_id, status=JobStatus.processing, message="Worker integration placeholder.")


@app.get("/api/ai/jobs/{job_id}")
async def get_ai_job(job_id: str) -> dict:
    try:
        return await fetch_ai_job(job_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI service is unavailable: {exc}") from exc


@app.get("/api/jobs/{job_id}/analysis", response_model=PrintabilityReport)
def get_analysis(job_id: str) -> PrintabilityReport:
    return PrintabilityReport()
