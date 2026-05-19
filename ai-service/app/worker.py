from pathlib import Path

from app.job_store import store
from app.pipeline.object_identity import identify_object
from app.pipeline.print_repair import repair_for_printing
from app.pipeline.reconstruction import reconstruct_mesh
from app.pipeline.segmentation import remove_background
from app.schemas import JobStatus, ReconstructionOptions
from app.settings import settings


def run_reconstruction_job(job_id: str, image_path: Path, options: ReconstructionOptions) -> None:
    try:
        store.update(job_id, status=JobStatus.processing, message="Identifying object and preparing image.")

        label, confidence = ("unknown object", 0.0)
        if options.identify_object:
            label, confidence = identify_object(image_path)

        job_dir = settings.work_dir / job_id
        segmented_path = image_path
        if options.remove_background:
            segmented_path = remove_background(image_path, job_dir)

        store.update(job_id, object_label=label, confidence=confidence, message="Running image-to-3D model.")
        mesh_paths = reconstruct_mesh(
            segmented_image=segmented_path,
            output_dir=job_dir,
            provider=settings.model_provider,
            quality=options.quality.value,
        )

        analysis = None
        if options.make_printable:
            store.update(job_id, message="Repairing mesh for 3D printing.")
            analysis = repair_for_printing(mesh_paths, options.wall_thickness_mm)

        base = f"{settings.public_base_url.rstrip('/')}/v1/files/{job_id}"
        store.update(
            job_id,
            status=JobStatus.ready,
            model_glb_url=f"{base}/model.glb",
            model_obj_url=f"{base}/model.obj",
            texture_url=f"{base}/texture.png",
            model_stl_url=f"{base}/model.stl",
            analysis=analysis,
            message="Reconstruction complete.",
        )
    except Exception as exc:
        store.fail(job_id, str(exc))
