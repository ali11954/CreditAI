'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { CheckCircle, AlertTriangle, Clock, FileText, Download, FileSpreadsheet, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/lib/api';

export default function CompliancePage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/compliance/cases');
      setItems(res.data.items || []);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل بيانات الامتثال');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleExport = async (format: 'excel' | 'pdf') => {
    try {
      const res = await api.post(`/export/${format}`, {
        data: items,
        columns: ['title', 'status', 'last_check', 'next_check'],
        filename: 'compliance',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `compliance.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const handleStatusUpdate = async (id: string, status: string) => {
    try {
      await api.put(`/compliance/cases/${id}`, { status });
      toast.success('تم تحديث الحالة بنجاح');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التحديث');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  const compliantCount = items.filter(item => item.status === 'compliant').length;
  const warningCount = items.filter(item => item.status === 'warning').length;
  const overdueCount = items.filter(item => item.status === 'overdue').length;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Compliance"
        titleAr="الامتثال"
        description="Regulatory compliance monitoring"
        descriptionAr="مراقبة الامتثال التنظيمي"
        actions={
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="font-arabic">
                <Download className="ml-2 h-4 w-4" /> تصدير
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => handleExport('excel')}>
                <FileSpreadsheet className="mr-2 h-4 w-4" /> Excel
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => handleExport('pdf')}>
                <FileText className="mr-2 h-4 w-4" /> PDF
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <CheckCircle className="h-8 w-8 text-green-500" />
              <div>
                <p className="text-2xl font-bold">{compliantCount}</p>
                <p className="text-sm text-muted-foreground font-arabic">متوافق</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <AlertTriangle className="h-8 w-8 text-yellow-500" />
              <div>
                <p className="text-2xl font-bold">{warningCount}</p>
                <p className="text-sm text-muted-foreground font-arabic">تحذير</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Clock className="h-8 w-8 text-blue-500" />
              <div>
                <p className="text-2xl font-bold">{overdueCount}</p>
                <p className="text-sm text-muted-foreground font-arabic">متأخر</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <FileText className="h-8 w-8 text-purple-500" />
              <div>
                <p className="text-2xl font-bold">{items.length}</p>
                <p className="text-sm text-muted-foreground font-arabic">إجمالي البنود</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="font-arabic">عناصر الامتثال</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {items.map((item) => (
              <div key={item.id} className="flex items-center justify-between rounded-md border p-4">
                <div className="flex items-center gap-3">
                  {item.status === 'compliant' ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <AlertTriangle className="h-5 w-5 text-yellow-500" />
                  )}
                  <div>
                    <p className="font-medium font-arabic">{item.title}</p>
                    <p className="text-sm text-muted-foreground font-arabic">
                      آخر فحص: {item.last_check} | الفحص القادم: {item.next_check}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={item.status === 'compliant' ? 'success' : item.status === 'warning' ? 'warning' : 'destructive'}>
                    {item.status === 'compliant' ? 'متوافق' : item.status === 'warning' ? 'تحذير' : 'متأخر'}
                  </Badge>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="sm">تحديث</Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                      <DropdownMenuItem onClick={() => handleStatusUpdate(item.id, 'compliant')}>متوافق</DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleStatusUpdate(item.id, 'warning')}>تحذير</DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleStatusUpdate(item.id, 'overdue')}>متأخر</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>
            ))}
            {items.length === 0 && (
              <p className="text-center text-muted-foreground font-arabic py-8">لا توجد عناصر امتثال</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
