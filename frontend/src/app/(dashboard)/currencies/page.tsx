'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Plus, MoreHorizontal, Edit, Trash2, DollarSign } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { ColumnDef } from '@tanstack/react-table';
import api from '@/lib/api';

export default function CurrenciesPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<any>(null);
  const [deletingItem, setDeletingItem] = useState<any>(null);
  const [formData, setFormData] = useState({
    code: '',
    name: '',
    name_ar: '',
    symbol: '',
    exchange_rate: '1.0',
    is_base: false,
    is_active: true,
  });

  const columns: ColumnDef<any>[] = [
    {
      accessorKey: 'code', header: 'الكود',
      cell: ({ row }) => <span className="font-mono font-bold">{row.getValue('code')}</span>,
    },
    {
      accessorKey: 'name', header: 'الاسم (إنجليزي)',
    },
    {
      accessorKey: 'name_ar', header: 'الاسم (عربي)',
      cell: ({ row }) => <span className="font-arabic">{row.getValue('name_ar')}</span>,
    },
    {
      accessorKey: 'symbol', header: 'الرمز',
      cell: ({ row }) => <span className="text-lg font-bold">{row.getValue('symbol')}</span>,
    },
    {
      accessorKey: 'exchange_rate', header: 'سعر الصرف',
      cell: ({ row }) => <span className="font-mono">{row.getValue('exchange_rate')}</span>,
    },
    {
      accessorKey: 'is_base', header: 'العملة الأساسية',
      cell: ({ row }) => {
        const isBase = row.getValue('is_base');
        return isBase ? <Badge variant="success">أساسية</Badge> : <Badge variant="secondary">فرعية</Badge>;
      },
    },
    {
      accessorKey: 'is_active', header: 'الحالة',
      cell: ({ row }) => {
        const isActive = row.getValue('is_active');
        return isActive ? <Badge variant="success">نشط</Badge> : <Badge variant="destructive">غير نشط</Badge>;
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
              <DropdownMenuItem onClick={() => openEditDialog(c)}><Edit className="mr-2 h-4 w-4" /> تعديل</DropdownMenuItem>
              {!c.is_base && (
                <DropdownMenuItem className="text-destructive" onClick={() => openDeleteDialog(c)}><Trash2 className="mr-2 h-4 w-4" /> حذف</DropdownMenuItem>
              )}
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
      const res = await api.get('/currencies');
      setData(res.data.items || []);
    } catch (err: any) {
      setError('فشل في تحميل العملات');
      toast.error('فشل في تحميل العملات');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        exchange_rate: parseFloat(formData.exchange_rate) || 1.0,
      };
      if (editingItem) {
        await api.put(`/currencies/${editingItem.id}`, payload);
        toast.success('تم تحديث العملة بنجاح');
      } else {
        await api.post('/currencies', payload);
        toast.success('تم إنشاء العملة بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData({ code: '', name: '', name_ar: '', symbol: '', exchange_rate: '1.0', is_base: false, is_active: true });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/currencies/${deletingItem.id}`);
      toast.success('تم حذف العملة بنجاح');
      setDeleteOpen(false);
      setDeletingItem(null);
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحذف');
    }
  };

  const openEditDialog = (item: any) => {
    setEditingItem(item);
    setFormData({
      code: item.code || '',
      name: item.name || '',
      name_ar: item.name_ar || '',
      symbol: item.symbol || '',
      exchange_rate: item.exchange_rate?.toString() || '1.0',
      is_base: item.is_base || false,
      is_active: item.is_active ?? true,
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
        title="Currencies"
        titleAr="العملات"
        description="Manage currency exchange rates"
        descriptionAr="إدارة العملات وأسعار الصرف"
        actions={
          <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData({ code: '', name: '', name_ar: '', symbol: '', exchange_rate: '1.0', is_base: false, is_active: true }); setDialogOpen(true); }}>
            <Plus className="ml-2 h-4 w-4" /> عملة جديدة
          </Button>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable
        columns={columns}
        data={data}
        searchKey="name"
        searchPlaceholder="بحث بالاسم..."
        loading={loading}
      />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل العملة' : 'عملة جديدة'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>كود العملة *</Label>
              <Input
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                required
                maxLength={3}
                placeholder="USD, SAR, YER"
                disabled={!!editingItem}
              />
            </div>
            <div className="space-y-2">
              <Label>الاسم (إنجليزي) *</Label>
              <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required placeholder="US Dollar" />
            </div>
            <div className="space-y-2">
              <Label>الاسم (عربي)</Label>
              <Input value={formData.name_ar} onChange={(e) => setFormData({ ...formData, name_ar: e.target.value })} placeholder="دولار أمريكي" />
            </div>
            <div className="space-y-2">
              <Label>الرمز</Label>
              <Input value={formData.symbol} onChange={(e) => setFormData({ ...formData, symbol: e.target.value })} placeholder="$" />
            </div>
            <div className="space-y-2">
              <Label>سعر الصرف</Label>
              <Input
                type="number"
                step="0.000001"
                value={formData.exchange_rate}
                onChange={(e) => setFormData({ ...formData, exchange_rate: e.target.value })}
                placeholder="1.0"
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>العملة الأساسية</Label>
              <Switch
                checked={formData.is_base}
                onCheckedChange={(checked) => setFormData({ ...formData, is_base: checked })}
              />
            </div>
            <div className="flex items-center justify-between">
              <Label>نشط</Label>
              <Switch
                checked={formData.is_active}
                onCheckedChange={(checked) => setFormData({ ...formData, is_active: checked })}
              />
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
            <AlertDialogDescription className="font-arabic">سيتم تنشيط العملة كغير نشطة.</AlertDialogDescription>
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
