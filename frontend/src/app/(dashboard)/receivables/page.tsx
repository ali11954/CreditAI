'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BarChart2, TrendingDown, Clock, AlertTriangle, DollarSign } from 'lucide-react';
import api from '@/lib/api';

interface AgingData {
  bucket: string;
  count: number;
  amount: number;
}

interface KPICard {
  label: string;
  value: string;
  icon: any;
  color: string;
  trend?: string;
}

export default function ReceivablesPage() {
  const [aging, setAging] = useState<AgingData[]>([]);
  const [kpis, setKpis] = useState<KPICard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const res = await api.get('/collections/sales-invoices');
      const invoices = res.data.items || [];
      
      const buckets: AgingData[] = [
        { bucket: '0-30 يوم', count: 0, amount: 0 },
        { bucket: '31-60 يوم', count: 0, amount: 0 },
        { bucket: '61-90 يوم', count: 0, amount: 0 },
        { bucket: '91-120 يوم', count: 0, amount: 0 },
        { bucket: '120+ يوم', count: 0, amount: 0 },
      ];

      let totalBalance = 0;
      let totalOverdue = 0;
      let overdueCount = 0;

      invoices.forEach((inv: any) => {
        const balance = inv.balance || 0;
        const overdueDays = inv.overdue_days || 0;
        totalBalance += balance;
        
        if (overdueDays > 0) {
          totalOverdue += balance;
          overdueCount++;
        }

        if (overdueDays <= 30) { buckets[0].count++; buckets[0].amount += balance; }
        else if (overdueDays <= 60) { buckets[1].count++; buckets[1].amount += balance; }
        else if (overdueDays <= 90) { buckets[2].count++; buckets[2].amount += balance; }
        else if (overdueDays <= 120) { buckets[3].count++; buckets[3].amount += balance; }
        else { buckets[4].count++; buckets[4].amount += balance; }
      });

      setAging(buckets);

      const avgDelay = invoices.reduce((sum: number, inv: any) => sum + (inv.overdue_days || 0), 0) / (invoices.length || 1);
      const collectionRate = invoices.length > 0 ? ((invoices.filter((i: any) => i.status === 'paid').length / invoices.length) * 100) : 0;

      setKpis([
        { label: 'إجمالي المديونيات', value: totalBalance.toLocaleString() + ' ر.ي', icon: DollarSign, color: 'text-blue-600 bg-blue-100' },
        { label: 'المديونيات المتأخرة', value: totalOverdue.toLocaleString() + ' ر.ي', icon: AlertTriangle, color: 'text-red-600 bg-red-100' },
        { label: 'DSO (متوسط أيام التحصيل)', value: Math.round(avgDelay) + ' يوم', icon: Clock, color: 'text-amber-600 bg-amber-100' },
        { label: 'نسبة التحصيل', value: collectionRate.toFixed(1) + '%', icon: TrendingDown, color: 'text-green-600 bg-green-100' },
        { label: 'عدد الفواتير المتأخرة', value: overdueCount.toString(), icon: BarChart2, color: 'text-purple-600 bg-purple-100' },
      ]);
    } catch { } finally { setLoading(false); }
  };

  const bucketColor = (i: number) => {
    const colors = ['bg-green-500', 'bg-yellow-500', 'bg-orange-500', 'bg-red-400', 'bg-red-600'];
    return colors[i] || 'bg-gray-500';
  };

  const maxAmount = Math.max(...aging.map(a => a.amount), 1);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
          <BarChart2 className="h-5 w-5 text-primary" />
        </div>
        <div>
          <h1 className="text-2xl font-bold font-arabic">المديونيات و Aging Report</h1>
          <p className="text-sm text-muted-foreground font-arabic">مؤشرات أداء التحصيل وتحليل الأعمار المدينة</p>
        </div>
      </div>

      {loading ? (
        <Card><CardContent className="py-10 text-center font-arabic">جاري التحميل...</CardContent></Card>
      ) : (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {kpis.map((kpi, i) => (
              <Card key={i}>
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${kpi.color}`}>
                      <kpi.icon className="h-5 w-5" />
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground font-arabic">{kpi.label}</p>
                      <p className="text-lg font-bold">{kpi.value}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">Aging Report — توزيع الأعمار المدينة</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {aging.map((bucket, i) => (
                  <div key={i} className="space-y-1">
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-arabic font-medium">{bucket.bucket}</span>
                      <span className="text-muted-foreground">{bucket.amount.toLocaleString()} ر.ي ({bucket.count} فاتورة)</span>
                    </div>
                    <div className="h-6 w-full rounded-full bg-muted overflow-hidden">
                      <div
                        className={`h-full rounded-full ${bucketColor(i)} transition-all`}
                        style={{ width: `${(bucket.amount / maxAmount) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
