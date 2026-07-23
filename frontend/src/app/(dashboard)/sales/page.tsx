'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import {
  Plus, MoreHorizontal, Eye, Edit, Trash2, Download, FileText,
  FileSpreadsheet, Upload, Loader2, ShoppingCart,
} from 'lucide-react';
import { ColumnDef } from '@tanstack/react-table';
import { toast } from 'sonner';
import api from '@/lib/api';
import { CurrencySelect, formatCurrency } from '@/components/ui/currency-select';
import { CustomerSelect } from '@/components/ui/customer-select';

export default function SalesPage() {
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
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [formData, setFormData] = useState({
    invoice_number: '',
    customer_id: '',
    invoice_date: '',
    due_date: '',
    amount: '',
    tax_amount: '0',
    discount_amount: '0',
    currency_id: '',
    status: 'draft',
    notes: '',
    product_type: '',
    quantity_tons: '',
  });

  const statusLabels: Record<string, string> = {
    draft: 'مسودة', sent: 'مرسلة', paid: 'مدفوعة', overdue: 'متأخرة', cancelled: 'ملغاة',
  };
  const statusVariants: Record<string, any> = {
    draft: 'secondary', sent: 'info', paid: 'success', overdue: 'destructive', cancelled: 'warning',
  };

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, page_size: 10 };
      if (search) params.search = search;
      if (statusFilter !== 'all') params.status = statusFilter;
      const res = await api.get('/sales', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل فواتير المبيعات');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const amount = parseFloat(formData.amount) || 0;
      const tax = parseFloat(formData.tax_amount) || 0;
      const discount = parseFloat(formData.discount_amount) || 0;
      const totalAmount = amount + tax - discount;
      const payload: any = {
        invoice_number: formData.invoice_number,
        customer_id: formData.customer_id,
        invoice_date: formData.invoice_date,
        due_date: formData.due_date,
        amount,
        tax_amount: tax,
        discount_amount: discount,
        total_amount: totalAmount,
        paid_amount: 0,
        balance: totalAmount,
        status: formData.status,
        notes: formData.notes || undefined,
        product_type: formData.product_type || undefined,
        quantity_tons: formData.quantity_tons ? parseFloat(formData.quantity_tons) : undefined,
      };
      if (formData.currency_id) payload.currency_id = formData.currency_id;

      if (editingItem) {
        await api.put(`/sales/${editingItem.id}`, payload);
        toast.success('تم تحديث الفاتورة بنجاح');
      } else {
        await api.post('/sales', payload);
        toast.success('تم إنشاء الفاتورة بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      resetForm();
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/sales/${deletingItem.id}`);
      toast.success('تم حذف الفاتورة بنجاح');
      setDeleteOpen(false);
      setDeletingItem(null);
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحذف');
    }
  };

  const handleExcelUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const formDataObj = new FormData();
      formDataObj.append('file', file);
      await api.post('/sales/upload-excel', formDataObj, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('تم رفع الملف بنجاح');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء رفع الملف');
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleExport = async (format: 'excel' | 'pdf') => {
    try {
      const res = await api.post(`/export/${format}`, {
        data,
        columns: ['invoice_number', 'customer_id', 'product_type', 'quantity_tons', 'amount', 'tax_amount', 'total_amount', 'paid_amount', 'balance', 'status'],
        filename: 'sales_invoices',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `sales_invoices.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const resetForm = () => {
    setFormData({
      invoice_number: '', customer_id: '', invoice_date: '', due_date: '',
      amount: '', tax_amount: '0', discount_amount: '0', currency_id: '',
      status: 'draft', notes: '', product_type: '', quantity_tons: '',
    });
  };

  const openEditDialog = (item: any) => {
    setEditingItem(item);
    setFormData({
      invoice_number: item.invoice_number || '',
      customer_id: item.customer_id || '',
      invoice_date: item.invoice_date?.split('T')[0] || '',
      due_date: item.due_date?.split('T')[0] || '',
      amount: String(item.amount || ''),
      tax_amount: String(item.tax_amount || '0'),
      discount_amount: String(item.discount_amount || '0'),
      currency_id: item.currency_id || '',
      status: item.status || 'draft',
      notes: item.notes || '',
      product_type: item.product_type || '',
      quantity_tons: item.quantity_tons ? String(item.quantity_tons) : '',
    });
    setDialogOpen(true);
  };

  const columns: ColumnDef<any>[] = [
    { accessorKey: 'invoice_number', header: 'رقم الفاتورة', cell: ({ row }) => <span className="font-mono font-bold">{row.getValue('invoice_number')}</span> },
    { accessorKey: 'customer_name', header: 'العميل', cell: ({ row }) => <span className="font-arabic">{row.getValue('customer_name') || '-'}</span> },
    {
      accessorKey: 'amount', header: 'المبلغ',
      cell: ({ row }) => formatCurrency(row.getValue('amount'), row.original.currency_code || 'YER_N', 'ar'),
    },
    {
      accessorKey: 'total_amount', header: 'الإجمالي',
      cell: ({ row }) => formatCurrency(row.getValue('total_amount'), row.original.currency_code || 'YER_N', 'ar'),
    },
    {
      accessorKey: 'paid_amount', header: 'المدفوع',
      cell: ({ row }) => formatCurrency(row.getValue('paid_amount'), row.original.currency_code || 'YER_N', 'ar'),
    },
    {
      accessorKey: 'balance', header: 'الرصيد',
      cell: ({ row }) => {
        const balance = row.getValue('balance') as number;
        return <span className={balance > 0 ? 'text-destructive font-bold' : 'text-green-600'}>{formatCurrency(balance, row.original.currency_code || 'YER_N', 'ar')}</span>;
      },
    },
    {
      accessorKey: 'status', header: 'الحالة',
      cell: ({ row }) => {
        const s = row.getValue('status') as string;
        return <Badge variant={statusVariants[s] || 'default'}>{statusLabels[s] || s}</Badge>;
      },
    },
    {
      accessorKey: 'due_date', header: 'تاريخ الاستحقاق',
      cell: ({ row }) => {
        const date = row.getValue('due_date') as string;
        return date ? new Date(date).toLocaleDateString('en-US') : '-';
      },
    },
    {
      accessorKey: 'product_type', header: 'نوع البضاعة',
      cell: ({ row }) => <span className="font-arabic">{row.getValue('product_type') || '-'}</span>,
    },
    {
      accessorKey: 'quantity_tons', header: 'الكمية (طن)',
      cell: ({ row }) => {
        const qty = row.getValue('quantity_tons');
        return qty ? <span className="font-mono">{String(qty)} طن</span> : '-';
      },
    },
    {
      id: 'actions', header: 'الإجراءات',
      cell: ({ row }) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0"><MoreHorizontal className="h-4 w-4" /></Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => openEditDialog(row.original)}><Edit className="mr-2 h-4 w-4" /> تعديل</DropdownMenuItem>
            <DropdownMenuItem className="text-destructive" onClick={() => { setDeletingItem(row.original); setDeleteOpen(true); }}><Trash2 className="mr-2 h-4 w-4" /> حذف</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ];

  const totalAmount = data.reduce((sum, item) => sum + (parseFloat(item.total_amount) || 0), 0);
  const totalPaid = data.reduce((sum, item) => sum + (parseFloat(item.paid_amount) || 0), 0);
  const totalBalance = data.reduce((sum, item) => sum + (parseFloat(item.balance) || 0), 0);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Sales"
        titleAr="المبيعات"
        description="Manage sales invoices"
        descriptionAr="إدارة فواتير المبيعات"
        actions={
          <div className="flex gap-2">
            <input ref={fileInputRef} type="file" accept=".xlsx,.xls" className="hidden" onChange={handleExcelUpload} />
            <Button variant="outline" className="font-arabic" onClick={() => fileInputRef.current?.click()} disabled={uploading}>
              {uploading ? <Loader2 className="ml-2 h-4 w-4 animate-spin" /> : <Upload className="ml-2 h-4 w-4" />}
              {uploading ? 'جاري الرفع...' : 'رفع Excel'}
            </Button>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="font-arabic"><Download className="ml-2 h-4 w-4" /> تصدير</Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem onClick={() => handleExport('excel')}><FileSpreadsheet className="mr-2 h-4 w-4" /> Excel</DropdownMenuItem>
                <DropdownMenuItem onClick={() => handleExport('pdf')}><FileText className="mr-2 h-4 w-4" /> PDF</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
            <Button className="font-arabic" onClick={() => { setEditingItem(null); resetForm(); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> فاتورة جديدة
            </Button>
          </div>
        }
      />

      <div className="flex gap-2 mb-4">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[180px] font-arabic"><SelectValue placeholder="فلترة بالحالة" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">جميع الحالات</SelectItem>
            <SelectItem value="draft">مسودة</SelectItem>
            <SelectItem value="sent">مرسلة</SelectItem>
            <SelectItem value="paid">مدفوعة</SelectItem>
            <SelectItem value="overdue">متأخرة</SelectItem>
            <SelectItem value="cancelled">ملغاة</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">إجمالي الفواتير</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold">{formatCurrency(totalAmount, 'YER_N', 'ar')}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">المدفوع</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold text-green-600">{formatCurrency(totalPaid, 'YER_N', 'ar')}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">الرصيد المتبقي</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold text-destructive">{formatCurrency(totalBalance, 'YER_N', 'ar')}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">عدد الفواتير</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold">{total}</p></CardContent>
        </Card>
      </div>

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable columns={columns} data={data} searchKey="invoice_number" searchPlaceholder="بحث برقم الفاتورة..." totalItems={total} loading={loading} onPageChange={setPage} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل الفاتورة' : 'فاتورة جديدة'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>رقم الفاتورة *</Label>
                <Input value={formData.invoice_number} onChange={(e) => setFormData({ ...formData, invoice_number: e.target.value })} required placeholder="INV-001" />
              </div>
              <div className="space-y-2">
                <Label>العميل *</Label>
                <CustomerSelect value={formData.customer_id} onChange={(v) => setFormData({ ...formData, customer_id: v })} />
              </div>
              <div className="space-y-2">
                <Label>تاريخ الفاتورة *</Label>
                <Input type="date" value={formData.invoice_date} onChange={(e) => setFormData({ ...formData, invoice_date: e.target.value })} required />
              </div>
              <div className="space-y-2">
                <Label>تاريخ الاستحقاق *</Label>
                <Input type="date" value={formData.due_date} onChange={(e) => setFormData({ ...formData, due_date: e.target.value })} required />
              </div>
              <div className="space-y-2">
                <Label>المبلغ *</Label>
                <Input type="number" step="0.01" value={formData.amount} onChange={(e) => setFormData({ ...formData, amount: e.target.value })} required />
              </div>
              <div className="space-y-2">
                <Label>العملة</Label>
                <CurrencySelect value={formData.currency_id} onChange={(v) => setFormData({ ...formData, currency_id: v })} />
              </div>
              <div className="space-y-2">
                <Label>الضريبة</Label>
                <Input type="number" step="0.01" value={formData.tax_amount} onChange={(e) => setFormData({ ...formData, tax_amount: e.target.value })} />
              </div>
              <div className="space-y-2">
                <Label>الخصم</Label>
                <Input type="number" step="0.01" value={formData.discount_amount} onChange={(e) => setFormData({ ...formData, discount_amount: e.target.value })} />
              </div>
              <div className="space-y-2">
                <Label>الحالة</Label>
                <Select value={formData.status} onValueChange={(v) => setFormData({ ...formData, status: v })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="draft">مسودة</SelectItem>
                    <SelectItem value="sent">مرسلة</SelectItem>
                    <SelectItem value="paid">مدفوعة</SelectItem>
                    <SelectItem value="overdue">متأخرة</SelectItem>
                    <SelectItem value="cancelled">ملغاة</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>نوع البضاعة</Label>
                <Input value={formData.product_type} onChange={(e) => setFormData({ ...formData, product_type: e.target.value })} placeholder="نوع البضاعة" />
              </div>
              <div className="space-y-2">
                <Label>الكمية بالطن</Label>
                <Input type="number" step="0.01" value={formData.quantity_tons} onChange={(e) => setFormData({ ...formData, quantity_tons: e.target.value })} placeholder="0.00" />
              </div>
            </div>
            <div className="space-y-2">
              <Label>ملاحظات</Label>
              <Input value={formData.notes} onChange={(e) => setFormData({ ...formData, notes: e.target.value })} placeholder="ملاحظات إضافية" />
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
