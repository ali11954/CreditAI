from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.document import Document, DocumentFolder
from app.schemas.document import DocumentCreate, DocumentUpdate


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_documents(
        self,
        page: int = 1,
        page_size: int = 20,
        folder_id: Optional[UUID] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Document], int]:
        query = select(Document)
        
        if folder_id:
            query = query.where(Document.folder_id == folder_id)
        
        if search:
            query = query.where(Document.name.ilike(f"%{search}%"))
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        documents = result.scalars().all()
        
        return documents, total
    
    async def get_document(self, document_id: UUID) -> Optional[Document]:
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()
    
    async def create_document(
        self,
        data: DocumentCreate,
        user_id: UUID
    ) -> Document:
        document = Document(
            folder_id=data.folder_id,
            name=data.name,
            file_path=data.file_path,
            file_type=data.file_type,
            file_size=data.file_size,
            mime_type=data.mime_type,
            version=data.version,
            description=data.description,
            tags=data.tags,
            extra_data=data.extra_data,
            uploaded_by=user_id
        )
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document
    
    async def update_document(
        self,
        document_id: UUID,
        data: DocumentUpdate
    ) -> Optional[Document]:
        document = await self.get_document(document_id)
        if not document:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(document, key, value)
        
        await self.db.commit()
        await self.db.refresh(document)
        return document
    
    async def delete_document(self, document_id: UUID) -> bool:
        document = await self.get_document(document_id)
        if not document:
            return False
        
        document.is_active = False
        await self.db.commit()
        return True
    
    async def get_folders(
        self,
        page: int = 1,
        page_size: int = 20,
        parent_id: Optional[UUID] = None
    ) -> Tuple[List[DocumentFolder], int]:
        query = select(DocumentFolder)
        
        if parent_id:
            query = query.where(DocumentFolder.parent_id == parent_id)
        else:
            query = query.where(DocumentFolder.parent_id.is_(None))
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        folders = result.scalars().all()
        
        return folders, total
    
    async def create_folder(
        self,
        folder_data: dict,
        user_id: UUID
    ) -> DocumentFolder:
        folder = DocumentFolder(
            created_by=user_id,
            **folder_data
        )
        self.db.add(folder)
        await self.db.commit()
        await self.db.refresh(folder)
        return folder
