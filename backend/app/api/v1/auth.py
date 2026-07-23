from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
import pyotp

from app.database import get_db
from app.services.auth_service import AuthService
from app.models.user import User, Role, UserRole, Permission, RolePermission
from app.models.core import Currency
from app.models.report import ReportTemplate
from app.schemas.auth import (
    LoginRequest, TokenResponse, RefreshTokenRequest,
    RegisterRequest, MFASetup, MFAVerifyRequest,
    ChangePasswordRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.dependencies import get_current_user

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    login_identifier = request.email or request.username
    if not login_identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username required"
        )
    user = await auth_service.authenticate_user(login_identifier, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if user.mfa_enabled:
        if not request.mfa_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MFA code required"
            )
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(request.mfa_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA code"
            )
    
    access_token = auth_service.create_access_token(user.id)
    refresh_token = auth_service.create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=30 * 60
    )


@router.get("/me")
async def get_current_user_profile(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "full_name_ar": current_user.full_name_ar,
        "phone": current_user.phone,
        "avatar": current_user.avatar,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "mfa_enabled": current_user.mfa_enabled,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    }


@router.post("/logout")
async def logout(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    await auth_service.logout_user(current_user.id)
    return {"message": "Logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.verify_refresh_token(request.refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    access_token = auth_service.create_access_token(user.id)
    new_refresh_token = auth_service.create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=30 * 60
    )


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = await auth_service.register_user(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    access_token = auth_service.create_access_token(user.id)
    refresh_token = auth_service.create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=30 * 60
    )


@router.post("/mfa-setup", response_model=MFASetup)
async def mfa_setup(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    
    user = await auth_service.update_mfa_secret(current_user.id, secret)
    
    return MFASetup(
        secret=secret,
        qr_code_url=totp.provisioning_uri(
            name=current_user.email,
            issuer_name="CreditAI"
        ),
        backup_codes=[]
    )


@router.post("/mfa-verify")
async def mfa_verify(request: MFAVerifyRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    totp = pyotp.TOTP(request.secret)
    if totp.verify(request.code):
        auth_service = AuthService(db)
        await auth_service.enable_mfa(current_user.id, request.secret)
        return {"message": "MFA enabled successfully"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid MFA code"
    )


@router.post("/change-password")
async def change_password(request: ChangePasswordRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    success = await auth_service.change_password(
        current_user.id,
        request.current_password,
        request.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid current password"
        )
    return {"message": "Password changed successfully"}


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    await auth_service.send_password_reset_email(request.email)
    return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    success = await auth_service.reset_password(request.token, request.new_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    return {"message": "Password reset successfully"}


@router.post("/seed")
async def seed_database(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count(User.id)))
    user_count = result.scalar()
    
    if user_count and user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database already seeded"
        )
    
    auth_service = AuthService(db)
    
    roles_data = [
        {"name": "Super Admin", "name_ar": "مسؤول النظام", "description": "Full system access", "is_system": True, "permissions": ["*"]},
        {"name": "Admin", "name_ar": "مدير", "description": "Administrative access", "is_system": True, "permissions": [
            "customers:read", "customers:create", "customers:update", "customers:delete", "customers:export",
            "credit_applications:read", "credit_applications:create", "credit_applications:update", "credit_applications:delete", "credit_applications:approve", "credit_applications:export",
            "credit_limits:read", "credit_limits:create", "credit_limits:update", "credit_limits:delete", "credit_limits:export",
            "collections:read", "collections:create", "collections:update", "collections:delete", "collections:assign", "collections:export",
            "legal_cases:read", "legal_cases:create", "legal_cases:update", "legal_cases:delete", "legal_cases:assign", "legal_cases:export",
            "documents:read", "documents:create", "documents:update", "documents:delete", "documents:upload", "documents:ocr", "documents:export",
            "reports:read", "reports:create", "reports:execute", "reports:export",
            "settings:read", "settings:update",
            "branches:read", "branches:create", "branches:update", "branches:delete",
            "departments:read", "departments:create", "departments:update", "departments:delete",
            "teams:read", "teams:create", "teams:update", "teams:delete",
            "users:read", "users:create", "users:update", "users:delete",
            "roles:read", "roles:create", "roles:update", "roles:delete",
            "audit:read", "audit:export",
            "compliance:read", "compliance:create", "compliance:update", "compliance:export",
            "exposure:read", "exposure:export",
            "notifications:read", "notifications:create", "notifications:update", "notifications:delete",
            "delegations:read", "delegations:create", "delegations:update", "delegations:delete",
            "currencies:read", "currencies:create", "currencies:update", "currencies:delete",
            "sales:read", "sales:create", "sales:update", "sales:delete", "sales:import", "sales:export",
        ]},
        {"name": "Credit Manager", "name_ar": "مدير الائتمان", "description": "Credit department manager", "is_system": False, "permissions": [
            "customers:read", "customers:create", "customers:update", "customers:export",
            "credit_applications:read", "credit_applications:create", "credit_applications:update", "credit_applications:approve", "credit_applications:export",
            "credit_limits:read", "credit_limits:create", "credit_limits:update", "credit_limits:export",
            "collections:read", "collections:assign", "collections:export",
            "reports:read", "reports:execute", "reports:export",
        ]},
        {"name": "Credit Analyst", "name_ar": "محلل ائتماني", "description": "Credit analysis specialist", "is_system": False, "permissions": [
            "customers:read", "customers:update",
            "credit_applications:read", "credit_applications:create", "credit_applications:update",
            "credit_limits:read", "credit_limits:update",
            "reports:read",
        ]},
        {"name": "Collection Manager", "name_ar": "مدير التحصيل", "description": "Collections department manager", "is_system": False, "permissions": [
            "customers:read",
            "collections:read", "collections:create", "collections:update", "collections:assign", "collections:export",
            "legal_cases:read", "legal_cases:create", "legal_cases:update",
            "reports:read", "reports:execute",
        ]},
        {"name": "Legal Manager", "name_ar": "مدير الشؤون القانونية", "description": "Legal department manager", "is_system": False, "permissions": [
            "customers:read",
            "legal_cases:read", "legal_cases:create", "legal_cases:update", "legal_cases:assign", "legal_cases:export",
            "documents:read", "documents:create", "documents:update", "documents:upload",
            "reports:read", "reports:execute",
        ]},
        {"name": "Compliance Manager", "name_ar": "مدير الامتثال", "description": "Compliance department manager", "is_system": False, "permissions": [
            "customers:read", "customers:export",
            "credit_applications:read",
            "compliance:read", "compliance:create", "compliance:update", "compliance:export",
            "audit:read", "audit:export",
            "reports:read", "reports:execute", "reports:export",
        ]},
        {"name": "Read Only", "name_ar": "عرض فقط", "description": "Read-only access", "is_system": False, "permissions": [
            "customers:read", "credit_applications:read", "credit_limits:read",
            "collections:read", "legal_cases:read", "documents:read", "reports:read",
            "sales:read",
        ]},
    ]
    
    created_roles = {}
    for role_data in roles_data:
        role = Role(
            name=role_data["name"],
            name_ar=role_data["name_ar"],
            description=role_data["description"],
            is_system=role_data["is_system"],
            permissions=role_data["permissions"]
        )
        db.add(role)
        await db.flush()
        created_roles[role_data["name"]] = role
    
    users_data = [
        {"email": "admin@creditai.com", "username": "admin", "full_name": "System Administrator", "full_name_ar": "مسؤول النظام", "password": "Admin@123", "role": "Super Admin", "is_superuser": True},
        {"email": "credit@creditai.com", "username": "credit", "full_name": "Credit Manager", "full_name_ar": "مدير الائتمان", "password": "Credit@123", "role": "Credit Manager", "is_superuser": False},
        {"email": "analyst@creditai.com", "username": "analyst", "full_name": "Credit Analyst", "full_name_ar": "محلل ائتماني", "password": "Analyst@123", "role": "Credit Analyst", "is_superuser": False},
        {"email": "collection@creditai.com", "username": "collection", "full_name": "Collection Manager", "full_name_ar": "مدير التحصيل", "password": "Collection@123", "role": "Collection Manager", "is_superuser": False},
        {"email": "legal@creditai.com", "username": "legal", "full_name": "Legal Manager", "full_name_ar": "مدير الشؤون القانونية", "password": "Legal@123", "role": "Legal Manager", "is_superuser": False},
        {"email": "compliance@creditai.com", "username": "compliance", "full_name": "Compliance Manager", "full_name_ar": "مدير الامتثال", "password": "Compliance@123", "role": "Compliance Manager", "is_superuser": False},
    ]
    
    created_users = []
    for user_data in users_data:
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            full_name=user_data["full_name"],
            full_name_ar=user_data["full_name_ar"],
            password_hash=auth_service.get_password_hash(user_data["password"]),
            is_superuser=user_data["is_superuser"],
            is_active=True
        )
        db.add(user)
        await db.flush()
        
        user_role = UserRole(
            user_id=user.id,
            role_id=created_roles[user_data["role"]].id
        )
        db.add(user_role)
        created_users.append({"email": user_data["email"], "password": user_data["password"]})
    
    currencies_data = [
        {"code": "YER_N", "name": "Yemeni Rial (North)", "name_ar": "ريال يمني شمالي", "symbol": "﷼", "is_base": True, "exchange_rate": 1.0},
        {"code": "YER_S", "name": "Yemeni Rial (South)", "name_ar": "ريال يمني جنوبي", "symbol": "﷼", "is_base": False, "exchange_rate": 1.0},
        {"code": "SAR", "name": "Saudi Riyal", "name_ar": "ريال سعودي", "symbol": "﷼", "is_base": False, "exchange_rate": 0.10},
        {"code": "USD", "name": "US Dollar", "name_ar": "دولار أمريكي", "symbol": "$", "is_base": False, "exchange_rate": 0.004},
    ]
    
    for currency_data in currencies_data:
        currency = Currency(**currency_data)
        db.add(currency)
    
    reports_data = [
        {
            "name": "Customer Summary Report",
            "name_ar": "تقرير ملخص العملاء",
            "title_en": "Customer Summary Report",
            "description": "تقرير شامل يحتوي على ملخص لجميع العملاء وبياناتهم الأساسية",
            "module": "customers",
            "query_template": "SELECT * FROM customers WHERE is_active = true",
            "format": "pdf",
            "icon": "Users",
            "color": "text-blue-500",
        },
        {
            "name": "Credit Applications Report",
            "name_ar": "تقرير طلبات الائتمان",
            "title_en": "Credit Applications Report",
            "description": "تقرير بجميع طلبات الائتمان وحالاتها من المسودة إلى الموافقة أو الرفض",
            "module": "credit",
            "query_template": "SELECT * FROM credit_applications WHERE is_active = true",
            "format": "pdf",
            "icon": "FileText",
            "color": "text-green-500",
        },
        {
            "name": "Credit Limits Report",
            "name_ar": "تقرير حدود الائتمان",
            "title_en": "Credit Limits Report",
            "description": "تقرير بحدود الائتمان المعتمدة للمعملاء والاستهلاك الحالي",
            "module": "credit",
            "query_template": "SELECT * FROM credit_limits WHERE is_active = true",
            "format": "pdf",
            "icon": "CreditCard",
            "color": "text-purple-500",
        },
        {
            "name": "Collections Report",
            "name_ar": "تقرير التحصيل",
            "title_en": "Collections Report",
            "description": "تقرير مفصل بالفواتير المتأخرة وأيام التأخير وحالة التحصيل",
            "module": "collections",
            "query_template": "SELECT * FROM invoices WHERE is_active = true",
            "format": "pdf",
            "icon": "TrendingUp",
            "color": "text-orange-500",
        },
        {
            "name": "Aging Report",
            "name_ar": "تقرير التقادم الائتماني",
            "title_en": "Aging Report",
            "description": "تحليل توزيع الديون حسب فترات التأخر (0-30، 31-60، 61-90، أكثر من 90 يوم)",
            "module": "collections",
            "query_template": "SELECT * FROM invoices WHERE is_active = true ORDER BY aging_days",
            "format": "pdf",
            "icon": "BarChart3",
            "color": "text-red-500",
        },
        {
            "name": "Risk Assessment Report",
            "name_ar": "تقرير تقييم المخاطر",
            "title_en": "Risk Assessment Report",
            "description": "تقييم شامل للمخاطر الائتمانية بناءً على درجة الائتمان وتصنيف العملاء",
            "module": "compliance",
            "query_template": "SELECT * FROM customers WHERE is_active = true",
            "format": "pdf",
            "icon": "AlertTriangle",
            "color": "text-yellow-500",
        },
        {
            "name": "Legal Cases Report",
            "name_ar": "تقرير القضايا القانونية",
            "title_en": "Legal Cases Report",
            "description": "تقرير بجميع القضايا القانونية الجارية وحالتها والتواريخ المهمة",
            "module": "legal",
            "query_template": "SELECT * FROM legal_cases WHERE is_active = true",
            "format": "pdf",
            "icon": "Scale",
            "color": "text-indigo-500",
        },
        {
            "name": "Document Registry Report",
            "name_ar": "تقرير سجل الوثائق",
            "title_en": "Document Registry Report",
            "description": "تقرير بجميع الوثائق المرفوعة في النظام مع تصنيفاتها وتواريخ الرفع",
            "module": "documents",
            "query_template": "SELECT * FROM documents WHERE is_active = true",
            "format": "pdf",
            "icon": "FolderOpen",
            "color": "text-teal-500",
        },
        {
            "name": "Audit Trail Report",
            "name_ar": "تقرير سجل التدقيق",
            "title_en": "Audit Trail Report",
            "description": "تقرير شامل بجميع العمليات والتعديلات التي تمت في النظام",
            "module": "audit",
            "query_template": "SELECT * FROM audit_logs ORDER BY created_at DESC",
            "format": "pdf",
            "icon": "History",
            "color": "text-gray-500",
        },
    ]
    
    for report_data in reports_data:
        report = ReportTemplate(**report_data)
        db.add(report)
    
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
    
    for module, config in PERMISSION_MODULES.items():
        for action in config['permissions']:
            perm = Permission(
                name=f"{module}:{action}",
                description=f"{config['ar']} - {action}",
                module=module,
                action=action
            )
            db.add(perm)
    
    await db.commit()
    
    return {
        "message": "Database seeded successfully",
        "users": created_users,
        "currencies": [c["code"] for c in currencies_data]
    }
