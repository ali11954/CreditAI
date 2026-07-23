from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User, Role, Permission, UserRole, RolePermission
from app.schemas.user import UserCreate, UserUpdate, RoleCreate, RoleUpdate, PermissionCreate
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.auth_service = AuthService(db)
    
    async def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[dict], int]:
        query = select(User)
        
        if search:
            query = query.where(
                (User.full_name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%")) |
                (User.username.ilike(f"%{search}%"))
            )
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        enriched = []
        for user in users:
            role_result = await self.db.execute(
                select(Role.id, Role.name, Role.name_ar)
                .join(UserRole, UserRole.role_id == Role.id)
                .where(UserRole.user_id == user.id)
                .limit(1)
            )
            role_row = role_result.first()
            role_id = role_row[0] if role_row else None
            role_name = role_row[1] if role_row else "viewer"
            role_name_ar = role_row[2] if role_row else None
            user_dict = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "full_name_ar": user.full_name_ar,
                "phone": user.phone,
                "avatar": user.avatar,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "mfa_enabled": user.mfa_enabled,
                "role": role_name or "viewer",
                "role_id": str(role_id) if role_id else None,
                "last_login": user.last_login,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            enriched.append(user_dict)
        
        return enriched, total
    
    async def get_user(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def create_user(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            full_name_ar=data.full_name_ar,
            phone=data.phone,
            password_hash=self.auth_service.get_password_hash(data.password),
            is_active=data.is_active,
            is_superuser=data.is_superuser
        )
        self.db.add(user)
        await self.db.flush()
        
        if data.role_id:
            user_role = UserRole(user_id=user.id, role_id=data.role_id)
            self.db.add(user_role)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update_user(self, user_id: UUID, data: UserUpdate) -> Optional[User]:
        user = await self.get_user(user_id)
        if not user:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        role_id = update_data.pop("role_id", None)
        
        for key, value in update_data.items():
            setattr(user, key, value)
        
        if role_id is not None:
            await self.db.execute(
                select(UserRole).where(UserRole.user_id == user_id)
            )
            existing = await self.db.execute(
                select(UserRole).where(UserRole.user_id == user_id)
            )
            existing_role = existing.scalar_one_or_none()
            
            if existing_role:
                existing_role.role_id = role_id
            else:
                user_role = UserRole(user_id=user_id, role_id=role_id)
                self.db.add(user_role)
        
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def delete_user(self, user_id: UUID) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
        
        user.is_active = False
        await self.db.commit()
        return True
    
    async def get_roles(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None
    ) -> Tuple[List[dict], int]:
        query = select(Role)
        
        if search:
            query = query.where(
                (Role.name.ilike(f"%{search}%")) |
                (Role.name_ar.ilike(f"%{search}%"))
            )
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        roles = result.scalars().all()
        
        enriched = []
        for role in roles:
            users_count_result = await self.db.execute(
                select(func.count())
                .select_from(UserRole)
                .where(UserRole.role_id == role.id)
            )
            users_count = users_count_result.scalar() or 0
            
            enriched.append({
                "id": role.id,
                "name": role.name,
                "name_ar": role.name_ar,
                "description": role.description,
                "is_system": role.is_system,
                "is_active": role.is_active,
                "permissions": role.permissions or [],
                "users_count": users_count,
                "created_at": role.created_at,
                "updated_at": role.updated_at,
            })
        
        return enriched, total
    
    async def get_role(self, role_id: UUID) -> Optional[dict]:
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        role = result.scalar_one_or_none()
        if not role:
            return None
        
        users_count_result = await self.db.execute(
            select(func.count())
            .select_from(UserRole)
            .where(UserRole.role_id == role.id)
        )
        users_count = users_count_result.scalar() or 0
        
        return {
            "id": role.id,
            "name": role.name,
            "name_ar": role.name_ar,
            "description": role.description,
            "is_system": role.is_system,
            "is_active": role.is_active,
            "permissions": role.permissions or [],
            "users_count": users_count,
            "created_at": role.created_at,
            "updated_at": role.updated_at,
        }
    
    async def create_role(self, data: RoleCreate) -> Role:
        role = Role(
            name=data.name,
            name_ar=data.name_ar,
            description=data.description,
            is_system=data.is_system,
            permissions=data.permissions
        )
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role
    
    async def update_role(self, role_id: UUID, data: RoleUpdate) -> Optional[dict]:
        role_dict = await self.get_role(role_id)
        if not role_dict:
            return None
        
        from app.models.user import Role
        role = (await self.db.execute(select(Role).where(Role.id == role_id))).scalar_one_or_none()
        if not role:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(role, key, value)
        
        await self.db.commit()
        await self.db.refresh(role)
        
        return await self.get_role(role_id)
    
    async def update_role_permissions(self, role_id: UUID, permissions: List[str]) -> Optional[dict]:
        role = await self.get_role(role_id)
        if not role:
            return None
        
        role.permissions = permissions
        await self.db.commit()
        
        users_count_result = await self.db.execute(
            select(func.count())
            .select_from(UserRole)
            .where(UserRole.role_id == role.id)
        )
        users_count = users_count_result.scalar() or 0
        
        return {
            "id": role.id,
            "name": role.name,
            "name_ar": role.name_ar,
            "description": role.description,
            "is_system": role.is_system,
            "is_active": role.is_active,
            "permissions": role.permissions or [],
            "users_count": users_count,
            "created_at": role.created_at,
            "updated_at": role.updated_at,
        }
    
    async def delete_role(self, role_id: UUID) -> bool:
        role_dict = await self.get_role(role_id)
        if not role_dict or role_dict.get("is_system"):
            return False
        
        from app.models.user import Role
        role = (await self.db.execute(select(Role).where(Role.id == role_id))).scalar_one_or_none()
        if not role:
            return False
        
        role.is_active = False
        await self.db.commit()
        return True
    
    async def get_permissions(
        self,
        page: int = 1,
        page_size: int = 20,
        module: Optional[str] = None
    ) -> Tuple[List[Permission], int]:
        query = select(Permission)
        
        if module:
            query = query.where(Permission.module == module)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_query)).scalar()
        
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        permissions = result.scalars().all()
        
        return permissions, total
    
    async def get_permission(self, permission_id: UUID) -> Optional[Permission]:
        result = await self.db.execute(select(Permission).where(Permission.id == permission_id))
        return result.scalar_one_or_none()
    
    async def create_permission(self, data: PermissionCreate) -> Permission:
        permission = Permission(
            name=data.name,
            description=data.description,
            module=data.module,
            action=data.action
        )
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        return permission
    
    async def delete_permission(self, permission_id: UUID) -> bool:
        permission = await self.get_permission(permission_id)
        if not permission:
            return False
        
        permission.is_active = False
        await self.db.commit()
        return True
