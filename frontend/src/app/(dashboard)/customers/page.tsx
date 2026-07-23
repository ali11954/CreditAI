'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Plus, MoreHorizontal, Eye, Edit, Trash2, FileSpreadsheet, Download, FileText } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { ColumnDef } from '@tanstack/react-table';
import Link from 'next/link';
import api from '@/lib/api';

const emptyForm = {
  name: '',
  name_ar: '',
  trade_name: '',
  business_type: '',
  tax_id: '',
  commercial_register: '',
  classification: '',
  risk_category: '',
  sales_region: '',
  status: 'active',
};

export default function CustomersPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<any>(null);
  const [deletingItem, setDeletingItem] = useState<any>(null);
  const [statusFilter, setStatusFilter] = useState('all');
  const [formData, setFormData] = useState(emptyForm);

  const columns: ColumnDef<any>[] = [
    {
      accessorKey: 'customer_code', header: 'كود العميل',
      cell: ({ row }) => <span className="font-mono text-xs">{row.getValue('customer_code')}</span>,
    },
    {
      accessorKey: 'name', header: 'اسم الشركة',
      cell: ({ row }) => (
        <Link href={`/customers/${row.original.id}`} className="font-medium hover:underline font-arabic">{row.getValue('name')}</Link>
      ),
    },
    { accessorKey: 'name_ar', header: 'الاسم بالعربي', cell: ({ row }) => <span className="font-arabic">{row.getValue('name_ar')}</span> },
    { accessorKey: 'business_type', header: 'نوع النشاط', cell: ({ row }) => <span className="font-arabic">{row.getValue('business_type')}</span> },
    { accessorKey: 'credit_score', header: 'الدرجة الائتمانية' },
    {
      accessorKey: 'status', header: 'الحالة',
      cell: ({ row }) => {
        const s = row.getValue('status') as string;
        const v: Record<string, 'success' | 'secondary' | 'destructive' | 'warning'> = { active: 'success', inactive: 'secondary', pending: 'warning', blocked: 'destructive' };
        const l: Record<string, string> = { active: 'نشط', inactive: 'غير نشط', pending: 'معلق', blocked: 'محظور' };
        return <Badge variant={v[s] || 'default'}>{l[s] || s}</Badge>;
      },
    },
    {
      id: 'actions', header: 'الإجراءات',
      cell: ({ row }) => {
        const c = row.original;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0"><MoreHorizontal className="h-4 w-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem asChild><Link href={`/customers/${c.id}`}><Eye className="mr-2 h-4 w-4" /> عرض</Link></DropdownMenuItem>
              <DropdownMenuItem onClick={() => openEditDialog(c)}><Edit className="mr-2 h-4 w-4" /> تعديل</DropdownMenuItem>
              <DropdownMenuItem className="text-destructive" onClick={() => openDeleteDialog(c)}><Trash2 className="mr-2 h-4 w-4" /> حذف</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, limit: 10 };
      if (search) params.search = search;
      if (statusFilter !== 'all') params.status = statusFilter;
      const res = await api.get('/customers', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل بيانات العملاء');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await api.put(`/customers/${editingItem.id}`, formData);
        toast.success('تم تحديث العميل بنجاح');
      } else {
        await api.post('/customers', formData);
        toast.success('تم إضافة العميل بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData(emptyForm);
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/customers/${deletingItem.id}`);
      toast.success('تم حذف العميل بنجاح');
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
        columns: ['customer_code', 'name', 'name_ar', 'business_type', 'tax_id', 'classification', 'risk_category', 'status'],
        filename: 'customers',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `customers.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const openEditDialog = (item: any) => {
    setEditingItem(item);
    setFormData({
      name: item.name || '',
      name_ar: item.name_ar || '',
      trade_name: item.trade_name || '',
      business_type: item.business_type || '',
      tax_id: item.tax_id || '',
      commercial_register: item.commercial_register || '',
      classification: item.classification || '',
      risk_category: item.risk_category || '',
      sales_region: item.sales_region || '',
      status: item.status || 'active',
    });
    setDialogOpen(true);
  };

  const openDeleteDialog = (item: any) => {
    setDeletingItem(item);
    setDeleteOpen(true);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Customers"
        titleAr="العملاء"
        description="Manage customer accounts and profiles"
        descriptionAr="إدارة حسابات العملاء والملفات الشخصية"
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
            <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData(emptyForm); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> عميل جديد
            </Button>
          </div>
        }
      />

      <div className="flex gap-2 mb-4">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[180px] font-arabic">
            <SelectValue placeholder="فلترة بالحالة" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">جميع الحالات</SelectItem>
            <SelectItem value="active">نشط</SelectItem>
            <SelectItem value="inactive">غير نشط</SelectItem>
            <SelectItem value="pending">معلق</SelectItem>
            <SelectItem value="blocked">محظور</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable
        columns={columns}
        data={data}
        searchKey="name"
        searchPlaceholder="بحث بالاسم..."
        totalItems={total}
        loading={loading}
        onPageChange={setPage}
      />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل العميل' : 'عميل جديد'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>اسم الشركة *</Label>
                <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required placeholder="اسم الشركة" />
              </div>
              <div className="space-y-2">
                <Label>الاسم بالعربي</Label>
                <Input value={formData.name_ar} onChange={(e) => setFormData({ ...formData, name_ar: e.target.value })} placeholder="اسم الشركة بالعربي" />
              </div>
              <div className="space-y-2">
                <Label>الاسم التجاري</Label>
                <Input value={formData.trade_name} onChange={(e) => setFormData({ ...formData, trade_name: e.target.value })} placeholder="الاسم التجاري" />
              </div>
              <div className="space-y-2">
                <Label>نوع النشاط</Label>
                <Select value={formData.business_type} onValueChange={(v) => setFormData({ ...formData, business_type: v })}>
                  <SelectTrigger><SelectValue placeholder="اختر نوع النشاط" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="technology">تقنية المعلومات</SelectItem>
                    <SelectItem value="manufacturing">التصنيع</SelectItem>
                    <SelectItem value="retail">التجزئة</SelectItem>
                    <SelectItem value="services">الخدمات</SelectItem>
                    <SelectItem value="construction">البناء</SelectItem>
                    <SelectItem value="trading">التجارة</SelectItem>
                    <SelectItem value="agriculture">الزراعة</SelectItem>
                    <SelectItem value="healthcare">الصحة</SelectItem>
                    <SelectItem value="education">التعليم</SelectItem>
                    <SelectItem value="other">أخرى</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>الرقم الضريبي</Label>
                <Input value={formData.tax_id} onChange={(e) => setFormData({ ...formData, tax_id: e.target.value })} placeholder="الرقم الضريبي" />
              </div>
              <div className="space-y-2">
                <Label>رقم السجل التجاري</Label>
                <Input value={formData.commercial_register} onChange={(e) => setFormData({ ...formData, commercial_register: e.target.value })} placeholder="رقم السجل التجاري" />
              </div>
              <div className="space-y-2">
                <Label>التصنيف</Label>
                <Select value={formData.classification} onValueChange={(v) => setFormData({ ...formData, classification: v })}>
                  <SelectTrigger><SelectValue placeholder="اختر التصنيف" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="platinum">بلاتيني</SelectItem>
                    <SelectItem value="gold">ذهبي</SelectItem>
                    <SelectItem value="silver">فضي</SelectItem>
                    <SelectItem value="bronze">برونزي</SelectItem>
                    <SelectItem value="standard">عادي</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>فئة المخاطرة</Label>
                <Select value={formData.risk_category} onValueChange={(v) => setFormData({ ...formData, risk_category: v })}>
                  <SelectTrigger><SelectValue placeholder="اختر فئة المخاطرة" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">منخفض</SelectItem>
                    <SelectItem value="medium">متوسط</SelectItem>
                    <SelectItem value="high">مرتفع</SelectItem>
                    <SelectItem value="critical">حرج</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>منطقة المبيعات</Label>
                <Input value={formData.sales_region} onChange={(e) => setFormData({ ...formData, sales_region: e.target.value })} placeholder="منطقة المبيعات" />
              </div>
              <div className="space-y-2">
                <Label>الحالة</Label>
                <Select value={formData.status} onValueChange={(v) => setFormData({ ...formData, status: v })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">نشط</SelectItem>
                    <SelectItem value="inactive">غير نشط</SelectItem>
                    <SelectItem value="pending">معلق</SelectItem>
                    <SelectItem value="blocked">محظور</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-4 border-t">
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
