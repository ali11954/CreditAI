from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import JWTError, jwt
import pyotp

from app.config import settings
from app.models.user import User, LoginHistory, ActiveSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where((User.username == username) | (User.email == username))
        )
        user = result.scalar_one_or_none()
        
        if not user or not self.verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        if user.locked_until and user.locked_until > datetime.utcnow():
            return None
        
        user.last_login = datetime.utcnow()
        user.failed_login_attempts = 0
        await self.db.commit()
        
        return user
    
    def create_access_token(self, user_id: UUID) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    def create_refresh_token(self, user_id: UUID) -> str:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "type": "refresh"
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    async def verify_refresh_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if payload.get("type") != "refresh":
                return None
            user_id = UUID(payload.get("sub"))
            result = await self.db.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except JWTError:
            return None
    
    async def register_user(self, data) -> Optional[User]:
        result = await self.db.execute(
            select(User).where((User.email == data.email) | (User.username == data.username))
        )
        if result.scalar_one_or_none():
            return None
        
        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            full_name_ar=data.full_name_ar,
            phone=data.phone,
            password_hash=self.get_password_hash(data.password)
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update_mfa_secret(self, user_id: UUID, secret: str) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one()
        user.mfa_secret = secret
        await self.db.commit()
        return user
    
    async def enable_mfa(self, user_id: UUID, secret: str):
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one()
        user.mfa_enabled = True
        user.mfa_secret = secret
        await self.db.commit()
    
    async def change_password(self, user_id: UUID, current_password: str, new_password: str) -> bool:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user or not self.verify_password(current_password, user.password_hash):
            return False
        
        user.password_hash = self.get_password_hash(new_password)
        await self.db.commit()
        return True
    
    async def send_password_reset_email(self, email: str):
        pass
    
    async def reset_password(self, token: str, new_password: str) -> bool:
        return False
    
    async def logout_user(self, user_id: UUID):
        result = await self.db.execute(
            select(ActiveSession).where(ActiveSession.user_id == user_id)
        )
        sessions = result.scalars().all()
        for session in sessions:
            await self.db.delete(session)
        await self.db.commit()
