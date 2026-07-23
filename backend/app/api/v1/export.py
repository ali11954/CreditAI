from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Union
import os
import tempfile

from app.dependencies import require_permission
from app.services.export_service import export_to_excel, export_to_pdf, export_to_csv

router = APIRouter()


def normalize_columns(columns):
    if not columns:
        return None
    result = []
    for col in columns:
        if isinstance(col, str):
            result.append({"key": col, "label": col})
        elif isinstance(col, dict):
            key = col.get("key", "")
            result.append({"key": key, "label": col.get("label", key)})
        else:
            result.append({"key": str(col), "label": str(col)})
    return result


class ExcelExportRequest(BaseModel):
    data: list[dict]
    filename: str = "export.xlsx"
    sheet_name: str = "Sheet1"
    columns: Optional[list] = None


class PdfExportRequest(BaseModel):
    data: list[dict]
    filename: str = "export.pdf"
    title: str = "Export Report"
    columns: Optional[list] = None
    orientation: str = Field(default="landscape", pattern="^(landscape|portrait)$")


class CsvExportRequest(BaseModel):
    data: list[dict]
    filename: str = "export.csv"
    columns: Optional[list] = None


@router.post("/excel")
async def export_excel(
    request: ExcelExportRequest,
    current_user=Depends(require_permission("export:excel")),
):
    try:
        temp_dir = tempfile.mkdtemp()
        filename = request.filename if request.filename.endswith(".xlsx") else f"{request.filename}.xlsx"
        filepath = os.path.join(temp_dir, filename)

        columns = normalize_columns(request.columns)

        await export_to_excel(
            data=request.data,
            filename=filepath,
            sheet_name=request.sheet_name,
            columns=columns,
        )

        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export Excel: {str(e)}",
        )


@router.post("/pdf")
async def export_pdf(
    request: PdfExportRequest,
    current_user=Depends(require_permission("export:pdf")),
):
    try:
        temp_dir = tempfile.mkdtemp()
        filename = request.filename if request.filename.endswith(".pdf") else f"{request.filename}.pdf"
        filepath = os.path.join(temp_dir, filename)

        columns = normalize_columns(request.columns)

        await export_to_pdf(
            data=request.data,
            filename=filepath,
            title=request.title,
            columns=columns,
            orientation=request.orientation,
        )

        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export PDF: {str(e)}",
        )


@router.post("/csv")
async def export_csv(
    request: CsvExportRequest,
    current_user=Depends(require_permission("export:csv")),
):
    try:
        temp_dir = tempfile.mkdtemp()
        filename = request.filename if request.filename.endswith(".csv") else f"{request.filename}.csv"
        filepath = os.path.join(temp_dir, filename)

        columns = normalize_columns(request.columns)

        await export_to_csv(
            data=request.data,
            filename=filepath,
            columns=columns,
        )

        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export CSV: {str(e)}",
        )
