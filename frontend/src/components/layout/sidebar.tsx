'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  LayoutDashboard,
  Users,
  Shield,
  Building2,
  UserPlus,
  FileText,
  CreditCard,
  Banknote,
  Scale,
  FolderOpen,
  BarChart3,
  CheckCircle,
  AlertTriangle,
  Brain,
  GitBranch,
  History,
  Database,
  Settings,
  ChevronLeft,
  ChevronRight,
  LogOut,
  DollarSign,
  ShoppingCart,
} from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

const iconMap: Record<string, any> = {
  LayoutDashboard,
  Users,
  Shield,
  Building2,
  UserPlus,
  FileText,
  CreditCard,
  Banknote,
  Scale,
  FolderOpen,
  BarChart3,
  CheckCircle,
  AlertTriangle,
  Brain,
  GitBranch,
  History,
  Database,
  Settings,
  DollarSign,
  ShoppingCart,
};

const navigationSections = [
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
      { label: 'الأدوار والصلاحيات', labelEn: 'Roles', href: '/roles', icon: 'Shield' },
    ],
  },
  {
    section: 'إدارة العملاء',
    sectionEn: 'Customer Management',
    items: [
      { label: 'العملاء', labelEn: 'Customers', href: '/customers', icon: 'Building2' },
      { label: 'المبيعات', labelEn: 'Sales', href: '/sales', icon: 'ShoppingCart' },
    ],
  },
  {
    section: 'القرارات الائتمانية',
    sectionEn: 'Credit Decisions',
    items: [
      { label: 'طلبات الائتمان', labelEn: 'Applications', href: '/credit-applications', icon: 'FileText' },
      { label: 'حدود الائتمان', labelEn: 'Credit Limits', href: '/credit-limits', icon: 'CreditCard' },
    ],
  },
  {
    section: 'التحصيل والتدفق النقدي',
    sectionEn: 'Collections',
    items: [
      { label: 'التحصيل', labelEn: 'Collections', href: '/collections', icon: 'Banknote' },
    ],
  },
  {
    section: 'الإجراءات القانونية',
    sectionEn: 'Legal',
    items: [
      { label: 'الإجراءات القانونية', labelEn: 'Legal', href: '/legal', icon: 'Scale' },
    ],
  },
  {
    section: 'إدارة الوثائق',
    sectionEn: 'Documents',
    items: [
      { label: 'الوثائق', labelEn: 'Documents', href: '/documents', icon: 'FolderOpen' },
    ],
  },
  {
    section: 'التقارير والتحليلات',
    sectionEn: 'Reports & Analytics',
    items: [
      { label: 'التقارير', labelEn: 'Reports', href: '/reports', icon: 'BarChart3' },
    ],
  },
  {
    section: 'الامتثال والمخاطر',
    sectionEn: 'Compliance & Risk',
    items: [
      { label: 'الامتثال', labelEn: 'Compliance', href: '/compliance', icon: 'CheckCircle' },
      { label: 'النفاذ والمخاطر', labelEn: 'Exposure', href: '/exposure', icon: 'AlertTriangle' },
    ],
  },
  {
    section: 'التقنية المتقدمة',
    sectionEn: 'Advanced Tech',
    items: [
      { label: 'مركز الذكاء الاصطناعي', labelEn: 'AI Center', href: '/ai-center', icon: 'Brain' },
      { label: 'سير العمل', labelEn: 'Workflow', href: '/workflow', icon: 'GitBranch' },
      { label: 'سجل التدقيق', labelEn: 'Audit', href: '/audit', icon: 'History' },
      { label: 'تكامل SAP', labelEn: 'SAP', href: '/sap-integration', icon: 'Database' },
    ],
  },
  {
    section: 'النظام',
    sectionEn: 'System',
    items: [
      { label: 'العملات', labelEn: 'Currencies', href: '/currencies', icon: 'DollarSign' },
      { label: 'الإعدادات', labelEn: 'Settings', href: '/settings', icon: 'Settings' },
    ],
  },
];

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const pathname = usePathname();
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(navigationSections.map((s) => s.sectionEn))
  );

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(section)) {
        next.delete(section);
      } else {
        next.add(section);
      }
      return next;
    });
  };

  return (
    <div
      className={cn(
        'relative flex h-screen flex-col border-l bg-card transition-all duration-300',
        collapsed ? 'w-16' : 'w-64'
      )}
    >
      <div className="flex h-14 items-center justify-between border-b px-4">
        {!collapsed && (
          <span className="text-lg font-bold text-primary">CreditAI</span>
        )}
        <button
          onClick={onToggle}
          className="rounded-md p-1 hover:bg-muted"
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      <ScrollArea className="flex-1 py-2">
        {navigationSections.map((section) => {
          const isExpanded = expandedSections.has(section.sectionEn);
          return (
            <div key={section.sectionEn} className="mb-1">
              {!collapsed && (
                <button
                  onClick={() => toggleSection(section.sectionEn)}
                  className="flex w-full items-center justify-between px-4 py-2 text-xs font-semibold text-muted-foreground hover:text-foreground"
                >
                  <span className="font-arabic">{section.section}</span>
                  <ChevronLeft
                    className={cn(
                      'h-3 w-3 transition-transform',
                      isExpanded && '-rotate-90'
                    )}
                  />
                </button>
              )}
              <div className={cn('space-y-0.5', collapsed && 'px-2')}>
                {section.items.map((item) => {
                  const Icon = iconMap[item.icon] || LayoutDashboard;
                  const isActive = pathname === item.href || pathname?.startsWith(item.href + '/');
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={cn(
                        'flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors hover:bg-muted',
                        isActive && 'bg-primary/10 text-primary font-medium',
                        collapsed && 'justify-center px-2'
                      )}
                      title={collapsed ? item.label : undefined}
                    >
                      <Icon className="h-4 w-4 shrink-0" />
                      {!collapsed && (
                        <span className="font-arabic truncate">{item.label}</span>
                      )}
                    </Link>
                  );
                })}
              </div>
            </div>
          );
        })}
      </ScrollArea>

      <div className="border-t p-2">
        <Link
          href="/login"
          className={cn(
            'flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground',
            collapsed && 'justify-center px-2'
          )}
        >
          <LogOut className="h-4 w-4" />
          {!collapsed && <span className="font-arabic">تسجيل الخروج</span>}
        </Link>
      </div>
    </div>
  );
}
