"""
GPU worker placeholder for expensive image-to-3D reconstruction.

Recommended low-budget path:
- Keep the browser height-map converter free and instant.
- Send only high-complexity jobs to this worker.
- Start with RunPod, Vast.ai, or Lambda Labs spot GPU machines.
- Cache generated meshes by image hash and settings hash.

Model adapters to add here:
- Stable Fast 3D for fast single-image mesh generation.
- TripoSR for broad object reconstruction.
- InstantMesh or OpenLRM for stronger geometry when latency is acceptable.
"""


def run_ai_reconstruction(job_id: str) -> None:
    raise NotImplementedError("Connect PyTorch/CUDA model inference here.")
