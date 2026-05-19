# STLForge AI Service

This folder is the dedicated AI API for high-quality image-to-3D reconstruction.

The current frontend browser converter is only a preview/fallback. For the result you actually want, the production flow should be:

1. Receive JPG/JPEG upload.
2. Segment the main object from the background.
3. Identify the object category.
4. Run a single-image 3D reconstruction model.
5. Generate textured `GLB`/`OBJ`.
6. Repair and thicken the mesh for 3D printing.
7. Export printable `STL` plus textured preview files.

## Recommended Model Order

Start with this order:

1. **Stable Fast 3D**: best first production choice for textured mesh output and speed.
2. **TripoSR**: lightweight fallback and easier to run locally.
3. **InstantMesh**: better quality in some cases, heavier and slower.
4. **SAM 3D Objects**: strong long-term option for object-aware reconstruction when available in your deployment environment.

## Run API

```bash
cd ai-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8100
```

Open:

```text
http://127.0.0.1:8100/docs
```

## Production Hosting

Use a GPU host for this service:

- RunPod
- Vast.ai
- Lambda Labs

Recommended GPU:

- Minimum: RTX 3060 12GB
- Better: RTX 4090 24GB
- Cloud sweet spot: A10G / L40S

For real GPU model installs, use Python 3.11 or 3.12. Python 3.14 is fine for the lightweight mock API, but many AI libraries do not publish wheels for it yet and will try to compile from source.

## API Contract

`POST /v1/reconstruct`

Returns a job id immediately. The worker can take minutes if quality settings are high.

`GET /v1/jobs/{job_id}`

Returns job status and output file URLs when complete.

Outputs:

- `model_glb_url`: textured 3D preview
- `model_obj_url`: OBJ mesh
- `texture_url`: image texture
- `model_stl_url`: repaired printable STL
- `analysis`: printability information

## Important

STL cannot store texture. Use `GLB` for the textured preview and `STL` for printing.
