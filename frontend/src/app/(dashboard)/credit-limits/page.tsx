'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Plus, Download, MoreHorizontal, Eye, Edit, Trash2, FileText, FileSpreadsheet } from 'lucide-react';
import { ColumnDef } from '@tanstack/react-table';
import { Progress } from '@/components/ui/progress';
import { toast } from 'sonner';
import api from '@/lib/api';
import { CurrencySelect, formatCurrency } from '@/components/ui/currency-select';
import { CustomerSelect } from '@/components/ui/customer-select';

interface CreditLimit {
  id: string;
  customer_id: string;
  customer_name?: string;
  limit_type: string;
  amount: number;
  utilized_amount: number;
  available_amount: number;
  currency_id?: string;
  currency_code?: string;
  start_date: string;
  end_date: string;
  status: string;
}

export default function CreditLimitsPage() {
  const [data, setData] = useState<CreditLimit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<CreditLimit | null>(null);
  const [deletingItem, setDeletingItem] = useState<CreditLimit | null>(null);
  const [formData, setFormData] = useState({
    customer_id: '',
    limit_type: 'credit_line',
    amount: '',
    currency_id: '',
    start_date: '',
    end_date: '',
  });

  const totalLimits = data.reduce((sum, item) => sum + (item.amount || 0), 0);
  const usedLimits = data.reduce((sum, item) => sum + (item.utilized_amount || 0), 0);
  const availableLimits = data.reduce((sum, item) => sum + (item.available_amount || 0), 0);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, limit: 10 };
      if (search) params.search = search;
      const res = await api.get('/credit-limits', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل حدود الائتمان');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload: any = {
        customer_id: formData.customer_id,
        limit_type: formData.limit_type,
        amount: parseFloat(formData.amount),
        available_amount: parseFloat(formData.amount),
        start_date: formData.start_date || undefined,
        end_date: formData.end_date || undefined,
      };
      if (formData.currency_id) payload.currency_id = formData.currency_id;
      if (editingItem) {
        await api.put(`/credit-limits/${editingItem.id}`, payload);
        toast.success('تم تحديث الحد بنجاح');
      } else {
        await api.post('/credit-limits', payload);
        toast.success('تم إنشاء الحد بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData({ customer_id: '', limit_type: 'credit_line', amount: '', currency_id: '', start_date: '', end_date: '' });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/credit-limits/${deletingItem.id}`);
      toast.success('تم حذف الحد بنجاح');
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
        columns: ['customer_name', 'limit_type', 'amount', 'utilized_amount', 'available_amount', 'status'],
        filename: 'credit_limits',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `credit_limits.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const columns: ColumnDef<CreditLimit>[] = [
    { accessorKey: 'customer_name', header: 'العميل', cell: ({ row }) => <span className="font-arabic">{row.getValue('customer_name') || row.original.customer_id}</span> },
    {
      accessorKey: 'amount',
      header: 'الحد الكلي',
      cell: ({ row }) => formatCurrency(row.getValue('amount'), row.original.currency_code || 'YER_N', 'ar'),
    },
    {
      accessorKey: 'utilized_amount',
      header: 'المستخدم',
      cell: ({ row }) => formatCurrency(row.getValue('utilized_amount'), row.original.currency_code || 'YER_N', 'ar'),
    },
    {
      accessorKey: 'available_amount',
      header: 'المتاح',
      cell: ({ row }) => formatCurrency(row.getValue('available_amount'), row.original.currency_code || 'YER_N', 'ar'),
    },
    {
      id: 'utilization',
      header: 'الاستهلاك',
      cell: ({ row }) => {
        const used = row.original.utilized_amount || 0;
        const total = row.original.amount || 0;
        const percent = total > 0 ? Math.round((used / total) * 100) : 0;
        return (
          <div className="flex items-center gap-2">
            <Progress value={percent} className="w-20 h-2" />
            <span className="text-sm">{percent}%</span>
          </div>
        );
      },
    },
    {
      accessorKey: 'status',
      header: 'الحالة',
      cell: ({ row }) => {
        const status = row.getValue('status') as string;
        const labels: Record<string, string> = { active: 'نشط', suspended: 'معلق', expired: 'منتهي' };
        return <Badge variant={status === 'active' ? 'success' : 'secondary'}>{labels[status] || status}</Badge>;
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
            <DropdownMenuItem onClick={() => { setEditingItem(row.original); setFormData({ customer_id: row.original.customer_id, limit_type: row.original.limit_type, amount: String(row.original.amount), currency_id: row.original.currency_id || '', start_date: row.original.start_date, end_date: row.original.end_date }); setDialogOpen(true); }}>
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
        title="Credit Limits"
        titleAr="حدود الائتمان"
        description="Manage customer credit limits"
        descriptionAr="إدارة حدود الائتمان للعملاء"
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
            <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData({ customer_id: '', limit_type: 'credit_line', amount: '', currency_id: '', start_date: '', end_date: '' }); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> تحديد حد جديد
            </Button>
          </div>
        }
      />

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-arabic">إجمالي الحدود</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{formatCurrency(totalLimits, 'YER_N', 'ar')}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-arabic">المستخدم</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{formatCurrency(usedLimits, 'YER_N', 'ar')}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-arabic">المتاح</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-green-600">{formatCurrency(availableLimits, 'YER_N', 'ar')}</p>
          </CardContent>
        </Card>
      </div>

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable columns={columns} data={data} totalItems={total} loading={loading} onPageChange={setPage} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل الحد' : 'تحديد حد جديد'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>العميل *</Label>
              <CustomerSelect value={formData.customer_id} onChange={(v) => setFormData({ ...formData, customer_id: v })} />
            </div>
            <div className="space-y-2">
              <Label>نوع الحد</Label>
              <Select value={formData.limit_type} onValueChange={(v) => setFormData({ ...formData, limit_type: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="credit_line">خط ائتمان</SelectItem>
                  <SelectItem value="overdraft">سحوبCESS</SelectItem>
                  <SelectItem value="guarantee">ضمان</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>المبلغ</Label>
              <Input type="number" step="0.01" value={formData.amount} onChange={(e) => setFormData({ ...formData, amount: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>العملة</Label>
              <CurrencySelect value={formData.currency_id} onChange={(v) => setFormData({ ...formData, currency_id: v })} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>تاريخ البداية</Label>
                <Input type="date" value={formData.start_date} onChange={(e) => setFormData({ ...formData, start_date: e.target.value })} />
              </div>
              <div className="space-y-2">
                <Label>تاريخ النهاية</Label>
                <Input type="date" value={formData.end_date} onChange={(e) => setFormData({ ...formData, end_date: e.target.value })} />
              </div>
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
