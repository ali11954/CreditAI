'use client';

import { useState, useEffect, useCallback } from 'react';
import { StatCard } from '@/components/widgets/stat-card';
import { ChartCard } from '@/components/widgets/chart-card';
import { RecentActivity } from '@/components/widgets/recent-activity';
import { AlertsWidget } from '@/components/widgets/alerts-widget';
import {
  Users,
  FileText,
  DollarSign,
  TrendingUp,
  AlertTriangle,
  Clock,
  Loader2,
} from 'lucide-react';
import { formatCurrency } from '@/components/ui/currency-select';
import { toast } from 'sonner';
import api from '@/lib/api';

export default function DashboardPage() {
  const [stats, setStats] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get('/dashboards/summary');
      const data = res.data;
      const s = data.stats;

      setStats([
        {
          title: 'إجمالي العملاء',
          titleEn: 'Total Customers',
          value: s.customers?.value?.toLocaleString('en-US') || '0',
          change: s.customers?.change || '+0%',
          changeType: s.customers?.changeType || 'positive',
          icon: Users,
        },
        {
          title: 'طلبات الائتمان',
          titleEn: 'Credit Applications',
          value: s.credit_applications?.value?.toLocaleString('en-US') || '0',
          change: s.credit_applications?.change || '+0%',
          changeType: s.credit_applications?.changeType || 'positive',
          icon: FileText,
        },
        {
          title: 'إجمالي الحسابات',
          titleEn: 'Total Exposure',
          value: formatCurrency(s.exposure?.value || 0, 'YER_N', 'ar'),
          change: s.exposure?.change || '+0%',
          changeType: s.exposure?.changeType || 'positive',
          icon: DollarSign,
        },
        {
          title: 'معدل القبول',
          titleEn: 'Approval Rate',
          value: `${s.approval_rate?.value || 0}%`,
          change: s.approval_rate?.change || '+0%',
          changeType: s.approval_rate?.changeType || 'positive',
          icon: TrendingUp,
        },
        {
          title: 'تحذيرات',
          titleEn: 'Overdue Invoices',
          value: String(s.overdue?.value || 0),
          change: s.overdue?.changeType === 'negative' ? '+1' : '0',
          changeType: s.overdue?.changeType || 'positive',
          icon: AlertTriangle,
        },
        {
          title: 'معلق',
          titleEn: 'Pending Review',
          value: String(s.pending?.value || 0),
          change: s.pending?.value > 0 ? 'يحتاج مراجعة' : 'لا يوجد',
          changeType: 'positive',
          icon: Clock,
        },
      ]);
    } catch (err: any) {
      console.error('Dashboard fetch error');
      setStats([
        { title: 'إجمالي العملاء', titleEn: 'Total Customers', value: '0', change: '+0%', changeType: 'positive', icon: Users },
        { title: 'طلبات الائتمان', titleEn: 'Credit Applications', value: '0', change: '+0%', changeType: 'positive', icon: FileText },
        { title: 'إجمالي الحسابات', titleEn: 'Total Exposure', value: formatCurrency(0, 'YER_N', 'ar'), change: '+0%', changeType: 'positive', icon: DollarSign },
        { title: 'معدل القبول', titleEn: 'Approval Rate', value: '0%', change: '+0%', changeType: 'positive', icon: TrendingUp },
        { title: 'تحذيرات', titleEn: 'Overdue Invoices', value: '0', change: '0', changeType: 'positive', icon: AlertTriangle },
        { title: 'معلق', titleEn: 'Pending Review', value: '0', change: '0', changeType: 'positive', icon: Clock },
      ]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchDashboard(); }, [fetchDashboard]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold font-arabic">لوحة التحكم</h1>
          <p className="text-muted-foreground font-arabic">
            مرحباً بك في منصة CreditAI Enterprise
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {stats.map((stat, i) => (
          <StatCard key={i} {...stat} />
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <ChartCard
          title="تحليل الائتمان"
          titleEn="Credit Analysis"
          type="area"
          endpoint="/dashboards/chart/credit-analysis"
        />
        <ChartCard
          title="المحصلة الشهرية"
          titleEn="Monthly Collections"
          type="bar"
          endpoint="/dashboards/chart/collections"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <RecentActivity />
        </div>
        <div>
          <AlertsWidget />
        </div>
      </div>
    </div>
  );
}
