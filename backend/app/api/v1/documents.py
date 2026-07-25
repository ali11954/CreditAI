from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.document_service import DocumentService
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[DocumentResponse])
async def list_documents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    folder_id: Optional[UUID] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("documents:read"))
):
    document_service = DocumentService(db)
    documents, total = await document_service.get_documents(
        page=page,
        page_size=page_size,
        folder_id=folder_id,
        search=search
    )
    return PaginatedResponse(
        items=documents,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("documents:read"))
):
    document_service = DocumentService(db)
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document_data: DocumentCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("documents:create"))
):
    document_service = DocumentService(db)
    document = await document_service.create_document(document_data, current_user.id)
    return document


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: UUID,
    document_data: DocumentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("documents:update"))
):
    document_service = DocumentService(db)
    document = await document_service.update_document(document_id, document_data)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("documents:delete"))
):
    document_service = DocumentService(db)
    success = await document_service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}


@router.get("/folders/")
async def list_folders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    parent_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("documents:read"))
):
    from app.models.document import DocumentFolder
    from sqlalchemy import select, func
    query = select(DocumentFolder).where(DocumentFolder.is_active == True)
    count_query = select(func.count(DocumentFolder.id)).where(DocumentFolder.is_active == True)
    if parent_id:
        query = query.where(DocumentFolder.parent_id == parent_id)
        count_query = count_query.where(DocumentFolder.parent_id == parent_id)
    else:
        query = query.where(DocumentFolder.parent_id == None)
        count_query = count_query.where(DocumentFolder.parent_id == None)
    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(DocumentFolder.name).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    folders = [dict(row._mapping) for row in result.all()]
    return {"items": folders, "total": total, "page": page, "page_size": page_size}


@router.post("/folders/", status_code=status.HTTP_201_CREATED)
async def create_folder(
    folder_data: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("documents:create"))
):
    from app.models.document import DocumentFolder
    folder = DocumentFolder(**folder_data, created_by=current_user.id)
    db.add(folder)
    await db.commit()
    await db.refresh(folder)
    return dict(folder._mapping)
