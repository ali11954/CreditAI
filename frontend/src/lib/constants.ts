export const APP_NAME = 'CreditAI Enterprise';
export const APP_NAME_AR = 'كريدي آيenterprise';

export const API_URL = '/api/v1';

export const LOCALES = [
  { code: 'ar', name: 'العربية', flag: '🇮🇱' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
] as const;

export const DEFAULT_LOCALE = 'ar';

export const ROLES = {
  ADMIN: 'admin',
  MANAGER: 'manager',
  ANALYST: 'analyst',
  COLLECTIONS: 'collections',
  LEGAL: 'legal',
  VIEWER: 'viewer',
} as const;

export const CUSTOMER_STATUSES = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  PENDING: 'pending',
  BLOCKED: 'blocked',
} as const;

export const CREDIT_STATUSES = {
  DRAFT: 'draft',
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
  EXPIRED: 'expired',
} as const;

export const PAYMENT_STATUSES = {
  PAID: 'paid',
  PENDING: 'pending',
  OVERDUE: 'overdue',
  PARTIAL: 'partial',
} as const;

export const RISK_LEVELS = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical',
} as const;

export const DOCUMENT_TYPES = {
  ID_CARD: 'id_card',
  PASSPORT: 'passport',
  INCOME_PROOF: 'income_proof',
  BANK_STATEMENT: 'bank_statement',
  CONTRACT: 'contract',
  COURT_ORDER: 'court_order',
  OTHER: 'other',
} as const;

export const NAVIGATION_ITEMS = [
  {
    section: 'الرئيسية',
    sectionEn: 'Main',
    items: [
      { label: 'لوحة التحكم', labelEn: 'Dashboard', href: '/', icon: 'LayoutDashboard' },
    ],
  },
  {
    section: 'إدارة المستخدمين',
    sectionEn: 'User Management',
    items: [
      { label: 'المستخدمون', labelEn: 'Users', href: '/users', icon: 'Users' },
      { label: 'الأدوار والصلاحيات', labelEn: 'Roles & Permissions', href: '/roles', icon: 'Shield' },
    ],
  },
  {
    section: 'إدارة العملاء',
    sectionEn: 'Customer Management',
    items: [
      { label: 'العملاء', labelEn: 'Customers', href: '/customers', icon: 'Building2' },
      { label: 'عميل جديد', labelEn: 'New Customer', href: '/customers/new', icon: 'UserPlus' },
    ],
  },
  {
    section: 'القرارات الائتمانية',
    sectionEn: 'Credit Decisions',
    items: [
      { label: 'طلبات الائتمان', labelEn: 'Credit Applications', href: '/credit-applications', icon: 'FileText' },
      { label: 'حدود الائتمان', labelEn: 'Credit Limits', href: '/credit-limits', icon: 'CreditCard' },
    ],
  },
  {
    section: 'التحصيل والتدفق النقدي',
    sectionEn: 'Collections & Cash Flow',
    items: [
      { label: 'التحصيل', labelEn: 'Collections', href: '/collections', icon: 'Banknote' },
    ],
  },
  {
    section: 'الإجراءات القانونية',
    sectionEn: 'Legal Actions',
    items: [
      { label: 'الإجراءات القانونية', labelEn: 'Legal', href: '/legal', icon: 'Scale' },
    ],
  },
  {
    section: 'إدارة الوثائق',
    sectionEn: 'Document Management',
    items: [
      { label: 'الوثائق', labelEn: 'Documents', href: '/documents', icon: 'FolderOpen' },
    ],
  },
  {
    section: 'التقارير',
    sectionEn: 'Reports',
    items: [
      { label: 'التقارير', labelEn: 'Reports', href: '/reports', icon: 'BarChart3' },
    ],
  },
  {
    section: 'الامتثال',
    sectionEn: 'Compliance',
    items: [
      { label: 'الامتثال', labelEn: 'Compliance', href: '/compliance', icon: 'CheckCircle' },
    ],
  },
  {
    section: 'إدارة المخاطر',
    sectionEn: 'Risk Management',
    items: [
      { label: 'النفاذ والمخاطر', labelEn: 'Exposure & Risk', href: '/exposure', icon: 'AlertTriangle' },
    ],
  },
  {
    section: 'مركز الذكاء الاصطناعي',
    sectionEn: 'AI Center',
    items: [
      { label: 'مركز الذكاء الاصطناعي', labelEn: 'AI Center', href: '/ai-center', icon: 'Brain' },
    ],
  },
  {
    section: 'أتمتة سير العمل',
    sectionEn: 'Workflow Automation',
    items: [
      { label: 'سير العمل', labelEn: 'Workflow', href: '/workflow', icon: 'GitBranch' },
    ],
  },
  {
    section: 'التدقيق والمراجعة',
    sectionEn: 'Audit',
    items: [
      { label: 'سجل التدقيق', labelEn: 'Audit Log', href: '/audit', icon: 'History' },
    ],
  },
  {
    section: 'تكامل SAP',
    sectionEn: 'SAP Integration',
    items: [
      { label: 'تكامل SAP', labelEn: 'SAP Integration', href: '/sap-integration', icon: 'Database' },
    ],
  },
  {
    section: 'الإعدادات',
    sectionEn: 'Settings',
    items: [
      { label: 'الإعدادات', labelEn: 'Settings', href: '/settings', icon: 'Settings' },
    ],
  },
];
