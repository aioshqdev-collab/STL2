# STLForge

STLForge is a free-first JPG/JPEG to STL web studio. The frontend already includes an in-browser height-map converter, 3D preview, model controls, STL download, and printability estimates. The backend is scaffolded for heavier AI reconstruction jobs when an upload is too complex for the free browser pipeline.

## Stack

- Frontend: Next.js, React Three Fiber, Tailwind CSS, Zustand
- Backend: FastAPI, Redis queue placeholder, PostgreSQL/S3 integration points
- AI workers: PyTorch/CUDA placeholders for Stable Fast 3D, TripoSR, OpenLRM, or InstantMesh
- Mesh checks: Blender/MeshLab/Netfabb-style worker placeholders

## Run Frontend

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000`.

## Backend Setup

Python is not installed on this machine yet. Once it is available:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Budget Strategy

Keep normal JPG to relief STL conversion free and local in the browser. Use the GPU AI pipeline only for complex object reconstruction, high-poly jobs, or uploads that need depth/shape hallucination beyond a height map. This keeps hosting costs low while preserving a professional upgrade path.
