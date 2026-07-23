'use client';

import { createContext, useContext, useState, useCallback, ReactNode, useEffect } from 'react';

type Locale = 'ar' | 'en';

interface LanguageContextType {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  isRtl: boolean;
  t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

const translations: Record<Locale, Record<string, string>> = {
  ar: {
    'app.name': 'كريدي آي enterprise',
    'nav.dashboard': 'لوحة التحكم',
    'nav.users': 'المستخدمون',
    'nav.roles': 'الأدوار والصلاحيات',
    'nav.customers': 'العملاء',
    'nav.creditApplications': 'طلبات الائتمان',
    'nav.creditLimits': 'حدود الائتمان',
    'nav.collections': 'التحصيل',
    'nav.legal': 'الإجراءات القانونية',
    'nav.documents': 'الوثائق',
    'nav.reports': 'التقارير',
    'nav.settings': 'الإعدادات',
    'nav.compliance': 'الامتثال',
    'nav.exposure': 'النفاذ والمخاطر',
    'nav.aiCenter': 'مركز الذكاء الاصطناعي',
    'nav.workflow': 'سير العمل',
    'nav.audit': 'سجل التدقيق',
    'nav.sapIntegration': 'تكامل SAP',
    'auth.login': 'تسجيل الدخول',
    'auth.logout': 'تسجيل الخروج',
    'auth.forgotPassword': 'نسيت كلمة المرور',
    'common.save': 'حفظ',
    'common.cancel': 'إلغاء',
    'common.delete': 'حذف',
    'common.edit': 'تعديل',
    'common.view': 'عرض',
    'common.search': 'بحث',
    'common.filter': 'تصفية',
    'common.export': 'تصدير',
    'common.import': 'استيراد',
    'common.loading': 'جاري التحميل...',
    'common.noData': 'لا توجد بيانات',
    'common.confirm': 'تأكيد',
    'common.back': 'رجوع',
    'common.next': 'التالي',
    'common.previous': 'السابق',
    'common.submit': 'إرسال',
    'common.close': 'إغلاق',
    'common.add': 'إضافة',
    'common.new': 'جديد',
    'common.status': 'الحالة',
    'common.active': 'نشط',
    'common.inactive': 'غير نشط',
    'common.pending': 'معلق',
    'common.approved': 'مقبول',
    'common.rejected': 'مرفوض',
    'common.all': 'الكل',
    'common.actions': 'الإجراءات',
    'common.details': 'التفاصيل',
    'common.overview': 'نظرة عامة',
    'common.general': 'عام',
    'common.yes': 'نعم',
    'common.no': 'لا',
    'common.success': 'نجاح',
    'common.error': 'خطأ',
    'common.warning': 'تحذير',
    'common.info': 'معلومات',
    'dashboard.welcome': 'مرحباً بك في منصة CreditAI Enterprise',
    'dashboard.totalCustomers': 'إجمالي العملاء',
    'dashboard.creditApplications': 'طلبات الائتمان',
    'dashboard.totalExposure': 'إجمالي الحسابات',
    'dashboard.approvalRate': 'معدل القبول',
    'dashboard.alerts': 'تحذيرات',
    'dashboard.pendingReview': 'معلق',
    'dashboard.creditAnalysis': 'تحليل الائتمان',
    'dashboard.monthlyCollections': 'المحصلة الشهرية',
    'dashboard.recentActivity': 'النشاط الأخير',
    'dashboard.alertsWidget': 'التحذيرات',
  },
  en: {
    'app.name': 'CreditAI Enterprise',
    'nav.dashboard': 'Dashboard',
    'nav.users': 'Users',
    'nav.roles': 'Roles & Permissions',
    'nav.customers': 'Customers',
    'nav.creditApplications': 'Credit Applications',
    'nav.creditLimits': 'Credit Limits',
    'nav.collections': 'Collections',
    'nav.legal': 'Legal',
    'nav.documents': 'Documents',
    'nav.reports': 'Reports',
    'nav.settings': 'Settings',
    'nav.compliance': 'Compliance',
    'nav.exposure': 'Exposure & Risk',
    'nav.aiCenter': 'AI Center',
    'nav.workflow': 'Workflow',
    'nav.audit': 'Audit Log',
    'nav.sapIntegration': 'SAP Integration',
    'auth.login': 'Login',
    'auth.logout': 'Logout',
    'auth.forgotPassword': 'Forgot Password',
    'common.save': 'Save',
    'common.cancel': 'Cancel',
    'common.delete': 'Delete',
    'common.edit': 'Edit',
    'common.view': 'View',
    'common.search': 'Search',
    'common.filter': 'Filter',
    'common.export': 'Export',
    'common.import': 'Import',
    'common.loading': 'Loading...',
    'common.noData': 'No data',
    'common.confirm': 'Confirm',
    'common.back': 'Back',
    'common.next': 'Next',
    'common.previous': 'Previous',
    'common.submit': 'Submit',
    'common.close': 'Close',
    'common.add': 'Add',
    'common.new': 'New',
    'common.status': 'Status',
    'common.active': 'Active',
    'common.inactive': 'Inactive',
    'common.pending': 'Pending',
    'common.approved': 'Approved',
    'common.rejected': 'Rejected',
    'common.all': 'All',
    'common.actions': 'Actions',
    'common.details': 'Details',
    'common.overview': 'Overview',
    'common.general': 'General',
    'common.yes': 'Yes',
    'common.no': 'No',
    'common.success': 'Success',
    'common.error': 'Error',
    'common.warning': 'Warning',
    'common.info': 'Info',
    'dashboard.welcome': 'Welcome to CreditAI Enterprise Platform',
    'dashboard.totalCustomers': 'Total Customers',
    'dashboard.creditApplications': 'Credit Applications',
    'dashboard.totalExposure': 'Total Exposure',
    'dashboard.approvalRate': 'Approval Rate',
    'dashboard.alerts': 'Alerts',
    'dashboard.pendingReview': 'Pending Review',
    'dashboard.creditAnalysis': 'Credit Analysis',
    'dashboard.monthlyCollections': 'Monthly Collections',
    'dashboard.recentActivity': 'Recent Activity',
    'dashboard.alertsWidget': 'Alerts',
  },
};

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('ar');

  useEffect(() => {
    const saved = localStorage.getItem('locale') as Locale;
    if (saved && (saved === 'ar' || saved === 'en')) {
      setLocaleState(saved);
    }
  }, []);

  const setLocale = useCallback((newLocale: Locale) => {
    setLocaleState(newLocale);
    localStorage.setItem('locale', newLocale);
    document.documentElement.lang = newLocale;
    document.documentElement.dir = newLocale === 'ar' ? 'rtl' : 'ltr';
  }, []);

  const t = useCallback(
    (key: string): string => {
      return translations[locale]?.[key] || translations.en[key] || key;
    },
    [locale]
  );

  return (
    <LanguageContext.Provider
      value={{
        locale,
        setLocale,
        isRtl: locale === 'ar',
        t,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
