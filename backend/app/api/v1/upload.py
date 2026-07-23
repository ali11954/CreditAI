import os
import uuid
from datetime import datetime

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse

from app.config import settings
from app.dependencies import require_permission

router = APIRouter()

UPLOADS_DIR = settings.UPLOAD_DIR


def _ensure_upload_dir(folder: str = "") -> str:
    base = os.path.join(UPLOADS_DIR, folder) if folder else UPLOADS_DIR
    os.makedirs(base, exist_ok=True)
    return base


def _safe_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    safe_name = "".join(c for c in name if c.isalnum() or c in "._- ").strip()
    if not safe_name:
        safe_name = "file"
    unique = uuid.uuid4().hex[:8]
    return f"{safe_name}_{unique}{ext}"


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Query(default="", description="Subfolder to organize uploads"),
    current_user=Depends(require_permission("upload:create")),
):
    if file.size and file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE} bytes",
        )

    upload_dir = _ensure_upload_dir(folder)
    safe_name = _safe_filename(file.filename or "upload")
    filepath = os.path.join(upload_dir, safe_name)

    async with aiofiles.open(filepath, "wb") as f:
        while chunk := await file.read(8192):
            await f.write(chunk)

    stat = os.stat(filepath)

    return {
        "filename": safe_name,
        "original_filename": file.filename,
        "filepath": filepath,
        "folder": folder,
        "size": stat.st_size,
        "content_type": file.content_type,
        "uploaded_by": str(current_user.id),
        "uploaded_at": datetime.utcnow().isoformat(),
    }


@router.post("/multiple", status_code=status.HTTP_201_CREATED)
async def upload_multiple_files(
    files: list[UploadFile] = File(...),
    folder: str = Query(default="", description="Subfolder to organize uploads"),
    current_user=Depends(require_permission("upload:create")),
):
    results = []
    errors = []

    for file in files:
        try:
            if file.size and file.size > settings.MAX_UPLOAD_SIZE:
                errors.append({
                    "filename": file.filename,
                    "error": f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE} bytes",
                })
                continue

            upload_dir = _ensure_upload_dir(folder)
            safe_name = _safe_filename(file.filename or "upload")
            filepath = os.path.join(upload_dir, safe_name)

            async with aiofiles.open(filepath, "wb") as f:
                while chunk := await file.read(8192):
                    await f.write(chunk)

            stat = os.stat(filepath)

            results.append({
                "filename": safe_name,
                "original_filename": file.filename,
                "filepath": filepath,
                "folder": folder,
                "size": stat.st_size,
                "content_type": file.content_type,
            })
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})

    return {
        "uploaded": results,
        "errors": errors,
        "total_uploaded": len(results),
        "total_errors": len(errors),
    }


@router.get("/{filename:path}")
async def get_uploaded_file(
    filename: str,
    folder: str = Query(default="", description="Subfolder containing the file"),
    current_user=Depends(require_permission("upload:read")),
):
    upload_dir = _ensure_upload_dir(folder)
    filepath = os.path.join(upload_dir, filename)

    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found")

    stat = os.stat(filepath)
    ext = os.path.splitext(filename)[1].lower()

    media_types = {
        ".pdf": "application/pdf",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".csv": "text/csv",
        ".txt": "text/plain",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
    }

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type=media_types.get(ext, "application/octet-stream"),
    )
