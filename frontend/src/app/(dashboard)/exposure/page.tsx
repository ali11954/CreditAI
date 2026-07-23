'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Plus, Download, MoreHorizontal, Edit, Trash2, FileText, FileSpreadsheet, Loader2 } from 'lucide-react';
import { DataTable } from '@/components/data-table/data-table';
import { CustomerSelect } from '@/components/ui/customer-select';
import { ColumnDef } from '@tanstack/react-table';
import dynamic from 'next/dynamic';
import { toast } from 'sonner';
import api from '@/lib/api';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface Exposure {
  id: string;
  customer_id: string;
  customer_name?: string;
  exposure_type: string;
  amount: number;
  currency: string;
  risk_level: string;
  status: string;
}

export default function ExposurePage() {
  const [data, setData] = useState<Exposure[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Exposure | null>(null);
  const [deletingItem, setDeletingItem] = useState<Exposure | null>(null);
  const [formData, setFormData] = useState({
    customer_id: '',
    exposure_type: 'credit',
    amount: '',
    currency: 'ILS',
    risk_level: 'low',
  });

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, limit: 10 };
      if (search) params.search = search;
      const res = await api.get('/exposure', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل بيانات التعرض');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = { ...formData, amount: parseFloat(formData.amount) };
      if (editingItem) {
        await api.put(`/exposure/${editingItem.id}`, payload);
        toast.success('تم تحديث التعرض بنجاح');
      } else {
        await api.post('/exposure', payload);
        toast.success('تم إنشاء التعرض بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData({ customer_id: '', exposure_type: 'credit', amount: '', currency: 'ILS', risk_level: 'low' });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/exposure/${deletingItem.id}`);
      toast.success('تم حذف التعرض بنجاح');
      setDeleteOpen(false);
      setDeletingItem(null);
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحذف');
    }
  };

  const handleExport = async (format: 'excel' | 'pdf') => {
    try {
      const res = await api.post(`/export/${format}`, {
        data,
        columns: ['customer_name', 'exposure_type', 'amount', 'currency', 'risk_level', 'status'],
        filename: 'exposure',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `exposure.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const totalExposure = data.reduce((sum, item) => sum + (item.amount || 0), 0);
  const riskDistribution = data.reduce((acc, item) => {
    acc[item.risk_level] = (acc[item.risk_level] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const pieOptions = {
    chart: { type: 'pie' as const },
    labels: ['منخفض', 'متوسط', 'مرتفع', 'حرج'],
    colors: ['#22c55e', '#f59e0b', '#ef4444', '#7c3aed'],
  };

  const columns: ColumnDef<Exposure>[] = [
    { accessorKey: 'customer_name', header: 'العميل', cell: ({ row }) => <span className="font-arabic">{row.getValue('customer_name') || row.original.customer_id}</span> },
    { accessorKey: 'exposure_type', header: 'النوع', cell: ({ row }) => <span className="font-arabic">{row.getValue('exposure_type')}</span> },
    {
      accessorKey: 'amount',
      header: 'المبلغ',
      cell: ({ row }) => new Intl.NumberFormat('en-US', { style: 'currency', currency: row.original.currency || 'USD', numberingSystem: 'latn' }).format(row.getValue('amount')),
    },
    {
      accessorKey: 'risk_level',
      header: 'مستوى المخاطرة',
      cell: ({ row }) => {
        const risk = row.getValue('risk_level') as string;
        const variants: Record<string, 'success' | 'warning' | 'destructive'> = { low: 'success', medium: 'warning', high: 'destructive', critical: 'destructive' };
        const labels: Record<string, string> = { low: 'منخفض', medium: 'متوسط', high: 'مرتفع', critical: 'حرج' };
        return <Badge variant={variants[risk] || 'default'}>{labels[risk] || risk}</Badge>;
      },
    },
    {
      accessorKey: 'status',
      header: 'الحالة',
      cell: ({ row }) => {
        const status = row.getValue('status') as string;
        return <Badge variant={status === 'active' ? 'success' : 'secondary'}>{status === 'active' ? 'نشط' : 'غير نشط'}</Badge>;
      },
    },
    {
      id: 'actions',
      header: 'الإجراءات',
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => { setEditingItem(row.original); setFormData({ customer_id: row.original.customer_id, exposure_type: row.original.exposure_type, amount: String(row.original.amount), currency: row.original.currency, risk_level: row.original.risk_level }); setDialogOpen(true); }}>
              <Edit className="mr-2 h-4 w-4" /> تعديل
            </DropdownMenuItem>
            <DropdownMenuItem className="text-destructive" onClick={() => { setDeletingItem(row.original); setDeleteOpen(true); }}>
              <Trash2 className="mr-2 h-4 w-4" /> حذف
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Exposure & Risk"
        titleAr="النفاذ والمخاطر"
        description="Risk exposure analysis"
        descriptionAr="تحليل المخاطر والنفاذ"
        actions={
          <div className="flex gap-2">
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
            <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData({ customer_id: '', exposure_type: 'credit', amount: '', currency: 'ILS', risk_level: 'low' }); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> إضافة تعرض
            </Button>
          </div>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <p className="text-2xl font-bold">$ {(totalExposure / 1000000).toFixed(1)}M</p>
            <p className="text-sm text-muted-foreground font-arabic">إجمالي النزاع</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-2xl font-bold">{data.filter(item => item.status === 'active').length}</p>
            <p className="text-sm text-muted-foreground font-arabic">الحسابات النشطة</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-2xl font-bold text-yellow-600">{riskDistribution.high || 0}</p>
            <p className="text-sm text-muted-foreground font-arabic">مخاطر مرتفعة</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-2xl font-bold text-green-600">{riskDistribution.low || 0}</p>
            <p className="text-sm text-muted-foreground font-arabic">مخاطر منخفضة</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="font-arabic">توزيع المخاطر</CardTitle>
          </CardHeader>
          <CardContent>
            <Chart options={pieOptions} series={[riskDistribution.low || 0, riskDistribution.medium || 0, riskDistribution.high || 0, riskDistribution.critical || 0]} type="pie" height={300} />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="font-arabic">قائمة التعرض</CardTitle>
          </CardHeader>
          <CardContent>
            <DataTable columns={columns} data={data} totalItems={total} loading={loading} onPageChange={setPage} />
          </CardContent>
        </Card>
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل التعرض' : 'تعرض جديد'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>العميل *</Label>
              <CustomerSelect value={formData.customer_id} onChange={(v) => setFormData({ ...formData, customer_id: v })} />
            </div>
            <div className="space-y-2">
              <Label>نوع التعرض</Label>
              <Select value={formData.exposure_type} onValueChange={(v) => setFormData({ ...formData, exposure_type: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="credit">ائتمان</SelectItem>
                  <SelectItem value="guarantee">ضمان</SelectItem>
                  <SelectItem value="market">سوق</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>المبلغ</Label>
              <Input type="number" value={formData.amount} onChange={(e) => setFormData({ ...formData, amount: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>العملة</Label>
              <Select value={formData.currency} onValueChange={(v) => setFormData({ ...formData, currency: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="ILS">شيكل</SelectItem>
                  <SelectItem value="USD">دولار</SelectItem>
                  <SelectItem value="EUR">يورو</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>مستوى المخاطرة</Label>
              <Select value={formData.risk_level} onValueChange={(v) => setFormData({ ...formData, risk_level: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">منخفض</SelectItem>
                  <SelectItem value="medium">متوسط</SelectItem>
                  <SelectItem value="high">مرتفع</SelectItem>
                  <SelectItem value="critical">حرج</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>إلغاء</Button>
              <Button type="submit">{editingItem ? 'تحديث' : 'حفظ'}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      <AlertDialog open={deleteOpen} onOpenChange={setDeleteOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle className="font-arabic">هل أنت متأكد؟</AlertDialogTitle>
            <AlertDialogDescription className="font-arabic">لا يمكن التراجع عن هذا الإجراء.</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-destructive text-destructive-foreground">حذف</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
