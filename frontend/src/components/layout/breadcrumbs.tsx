'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronLeft, Home } from 'lucide-react';

const routeLabels: Record<string, { ar: string; en: string }> = {
  dashboard: { ar: 'لوحة التحكم', en: 'Dashboard' },
  users: { ar: 'المستخدمون', en: 'Users' },
  roles: { ar: 'الأدوار والصلاحيات', en: 'Roles' },
  customers: { ar: 'العملاء', en: 'Customers' },
  new: { ar: 'جديد', en: 'New' },
  'credit-applications': { ar: 'طلبات الائتمان', en: 'Credit Applications' },
  'credit-limits': { ar: 'حدود الائتمان', en: 'Credit Limits' },
  collections: { ar: 'التحصيل', en: 'Collections' },
  legal: { ar: 'الإجراءات القانونية', en: 'Legal' },
  documents: { ar: 'الوثائق', en: 'Documents' },
  reports: { ar: 'التقارير', en: 'Reports' },
  settings: { ar: 'الإعدادات', en: 'Settings' },
  compliance: { ar: 'الامتثال', en: 'Compliance' },
  exposure: { ar: 'النفاذ والمخاطر', en: 'Exposure' },
  'ai-center': { ar: 'مركز الذكاء الاصطناعي', en: 'AI Center' },
  workflow: { ar: 'سير العمل', en: 'Workflow' },
  audit: { ar: 'سجل التدقيق', en: 'Audit' },
  'sap-integration': { ar: 'تكامل SAP', en: 'SAP Integration' },
};

export function Breadcrumbs() {
  const pathname = usePathname();
  const segments = pathname?.split('/').filter(Boolean) || [];

  if (segments.length === 0 || (segments.length === 1 && segments[0] === 'dashboard')) {
    return null;
  }

  const breadcrumbs = segments.map((segment, index) => {
    const href = '/' + segments.slice(0, index + 1).join('/');
    const label = routeLabels[segment] || { ar: segment, en: segment };
    const isLast = index === segments.length - 1;
    return { href, label, isLast };
  });

  return (
    <nav className="mb-4 flex items-center gap-1 text-sm text-muted-foreground font-arabic">
      <Link href="/" className="flex items-center hover:text-foreground">
        <Home className="h-4 w-4" />
      </Link>
      {breadcrumbs.map((crumb) => (
        <span key={crumb.href} className="flex items-center gap-1">
          <ChevronLeft className="h-3 w-3" />
          {crumb.isLast ? (
            <span className="text-foreground font-medium">{crumb.label.ar}</span>
          ) : (
            <Link href={crumb.href} className="hover:text-foreground">
              {crumb.label.ar}
            </Link>
          )}
        </span>
      ))}
    </nav>
  );
}
