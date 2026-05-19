from pathlib import Path
from shutil import copyfileobj
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.job_store import store
from app.schemas import JobResult, JobStatus, Quality, ReconstructionOptions
from app.settings import settings
from app.worker import run_reconstruction_job


app = FastAPI(title=settings.service_name, version="0.1.0")

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
    return {"status": "ok", "model_provider": settings.model_provider}


@app.post("/v1/reconstruct", response_model=JobResult)
async def reconstruct(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    quality: Quality = Form(Quality.high),
    target_format: str = Form("all"),
    make_printable: bool = Form(True),
    identify_object: bool = Form(True),
    remove_background: bool = Form(True),
    preserve_texture: bool = Form(True),
    wall_thickness_mm: float = Form(1.2),
) -> JobResult:
    if file.content_type not in {"image/jpeg", "image/jpg", "image/png"}:
        raise HTTPException(status_code=400, detail="Upload a JPG, JPEG, or PNG image.")

    options = ReconstructionOptions(
        quality=quality,
        target_format=target_format,
        make_printable=make_printable,
        identify_object=identify_object,
        remove_background=remove_background,
        preserve_texture=preserve_texture,
        wall_thickness_mm=wall_thickness_mm,
    )

    job_id = str(uuid4())
    job_dir = settings.work_dir / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename or "upload.jpg").suffix or ".jpg"
    image_path = job_dir / f"input{suffix}"
    with image_path.open("wb") as output:
        copyfileobj(file.file, output)

    job = store.create(
        JobResult(
            job_id=job_id,
            status=JobStatus.queued,
            message="Queued for AI reconstruction.",
        )
    )
    background_tasks.add_task(run_reconstruction_job, job_id, image_path, options)
    return job


@app.get("/v1/jobs/{job_id}", response_model=JobResult)
def get_job(job_id: str) -> JobResult:
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job


@app.get("/v1/files/{job_id}/{filename}")
def get_file(job_id: str, filename: str) -> FileResponse:
    allowed = {"model.glb", "model.obj", "model.stl", "texture.png"}
    if filename not in allowed:
        raise HTTPException(status_code=400, detail="File is not available.")
    path = settings.work_dir / job_id / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path)
