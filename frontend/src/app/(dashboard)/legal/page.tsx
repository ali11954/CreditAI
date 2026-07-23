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
import { CustomerSelect } from '@/components/ui/customer-select';
import { ColumnDef } from '@tanstack/react-table';
import { toast } from 'sonner';
import api from '@/lib/api';

interface LegalCase {
  id: string;
  customer_id: string;
  customer_name?: string;
  case_type: string;
  court: string;
  amount: number;
  court_date: string;
  lawyer: string;
  status: string;
}

export default function LegalPage() {
  const [data, setData] = useState<LegalCase[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<LegalCase | null>(null);
  const [deletingItem, setDeletingItem] = useState<LegalCase | null>(null);
  const [formData, setFormData] = useState({
    customer_id: '',
    case_type: '',
    court: '',
    amount: '',
    court_date: '',
    lawyer: '',
  });

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, limit: 10 };
      if (search) params.search = search;
      const res = await api.get('/legal/cases', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل القضايا القانونية');
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
        await api.put(`/legal/cases/${editingItem.id}`, payload);
        toast.success('تم تحديث القضية بنجاح');
      } else {
        await api.post('/legal/cases', payload);
        toast.success('تم إنشاء القضية بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData({ customer_id: '', case_type: '', court: '', amount: '', court_date: '', lawyer: '' });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/legal/cases/${deletingItem.id}`);
      toast.success('تم حذف القضية بنجاح');
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
        columns: ['customer_name', 'case_type', 'court', 'amount', 'court_date', 'lawyer', 'status'],
        filename: 'legal_cases',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `legal_cases.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const columns: ColumnDef<LegalCase>[] = [
    { accessorKey: 'customer_name', header: 'العميل', cell: ({ row }) => <span className="font-arabic">{row.getValue('customer_name') || row.original.customer_id}</span> },
    { accessorKey: 'case_type', header: 'النوع', cell: ({ row }) => <span className="font-arabic">{row.getValue('case_type')}</span> },
    { accessorKey: 'court', header: 'المحكمة', cell: ({ row }) => <span className="font-arabic">{row.getValue('court')}</span> },
    {
      accessorKey: 'amount',
      header: 'المبلغ',
      cell: ({ row }) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', numberingSystem: 'latn' }).format(row.getValue('amount')),
    },
    { accessorKey: 'court_date', header: 'تاريخ الجلسة' },
    { accessorKey: 'lawyer', header: 'المحامي', cell: ({ row }) => <span className="font-arabic">{row.getValue('lawyer')}</span> },
    {
      accessorKey: 'status',
      header: 'الحالة',
      cell: ({ row }) => {
        const status = row.getValue('status') as string;
        const labels: Record<string, string> = { filed: 'مقدم', hearing: 'سماع', judgment: 'حكم', enforced: 'منفذ' };
        return <Badge variant={status === 'enforced' ? 'success' : 'warning'}>{labels[status] || status}</Badge>;
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
            <DropdownMenuItem onClick={() => { setEditingItem(row.original); setFormData({ customer_id: row.original.customer_id, case_type: row.original.case_type, court: row.original.court, amount: String(row.original.amount), court_date: row.original.court_date, lawyer: row.original.lawyer }); setDialogOpen(true); }}>
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
        title="Legal"
        titleAr="الإجراءات القانونية"
        description="Manage legal actions and cases"
        descriptionAr="إدارة الإجراءات والقضايا القانونية"
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
            <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData({ customer_id: '', case_type: '', court: '', amount: '', court_date: '', lawyer: '' }); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> إجراء جديد
            </Button>
          </div>
        }
      />

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">القضايا النشطة</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold">{data.filter(item => item.status !== 'enforced').length}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">إجمالي المبالغ</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold text-destructive">$ {(data.reduce((sum, item) => sum + (item.amount || 0), 0) / 1000000).toFixed(1)}M</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">جلسات قادمة</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold text-yellow-600">{data.filter(item => item.status === 'hearing').length}</p></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm font-arabic">القضايا المنتهية</CardTitle></CardHeader>
          <CardContent><p className="text-2xl font-bold text-green-600">{data.filter(item => item.status === 'enforced').length}</p></CardContent>
        </Card>
      </div>

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable columns={columns} data={data} totalItems={total} loading={loading} onPageChange={setPage} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل القضية' : 'قضية جديدة'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>العميل *</Label>
              <CustomerSelect value={formData.customer_id} onChange={(v) => setFormData({ ...formData, customer_id: v })} />
            </div>
            <div className="space-y-2">
              <Label>نوع القضية</Label>
              <Input value={formData.case_type} onChange={(e) => setFormData({ ...formData, case_type: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>المحكمة</Label>
              <Input value={formData.court} onChange={(e) => setFormData({ ...formData, court: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>المبلغ</Label>
              <Input type="number" value={formData.amount} onChange={(e) => setFormData({ ...formData, amount: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>تاريخ الجلسة</Label>
              <Input type="date" value={formData.court_date} onChange={(e) => setFormData({ ...formData, court_date: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>المحامي</Label>
              <Input value={formData.lawyer} onChange={(e) => setFormData({ ...formData, lawyer: e.target.value })} />
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
