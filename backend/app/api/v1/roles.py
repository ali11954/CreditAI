from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import RoleCreate, RoleUpdate, RoleResponse
from app.schemas.common import PaginatedResponse
from app.dependencies import get_current_active_user, require_permission

router = APIRouter()


class PermissionsUpdate(BaseModel):
    permissions: List[str]


@router.get("/all-permissions")
async def list_all_permissions(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:read"))
):
    user_service = UserService(db)
    permissions, total = await user_service.get_permissions(page=1, page_size=200)
    return {"items": permissions, "total": total}


@router.get("/active")
async def list_active_roles(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:read"))
):
    user_service = UserService(db)
    roles, total = await user_service.get_roles(page=1, page_size=100)
    active_roles = [r for r in roles if r.get("is_active")]
    return {"items": active_roles, "total": len(active_roles)}


@router.get("/", response_model=PaginatedResponse[RoleResponse])
async def list_roles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:read"))
):
    user_service = UserService(db)
    roles, total = await user_service.get_roles(
        page=page,
        page_size=page_size,
        search=search
    )
    return PaginatedResponse(
        items=roles,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:read"))
):
    user_service = UserService(db)
    role = await user_service.get_role(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:create"))
):
    user_service = UserService(db)
    role = await user_service.create_role(role_data)
    return role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: UUID,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:update"))
):
    user_service = UserService(db)
    role = await user_service.update_role(role_id, role_data)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.delete("/{role_id}")
async def delete_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:delete"))
):
    user_service = UserService(db)
    success = await user_service.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}


@router.put("/{role_id}/permissions", response_model=RoleResponse)
async def update_role_permissions(
    role_id: UUID,
    data: PermissionsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:update"))
):
    user_service = UserService(db)
    result = await user_service.update_role_permissions(role_id, data.permissions)
    if not result:
        raise HTTPException(status_code=404, detail="Role not found")
    return result


@router.post("/seed-permissions")
async def seed_permissions(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_permission("roles:create"))
):
    from app.models.user import Permission
    
    PERMISSION_MODULES = {
        'customers': {'ar': 'العملاء', 'permissions': ['read', 'create', 'update', 'delete', 'export']},
        'credit_applications': {'ar': 'طلبات الائتمان', 'permissions': ['read', 'create', 'update', 'delete', 'approve', 'export']},
        'credit_limits': {'ar': 'الحدود الائتمانية', 'permissions': ['read', 'create', 'update', 'delete', 'export']},
        'collections': {'ar': 'التحصيل', 'permissions': ['read', 'create', 'update', 'delete', 'assign', 'export']},
        'legal_cases': {'ar': 'القضايا القانونية', 'permissions': ['read', 'create', 'update', 'delete', 'assign', 'export']},
        'documents': {'ar': 'المستندات', 'permissions': ['read', 'create', 'update', 'delete', 'upload', 'ocr', 'export']},
        'reports': {'ar': 'التقارير', 'permissions': ['read', 'create', 'execute', 'export']},
        'settings': {'ar': 'الإعدادات', 'permissions': ['read', 'update']},
        'branches': {'ar': 'الفروع', 'permissions': ['read', 'create', 'update', 'delete']},
        'departments': {'ar': 'الأقسام', 'permissions': ['read', 'create', 'update', 'delete']},
        'teams': {'ar': 'الفرق', 'permissions': ['read', 'create', 'update', 'delete']},
        'users': {'ar': 'المستخدمين', 'permissions': ['read', 'create', 'update', 'delete']},
        'roles': {'ar': 'الأدوار', 'permissions': ['read', 'create', 'update', 'delete']},
        'audit': {'ar': 'سجل المراجعة', 'permissions': ['read', 'export']},
        'compliance': {'ar': 'الامتثال', 'permissions': ['read', 'create', 'update', 'export']},
        'exposure': {'ar': 'التعرض', 'permissions': ['read', 'export']},
        'notifications': {'ar': 'الإشعارات', 'permissions': ['read', 'create', 'update', 'delete']},
        'delegations': {'ar': 'التفويضات', 'permissions': ['read', 'create', 'update', 'delete']},
        'currencies': {'ar': 'العملات', 'permissions': ['read', 'create', 'update', 'delete']},
        'sales': {'ar': 'المبيعات', 'permissions': ['read', 'create', 'update', 'delete', 'import', 'export']},
    }
    
    created = 0
    for module, config in PERMISSION_MODULES.items():
        for action in config['permissions']:
            perm_name = f"{module}:{action}"
            existing = await db.execute(select(Permission).where(Permission.name == perm_name))
            if not existing.scalar_one_or_none():
                perm = Permission(
                    name=perm_name,
                    description=f"{config['ar']} - {action}",
                    module=module,
                    action=action
                )
                db.add(perm)
                created += 1
    
    await db.commit()
    return {"message": f"Seeded {created} new permissions", "total_created": created}
