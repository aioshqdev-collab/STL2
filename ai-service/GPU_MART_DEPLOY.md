# GPU Mart Deployment Notes

Do not commit passwords or rented-machine credentials to the repo.

## Recommended Architecture

Use the GPU machine as an HTTP AI worker:

```text
Frontend -> local/backend API -> GPU AI service -> returns GLB/STL URLs
```

This is better than SSH per upload because:

- The model stays loaded in GPU memory.
- Jobs can be queued and retried.
- The frontend can poll status.
- You do not need to expose SSH credentials to the app.
- File transfer is normal HTTP instead of remote shell automation.

## Ports

If your rented machine exposes a custom port, map the AI API to that port or reverse-proxy to it.

Example public API:

```text
http://YOUR_GPU_HOST:YOUR_PORT
```

Then set this on your main backend:

```powershell
$env:AI_SERVICE_URL="http://YOUR_GPU_HOST:YOUR_PORT"
```

## Windows GPU Machine Setup

If the rented instance is Windows, connect using RDP unless OpenSSH is explicitly enabled.

On the GPU machine:

```powershell
cd C:\
git clone YOUR_REPO_URL STL2
cd C:\STL2\ai-service
py -3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8100
```

For the real model environment, use Python 3.11 or 3.12, then install GPU packages from `requirements-gpu.txt`.

## Linux GPU Machine Setup

```bash
git clone YOUR_REPO_URL STL2
cd STL2/ai-service
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8100
```

## Starting/Stopping The Instance

If GPU Mart provides an API for starting and stopping rented machines, put that in the backend as a provider adapter. If it does not, the machine must already be running before jobs can be processed.

Do not make the public website perform SSH logins. Keep SSH/RDP for deployment and maintenance only.

## Security Checklist

- Change the machine password after sharing it anywhere.
- Prefer SSH keys over passwords.
- Restrict inbound ports to the API port and admin port.
- Add an API token before public launch.
- Store uploads and outputs in S3/R2 instead of leaving them on the GPU disk.
- Delete temporary job folders after download expiry.
