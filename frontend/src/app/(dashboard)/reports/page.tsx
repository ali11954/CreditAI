'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  BarChart3, FileText, Users, CreditCard, TrendingUp,
  AlertTriangle, DollarSign, ShoppingCart, Loader2,
} from 'lucide-react';
import { toast } from 'sonner';
import api from '@/lib/api';
import { formatCurrency } from '@/components/ui/currency-select';

export default function ReportsPage() {
  const [agingData, setAgingData] = useState<any>(null);
  const [salesSummary, setSalesSummary] = useState<any>(null);
  const [riskData, setRiskData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('sales');

  const fetchAll = useCallback(async () => {
    setLoading(true);
    try {
      const [agingRes, salesRes, riskRes] = await Promise.allSettled([
        api.get('/reports/aging'),
        api.get('/reports/sales-summary'),
        api.get('/reports/risk-assessment'),
      ]);
      if (agingRes.status === 'fulfilled') setAgingData(agingRes.value.data);
      if (salesRes.status === 'fulfilled') setSalesSummary(salesRes.value.data);
      if (riskRes.status === 'fulfilled') setRiskData(riskRes.value.data);
    } catch (err: any) {
      toast.error('فشل في تحميل التقارير');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  const bucketColors: Record<string, string> = {
    current: 'text-green-600',
    '1_30': 'text-yellow-600',
    '31_60': 'text-orange-600',
    '61_90': 'text-red-500',
    '90_plus': 'text-red-700',
  };

  const riskColors: Record<string, string> = {
    low: 'text-green-600',
    medium: 'text-yellow-600',
    high: 'text-orange-600',
    critical: 'text-red-700',
  };
  const riskLabels: Record<string, string> = {
    low: 'منخفض', medium: 'متوسط', high: 'عالي', critical: 'حرج',
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports & Analytics"
        titleAr="التقارير والتحليلات"
        description="Live analytics and risk reports"
        descriptionAr="تحليلات مباشرة وتقارير المخاطر"
      />

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="font-arabic">
          <TabsTrigger value="sales">تقرير المبيعات</TabsTrigger>
          <TabsTrigger value="aging">التحليل العمراني للديون</TabsTrigger>
          <TabsTrigger value="risk">تقييم المخاطر</TabsTrigger>
        </TabsList>

        <TabsContent value="sales" className="space-y-6">
          {salesSummary && (
            <>
              <div className="grid gap-4 md:grid-cols-4">
                <Card>
                  <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">إجمالي الفواتير</CardTitle></CardHeader>
                  <CardContent>
                    <p className="text-2xl font-bold">{salesSummary.overall?.total_invoices || 0}</p>
                    <p className="text-xs text-muted-foreground font-arabic">{formatCurrency(salesSummary.overall?.total_amount || 0, 'YER_N', 'ar')}</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">المدفوع</CardTitle></CardHeader>
                  <CardContent>
                    <p className="text-2xl font-bold text-green-600">{formatCurrency(salesSummary.overall?.total_paid || 0, 'YER_N', 'ar')}</p>
                    <p className="text-xs text-muted-foreground font-arabic">
                      {salesSummary.overall?.total_amount > 0
                        ? `${Math.round((salesSummary.overall.total_paid / salesSummary.overall.total_amount) * 100)}%`
                        : '0%'} من الإجمالي
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">الرصيد المتبقي</CardTitle></CardHeader>
                  <CardContent>
                    <p className="text-2xl font-bold text-destructive">{formatCurrency(salesSummary.overall?.total_balance || 0, 'YER_N', 'ar')}</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">المتأخرات</CardTitle></CardHeader>
                  <CardContent>
                    <p className="text-2xl font-bold text-destructive">{salesSummary.overdue?.count || 0}</p>
                    <p className="text-xs text-muted-foreground font-arabic">{formatCurrency(salesSummary.overdue?.total_balance || 0, 'YER_N', 'ar')}</p>
                  </CardContent>
                </Card>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <Card>
                  <CardHeader><CardTitle className="text-base font-arabic">الحالة</CardTitle></CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {(salesSummary.by_status || []).map((s: any) => (
                        <div key={s.status} className="flex items-center justify-between">
                          <span className="font-arabic text-sm">{s.status}</span>
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-bold">{s.count}</span>
                            <Badge variant="outline">{formatCurrency(s.balance, 'YER_N', 'ar')}</Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader><CardTitle className="text-base font-arabic">آخر 30 يوم</CardTitle></CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between"><span className="text-sm text-muted-foreground font-arabic">عدد الفواتير</span><span className="font-bold">{salesSummary.last_30_days?.invoice_count || 0}</span></div>
                      <div className="flex justify-between"><span className="text-sm text-muted-foreground font-arabic">إجمالي المبيعات</span><span className="font-bold">{formatCurrency(salesSummary.last_30_days?.total_amount || 0, 'YER_N', 'ar')}</span></div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {(salesSummary.top_customers || []).length > 0 && (
                <Card>
                  <CardHeader><CardTitle className="text-base font-arabic">أكبر العملاء</CardTitle></CardHeader>
                  <CardContent>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b">
                            <th className="text-right p-2 font-arabic">العميل</th>
                            <th className="text-right p-2 font-arabic">الفواتير</th>
                            <th className="text-right p-2 font-arabic">الإجمالي</th>
                            <th className="text-right p-2 font-arabic">الرصيد</th>
                          </tr>
                        </thead>
                        <tbody>
                          {salesSummary.top_customers.map((c: any, i: number) => (
                            <tr key={i} className="border-b">
                              <td className="p-2 font-arabic">{c.name}</td>
                              <td className="p-2">{c.invoice_count}</td>
                              <td className="p-2">{formatCurrency(c.total_amount, 'YER_N', 'ar')}</td>
                              <td className="p-2 text-destructive">{formatCurrency(c.balance, 'YER_N', 'ar')}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CardContent>
                </Card>
              )}
            </>
          )}
        </TabsContent>

        <TabsContent value="aging" className="space-y-6">
          {agingData && (
            <>
              <div className="grid gap-4 md:grid-cols-5">
                {Object.entries(agingData.buckets || {}).map(([key, bucket]: [string, any]) => (
                  <Card key={key}>
                    <CardHeader className="pb-2"><CardTitle className="text-xs font-arabic">{bucket.label}</CardTitle></CardHeader>
                    <CardContent>
                      <p className={`text-xl font-bold ${bucketColors[key] || ''}`}>{bucket.count}</p>
                      <p className="text-xs text-muted-foreground">{formatCurrency(bucket.total, 'YER_N', 'ar')}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>

              <Card>
                <CardHeader><CardTitle className="text-base font-arabic">تفاصيل الفواتير المتأخرة</CardTitle></CardHeader>
                <CardContent>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b">
                          <th className="text-right p-2 font-arabic">رقم الفاتورة</th>
                          <th className="text-right p-2 font-arabic">العميل</th>
                          <th className="text-right p-2 font-arabic">الإجمالي</th>
                          <th className="text-right p-2 font-arabic">المدفوع</th>
                          <th className="text-right p-2 font-arabic">الرصيد</th>
                          <th className="text-right p-2 font-arabic">أيام التأخير</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(agingData.buckets?.['90_plus']?.items || []).map((item: any) => (
                          <tr key={item.id} className="border-b bg-red-50">
                            <td className="p-2 font-mono">{item.invoice_number}</td>
                            <td className="p-2 font-arabic">{item.customer_name}</td>
                            <td className="p-2">{formatCurrency(item.total_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2">{formatCurrency(item.paid_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2 text-destructive font-bold">{formatCurrency(item.balance, item.currency_code, 'ar')}</td>
                            <td className="p-2 text-destructive font-bold">{item.days_overdue} يوم</td>
                          </tr>
                        ))}
                        {(agingData.buckets?.['61_90']?.items || []).map((item: any) => (
                          <tr key={item.id} className="border-b bg-orange-50">
                            <td className="p-2 font-mono">{item.invoice_number}</td>
                            <td className="p-2 font-arabic">{item.customer_name}</td>
                            <td className="p-2">{formatCurrency(item.total_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2">{formatCurrency(item.paid_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2 text-orange-600 font-bold">{formatCurrency(item.balance, item.currency_code, 'ar')}</td>
                            <td className="p-2 text-orange-600 font-bold">{item.days_overdue} يوم</td>
                          </tr>
                        ))}
                        {(agingData.buckets?.['31_60']?.items || []).map((item: any) => (
                          <tr key={item.id} className="border-b bg-yellow-50">
                            <td className="p-2 font-mono">{item.invoice_number}</td>
                            <td className="p-2 font-arabic">{item.customer_name}</td>
                            <td className="p-2">{formatCurrency(item.total_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2">{formatCurrency(item.paid_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2 text-yellow-600">{formatCurrency(item.balance, item.currency_code, 'ar')}</td>
                            <td className="p-2 text-yellow-600">{item.days_overdue} يوم</td>
                          </tr>
                        ))}
                        {(agingData.buckets?.['1_30']?.items || []).map((item: any) => (
                          <tr key={item.id} className="border-b">
                            <td className="p-2 font-mono">{item.invoice_number}</td>
                            <td className="p-2 font-arabic">{item.customer_name}</td>
                            <td className="p-2">{formatCurrency(item.total_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2">{formatCurrency(item.paid_amount, item.currency_code, 'ar')}</td>
                            <td className="p-2">{formatCurrency(item.balance, item.currency_code, 'ar')}</td>
                            <td className="p-2">{item.days_overdue} يوم</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>

        <TabsContent value="risk" className="space-y-6">
          {riskData && (
            <>
              <div className="grid gap-4 md:grid-cols-4">
                {Object.entries(riskData.summary || {}).map(([level, data]: [string, any]) => (
                  <Card key={level}>
                    <CardHeader className="pb-2"><CardTitle className={`text-sm font-arabic ${riskColors[level]}`}>{riskLabels[level]}</CardTitle></CardHeader>
                    <CardContent>
                      <p className="text-2xl font-bold">{data.count}</p>
                      <p className="text-xs text-muted-foreground">{formatCurrency(data.total_balance, 'YER_N', 'ar')}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>

              <Card>
                <CardHeader><CardTitle className="text-base font-arabic">تقييم المخاطر حسب العميل</CardTitle></CardHeader>
                <CardContent>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b">
                          <th className="text-right p-2 font-arabic">العميل</th>
                          <th className="text-right p-2 font-arabic">الفواتير</th>
                          <th className="text-right p-2 font-arabic">الإجمالي</th>
                          <th className="text-right p-2 font-arabic">الرصيد</th>
                          <th className="text-right p-2 font-arabic">نسبة الدفع</th>
                          <th className="text-right p-2 font-arabic">المخاطر</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(riskData.customers || []).map((c: any) => (
                          <tr key={c.customer_id} className="border-b">
                            <td className="p-2 font-arabic">{c.customer_name}</td>
                            <td className="p-2">{c.invoice_count}</td>
                            <td className="p-2">{formatCurrency(c.total_amount, 'YER_N', 'ar')}</td>
                            <td className="p-2 text-destructive">{formatCurrency(c.balance, 'YER_N', 'ar')}</td>
                            <td className="p-2">
                              <div className="flex items-center gap-2">
                                <div className="w-16 h-2 bg-muted rounded-full overflow-hidden">
                                  <div className={`h-full rounded-full ${c.payment_ratio >= 90 ? 'bg-green-500' : c.payment_ratio >= 70 ? 'bg-yellow-500' : c.payment_ratio >= 50 ? 'bg-orange-500' : 'bg-red-500'}`} style={{ width: `${c.payment_ratio}%` }} />
                                </div>
                                <span className="text-xs">{c.payment_ratio}%</span>
                              </div>
                            </td>
                            <td className="p-2">
                              <Badge variant={c.risk_level === 'low' ? 'success' : c.risk_level === 'medium' ? 'warning' : c.risk_level === 'high' ? 'destructive' : 'destructive'}>
                                {riskLabels[c.risk_level]}
                              </Badge>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
