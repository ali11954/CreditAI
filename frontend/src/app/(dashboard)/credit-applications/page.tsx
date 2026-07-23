'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Plus, ArrowUpDown, MoreHorizontal, Eye, Check, X, Download, FileText, FileSpreadsheet } from 'lucide-react';
import { ColumnDef } from '@tanstack/react-table';
import Link from 'next/link';
import { toast } from 'sonner';
import api from '@/lib/api';
import { CurrencySelect, formatCurrency } from '@/components/ui/currency-select';
import { CustomerSelect } from '@/components/ui/customer-select';

interface Application {
  id: string;
  customer_id: string;
  customer_name?: string;
  application_type: string;
  requested_amount: number;
  currency_id?: string;
  currency_code?: string;
  purpose: string;
  status: string;
  risk_level?: string;
  created_at: string;
}

const statusLabels: Record<string, string> = {
  pending: 'معلق',
  approved: 'مقبول',
  rejected: 'مرفوض',
  under_review: 'قيد المراجعة',
  draft: 'مسودة',
};

const statusVariants: Record<string, any> = {
  pending: 'warning',
  approved: 'success',
  rejected: 'destructive',
  under_review: 'info',
  draft: 'secondary',
};

const riskLabels: Record<string, string> = { low: 'منخفض', medium: 'متوسط', high: 'مرتفع', critical: 'حرج' };

export default function CreditApplicationsPage() {
  const [data, setData] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Application | null>(null);
  const [deletingItem, setDeletingItem] = useState<Application | null>(null);
  const [statusFilter, setStatusFilter] = useState('all');
  const [formData, setFormData] = useState({
    customer_id: '',
    application_type: 'credit_line',
    requested_amount: '',
    currency_id: '',
    purpose: '',
  });

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, limit: 10 };
      if (search) params.search = search;
      if (statusFilter !== 'all') params.status = statusFilter;
      const res = await api.get('/credit-applications', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل طلبات الائتمان');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleStatusChange = async (id: string, status: string) => {
    try {
      await api.put(`/credit-applications/${id}`, { status });
      toast.success('تم تحديث الحالة بنجاح');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء تحديث الحالة');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload: any = {
        customer_id: formData.customer_id,
        application_type: formData.application_type,
        requested_amount: parseFloat(formData.requested_amount),
        purpose: formData.purpose || undefined,
      };
      if (formData.currency_id) payload.currency_id = formData.currency_id;
      if (editingItem) {
        await api.put(`/credit-applications/${editingItem.id}`, payload);
        toast.success('تم تحديث الطلب بنجاح');
      } else {
        await api.post('/credit-applications', payload);
        toast.success('تم إنشاء الطلب بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData({ customer_id: '', application_type: 'credit_line', requested_amount: '', currency_id: '', purpose: '' });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/credit-applications/${deletingItem.id}`);
      toast.success('تم حذف الطلب بنجاح');
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
        columns: ['customer_name', 'application_type', 'requested_amount', 'purpose', 'status', 'created_at'],
        filename: 'credit_applications',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `credit_applications.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const columns: ColumnDef<Application>[] = [
    {
      accessorKey: 'customer_name',
      header: ({ column }) => (
        <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}>
          العميل <ArrowUpDown className="mr-2 h-4 w-4" />
        </Button>
      ),
      cell: ({ row }) => (
        <Link href={`/credit-applications/${row.original.id}`} className="font-medium hover:underline font-arabic">
          {row.getValue('customer_name') || row.original.customer_id}
        </Link>
      ),
    },
    {
      accessorKey: 'application_type',
      header: 'النوع',
      cell: ({ row }) => {
        const types: Record<string, string> = { credit_line: 'خط ائتمان', loan: 'قرض', guarantee: 'ضمان' };
        return <span className="font-arabic">{types[row.getValue('application_type') as string] || row.getValue('application_type')}</span>;
      },
    },
    {
      accessorKey: 'requested_amount',
      header: 'المبلغ',
      cell: ({ row }) => formatCurrency(row.getValue('requested_amount'), row.original.currency_code || 'YER_N', 'ar'),
    },
    {
      accessorKey: 'status',
      header: 'الحالة',
      cell: ({ row }) => {
        const status = row.getValue('status') as string;
        return <Badge variant={statusVariants[status] || 'default'}>{statusLabels[status] || status}</Badge>;
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
            <DropdownMenuItem asChild>
              <Link href={`/credit-applications/${row.original.id}`}>
                <Eye className="mr-2 h-4 w-4" /> عرض
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => { setEditingItem(row.original); setFormData({ customer_id: row.original.customer_id, application_type: row.original.application_type, requested_amount: String(row.original.requested_amount), currency_id: row.original.currency_id || '', purpose: row.original.purpose }); setDialogOpen(true); }}>
              <Check className="mr-2 h-4 w-4" /> تعديل
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => handleStatusChange(row.original.id, 'approved')}>
              <Check className="mr-2 h-4 w-4 text-green-500" /> موافقة
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => handleStatusChange(row.original.id, 'rejected')}>
              <X className="mr-2 h-4 w-4 text-destructive" /> رفض
            </DropdownMenuItem>
            <DropdownMenuItem className="text-destructive" onClick={() => { setDeletingItem(row.original); setDeleteOpen(true); }}>
              <X className="mr-2 h-4 w-4" /> حذف
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Credit Applications"
        titleAr="طلبات الائتمان"
        description="Review and manage credit applications"
        descriptionAr="مراجعة وإدارة طلبات الائتمان"
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
            <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData({ customer_id: '', application_type: 'credit_line', requested_amount: '', currency_id: '', purpose: '' }); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> طلب جديد
            </Button>
          </div>
        }
      />

      <div className="flex gap-2 mb-4">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[180px] font-arabic"><SelectValue placeholder="فلترة بالحالة" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">جميع الحالات</SelectItem>
            <SelectItem value="pending">معلق</SelectItem>
            <SelectItem value="under_review">قيد المراجعة</SelectItem>
            <SelectItem value="approved">مقبول</SelectItem>
            <SelectItem value="rejected">مرفوض</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable columns={columns} data={data} searchKey="customer_name" searchPlaceholder="بحث بالعميل..." totalItems={total} loading={loading} onPageChange={setPage} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل الطلب' : 'طلب جديد'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>العميل *</Label>
              <CustomerSelect value={formData.customer_id} onChange={(v) => setFormData({ ...formData, customer_id: v })} />
            </div>
            <div className="space-y-2">
              <Label>نوع الطلب</Label>
              <Select value={formData.application_type} onValueChange={(v) => setFormData({ ...formData, application_type: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="credit_line">خط ائتمان</SelectItem>
                  <SelectItem value="loan">قرض</SelectItem>
                  <SelectItem value="guarantee">ضمان</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>المبلغ المطلوب</Label>
              <Input type="number" step="0.01" value={formData.requested_amount} onChange={(e) => setFormData({ ...formData, requested_amount: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>العملة</Label>
              <CurrencySelect value={formData.currency_id} onChange={(v) => setFormData({ ...formData, currency_id: v })} />
            </div>
            <div className="space-y-2">
              <Label>الغرض</Label>
              <Input value={formData.purpose} onChange={(e) => setFormData({ ...formData, purpose: e.target.value })} />
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
