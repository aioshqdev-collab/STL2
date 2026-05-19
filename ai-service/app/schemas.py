from enum import Enum

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    ready = "ready"
    failed = "failed"


class Quality(str, Enum):
    draft = "draft"
    balanced = "balanced"
    high = "high"
    ultra = "ultra"


class ReconstructionOptions(BaseModel):
    quality: Quality = Quality.high
    target_format: str = Field(default="glb", pattern="^(glb|obj|stl|all)$")
    make_printable: bool = True
    identify_object: bool = True
    remove_background: bool = True
    preserve_texture: bool = True
    wall_thickness_mm: float = Field(default=1.2, ge=0.4, le=8)


class AnalysisReport(BaseModel):
    printable_score: int = 0
    non_manifold_edges: int = 0
    thin_wall_count: int = 0
    floating_shells: int = 0
    broken_normals: int = 0
    notes: list[str] = []


class JobResult(BaseModel):
    job_id: str
    status: JobStatus
    object_label: str | None = None
    confidence: float | None = None
    model_glb_url: str | None = None
    model_obj_url: str | None = None
    texture_url: str | None = None
    model_stl_url: str | None = None
    analysis: AnalysisReport | None = None
    message: str = ""
