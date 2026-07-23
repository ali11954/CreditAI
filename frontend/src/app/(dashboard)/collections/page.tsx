'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Plus, Download, MoreHorizontal, Phone, Mail, FileText, FileSpreadsheet, Upload, Loader2, CreditCard, DollarSign } from 'lucide-react';
import { ColumnDef } from '@tanstack/react-table';
import { toast } from 'sonner';
import api from '@/lib/api';
import { formatCurrency } from '@/components/ui/currency-select';
import { CustomerSelect } from '@/components/ui/customer-select';

export default function CollectionsPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [activityDialogOpen, setActivityDialogOpen] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState<any>(null);
  const [activityType, setActivityType] = useState('payment');
  const [activityData, setActivityData] = useState({
    amount: '',
    notes: '',
    next_action: '',
    next_action_date: '',
  });

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, page_size: 10 };
      if (search) params.search = search;
      if (statusFilter !== 'all') params.status = statusFilter;
      const res = await api.get('/collections/sales-invoices', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل بيانات التحصيل');
    } finally {
      setLoading(false);
    }
  }, [page, search, statusFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleAddActivity = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedInvoice) return;
    try {
      const payload: any = {
        customer_id: selectedInvoice.customer_id,
        invoice_id: selectedInvoice.id,
        activity_type: activityType,
        amount: parseFloat(activityData.amount) || 0,
        notes: activityData.notes,
        next_action: activityData.next_action,
        next_action_date: activityData.next_action_date || undefined,
      };

      await api.post('/collections/activities', payload);
      toast.success('تم إضافة النشاط بنجاح');
      setActivityDialogOpen(false);
      setSelectedInvoice(null);
      setActivityData({ amount: '', notes: '', next_action: '', next_action_date: '' });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleExport = async (format: 'excel' | 'pdf') => {
    try {
      const res = await api.post(`/export/${format}`, {
        data,
        columns: ['customer_name', 'invoice_number', 'amount', 'total_amount', 'paid_amount', 'balance', 'due_date', 'status'],
        filename: 'collections',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `collections.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const handleExcelUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      const formDataObj = new FormData();
      formDataObj.append('file', file);
      await api.post('/collections/upload-excel', formDataObj, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      toast.success('تم رفع الملف بنجاح');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء رفع الملف');
    }
  };

  const statusLabels: Record<string, string> = {
    draft: 'مسودة', sent: 'مرسلة', paid: 'مدفوعة', overdue: 'متأخرة', cancelled: 'ملغاة',
  };
  const statusVariants: Record<string, any> = {
    draft: 'secondary', sent: 'info', paid: 'success', overdue: 'destructive', cancelled: 'warning',
  };

  const columns: ColumnDef<any>[] = [
    { accessorKey: 'customer_name', header: 'العميل', cell: ({ row }) => <span className="font-arabic font-medium">{row.getValue('customer_name') || '-'}</span> },
    { accessorKey: 'invoice_number', header: 'رقم الفاتورة', cell: ({ row }) => <span className="font-mono font-bold">{row.getValue('invoice_number')}</span> },
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
      accessorKey: 'due_date', header: 'تاريخ الاستحقاق',
      cell: ({ row }) => {
        const date = row.getValue('due_date') as string;
        return date ? new Date(date).toLocaleDateString('en-US') : '-';
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
      id: 'actions', header: 'الإجراءات',
      cell: ({ row }) => {
        const inv = row.original;
        const hasBalance = inv.balance > 0;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {hasBalance && (
                <>
                  <DropdownMenuItem onClick={() => { setSelectedInvoice(inv); setActivityType('payment'); setActivityData({ amount: String(inv.balance), notes: '', next_action: '', next_action_date: '' }); setActivityDialogOpen(true); }}>
                    <CreditCard className="mr-2 h-4 w-4" /> تسجيل دفعة
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => { setSelectedInvoice(inv); setActivityType('call'); setActivityData({ amount: '', notes: '', next_action: '', next_action_date: '' }); setActivityDialogOpen(true); }}>
                    <Phone className="mr-2 h-4 w-4" /> مكالمة تFollow-up
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => { setSelectedInvoice(inv); setActivityType('email'); setActivityData({ amount: '', notes: '', next_action: '', next_action_date: '' }); setActivityDialogOpen(true); }}>
                    <Mail className="mr-2 h-4 w-4" /> إرسال إشعار
                  </DropdownMenuItem>
                </>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  const totalAmount = data.reduce((sum, item) => sum + (item.amount || 0), 0);
  const totalPaid = data.reduce((sum, item) => sum + (item.paid_amount || 0), 0);
  const totalBalance = data.reduce((sum, item) => sum + (item.balance || 0), 0);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Collections"
        titleAr="التحصيل"
        description="Manage debt collection from sales invoices"
        descriptionAr="إدارة تحصيل الديون من فواتير المبيعات"
        actions={
          <div className="flex gap-2">
            <input ref={useRef<HTMLInputElement>(null)} type="file" accept=".xlsx,.xls" className="hidden" onChange={handleExcelUpload} />
            <Button variant="outline" className="font-arabic">
              <Upload className="ml-2 h-4 w-4" /> رفع Excel
            </Button>
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
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">إجمالي المبالغ</CardTitle></CardHeader>
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

      <DataTable columns={columns} data={data} searchKey="customer_name" searchPlaceholder="بحث بالعميل..." totalItems={total} loading={loading} onPageChange={setPage} />

      <Dialog open={activityDialogOpen} onOpenChange={setActivityDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>
              {activityType === 'payment' ? 'تسجيل دفعة' : activityType === 'call' ? 'مكالمة تFollow-up' : 'إرسال إشعار'}
              {selectedInvoice && ` - ${selectedInvoice.invoice_number}`}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleAddActivity} className="space-y-4">
            {activityType === 'payment' && (
              <div className="space-y-2">
                <Label>المبلغ المدفوع *</Label>
                <Input type="number" step="0.01" value={activityData.amount} onChange={(e) => setActivityData({ ...activityData, amount: e.target.value })} required />
                {selectedInvoice && (
                  <p className="text-sm text-muted-foreground font-arabic">الرصيد المتبقي: {formatCurrency(selectedInvoice.balance, selectedInvoice.currency_code || 'YER_N', 'ar')}</p>
                )}
              </div>
            )}
            <div className="space-y-2">
              <Label>ملاحظات</Label>
              <Textarea value={activityData.notes} onChange={(e) => setActivityData({ ...activityData, notes: e.target.value })} placeholder="أضف ملاحظات..." />
            </div>
            <div className="space-y-2">
              <Label>الإجراء التالي</Label>
              <Input value={activityData.next_action} onChange={(e) => setActivityData({ ...activityData, next_action: e.target.value })} placeholder="الإجراء التالي المطلوب" />
            </div>
            <div className="space-y-2">
              <Label>تاريخ الإجراء التالي</Label>
              <Input type="date" value={activityData.next_action_date} onChange={(e) => setActivityData({ ...activityData, next_action_date: e.target.value })} />
            </div>
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setActivityDialogOpen(false)}>إلغاء</Button>
              <Button type="submit">حفظ</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
