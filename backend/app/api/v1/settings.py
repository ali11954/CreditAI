from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models.settings import SystemSetting, ModuleConfig, MenuConfig
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission


class SystemSettingCreate(BaseModel):
    key: str
    value: Optional[str] = None
    value_type: str = "string"
    description: Optional[str] = None
    module: Optional[str] = None


class SystemSettingUpdate(BaseModel):
    value: Optional[str] = None
    value_type: Optional[str] = None
    description: Optional[str] = None
    module: Optional[str] = None
    is_active: Optional[bool] = None


class SystemSettingResponse(BaseModel):
    id: UUID
    key: str
    value: Optional[str] = None
    value_type: str
    description: Optional[str] = None
    module: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ModuleConfigUpdate(BaseModel):
    is_enabled: Optional[bool] = None
    settings: Optional[dict] = None


class ModuleConfigResponse(BaseModel):
    id: UUID
    module_name: str
    is_enabled: bool
    settings: dict = {}
    company_id: Optional[UUID] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MenuConfigCreate(BaseModel):
    name: str
    name_ar: Optional[str] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    parent_id: Optional[UUID] = None
    sort_order: str = "0"
    is_visible: bool = True
    permission_required: Optional[str] = None
    module: Optional[str] = None


class MenuConfigUpdate(BaseModel):
    name: Optional[str] = None
    name_ar: Optional[str] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    parent_id: Optional[UUID] = None
    sort_order: Optional[str] = None
    is_visible: Optional[bool] = None
    permission_required: Optional[str] = None
    module: Optional[str] = None
    is_active: Optional[bool] = None


class MenuConfigResponse(BaseModel):
    id: UUID
    name: str
    name_ar: Optional[str] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    parent_id: Optional[UUID] = None
    sort_order: str
    is_visible: bool
    permission_required: Optional[str] = None
    module: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/system", response_model=List[SystemSettingResponse])
async def list_system_settings(
    module: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:read"))
):
    query = select(SystemSetting)
    if module:
        query = query.where(SystemSetting.module == module)
    query = query.where(SystemSetting.is_active == True)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/system/{key}", response_model=SystemSettingResponse)
async def get_system_setting(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:read"))
):
    result = await db.execute(select(SystemSetting).where(SystemSetting.key == key))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="System setting not found")
    return item


@router.post("/system", response_model=SystemSettingResponse, status_code=status.HTTP_201_CREATED)
async def create_system_setting(
    setting_data: SystemSettingCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:create"))
):
    result = await db.execute(select(SystemSetting).where(SystemSetting.key == setting_data.key))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Setting with this key already exists")

    item = SystemSetting(
        key=setting_data.key,
        value=setting_data.value,
        value_type=setting_data.value_type,
        description=setting_data.description,
        module=setting_data.module
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/system/{key}", response_model=SystemSettingResponse)
async def update_system_setting(
    key: str,
    setting_data: SystemSettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:update"))
):
    result = await db.execute(select(SystemSetting).where(SystemSetting.key == key))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="System setting not found")

    update_data = setting_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/system/{key}")
async def delete_system_setting(
    key: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:delete"))
):
    result = await db.execute(select(SystemSetting).where(SystemSetting.key == key))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="System setting not found")

    item.is_active = False
    await db.flush()
    return {"message": "System setting deleted successfully"}


@router.get("/modules", response_model=List[ModuleConfigResponse])
async def list_module_configs(
    company_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:read"))
):
    query = select(ModuleConfig)
    if company_id:
        query = query.where(ModuleConfig.company_id == company_id)
    query = query.where(ModuleConfig.is_active == True)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/modules/{module_name}", response_model=ModuleConfigResponse)
async def get_module_config(
    module_name: str,
    company_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:read"))
):
    query = select(ModuleConfig).where(ModuleConfig.module_name == module_name)
    if company_id:
        query = query.where(ModuleConfig.company_id == company_id)

    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Module config not found")
    return item


@router.put("/modules/{module_name}", response_model=ModuleConfigResponse)
async def update_module_config(
    module_name: str,
    config_data: ModuleConfigUpdate,
    company_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:update"))
):
    query = select(ModuleConfig).where(ModuleConfig.module_name == module_name)
    if company_id:
        query = query.where(ModuleConfig.company_id == company_id)

    result = await db.execute(query)
    item = result.scalar_one_or_none()

    if not item:
        item = ModuleConfig(
            module_name=module_name,
            company_id=company_id,
            is_enabled=config_data.is_enabled if config_data.is_enabled is not None else True,
            settings=config_data.settings or {}
        )
        db.add(item)
    else:
        update_data = config_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.get("/menus", response_model=List[MenuConfigResponse])
async def list_menus(
    parent_id: Optional[UUID] = None,
    module: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:read"))
):
    query = select(MenuConfig).where(MenuConfig.is_active == True)
    if parent_id:
        query = query.where(MenuConfig.parent_id == parent_id)
    else:
        query = query.where(MenuConfig.parent_id == None)
    if module:
        query = query.where(MenuConfig.module == module)

    query = query.order_by(MenuConfig.sort_order)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/menus/{menu_id}", response_model=MenuConfigResponse)
async def get_menu(
    menu_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:read"))
):
    result = await db.execute(select(MenuConfig).where(MenuConfig.id == menu_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu not found")
    return item


@router.post("/menus", response_model=MenuConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: MenuConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:create"))
):
    item = MenuConfig(
        name=menu_data.name,
        name_ar=menu_data.name_ar,
        icon=menu_data.icon,
        url=menu_data.url,
        parent_id=menu_data.parent_id,
        sort_order=menu_data.sort_order,
        is_visible=menu_data.is_visible,
        permission_required=menu_data.permission_required,
        module=menu_data.module
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@router.put("/menus/{menu_id}", response_model=MenuConfigResponse)
async def update_menu(
    menu_id: UUID,
    menu_data: MenuConfigUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:update"))
):
    result = await db.execute(select(MenuConfig).where(MenuConfig.id == menu_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu not found")

    update_data = menu_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    await db.flush()
    await db.refresh(item)
    return item


@router.delete("/menus/{menu_id}")
async def delete_menu(
    menu_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("settings:delete"))
):
    result = await db.execute(select(MenuConfig).where(MenuConfig.id == menu_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu not found")

    item.is_active = False
    await db.flush()
    return {"message": "Menu deleted successfully"}
