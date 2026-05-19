import os
from typing import Any

import httpx
from fastapi import UploadFile


AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:8100").rstrip("/")
AI_SERVICE_TIMEOUT_SECONDS = float(os.getenv("AI_SERVICE_TIMEOUT_SECONDS", "3600"))


async def submit_ai_reconstruction(file: UploadFile, quality: str = "high") -> dict[str, Any]:
    content = await file.read()
    await file.seek(0)

    files = {
        "file": (
            file.filename or "upload.jpg",
            content,
            file.content_type or "image/jpeg",
        )
    }
    data = {
        "quality": quality,
        "target_format": "all",
        "make_printable": "true",
        "identify_object": "true",
        "remove_background": "true",
        "preserve_texture": "true",
    }

    async with httpx.AsyncClient(timeout=AI_SERVICE_TIMEOUT_SECONDS) as client:
        response = await client.post(f"{AI_SERVICE_URL}/v1/reconstruct", files=files, data=data)
        response.raise_for_status()
        return response.json()


async def fetch_ai_job(job_id: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(f"{AI_SERVICE_URL}/v1/jobs/{job_id}")
        response.raise_for_status()
        return response.json()
