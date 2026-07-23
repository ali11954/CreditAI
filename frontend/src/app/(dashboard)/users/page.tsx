'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Plus, FileSpreadsheet, MoreHorizontal, Eye, Edit, Trash2, Loader2 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { ColumnDef } from '@tanstack/react-table';
import Link from 'next/link';
import api from '@/lib/api';

export default function UsersPage() {
  const [data, setData] = useState<any[]>([]);
  const [roles, setRoles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<any>(null);
  const [deletingItem, setDeletingItem] = useState<any>(null);
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
    full_name_ar: '',
    role_id: '',
    password: '',
  });

  const columns: ColumnDef<any>[] = [
    {
      accessorKey: 'full_name',
      header: 'الاسم',
      cell: ({ row }) => (
        <Link href={`/users/${row.original.id}`} className="font-medium hover:underline font-arabic">{row.getValue('full_name')}</Link>
      ),
    },
    { accessorKey: 'full_name_ar', header: 'الاسم بالعربي', cell: ({ row }) => <span className="font-arabic">{row.getValue('full_name_ar')}</span> },
    { accessorKey: 'email', header: 'البريد الإلكتروني' },
    {
      accessorKey: 'role', header: 'الدور',
      cell: ({ row }) => <span className="font-arabic">{row.getValue('role')}</span>,
    },
    {
      accessorKey: 'is_active', header: 'الحالة',
      cell: ({ row }) => {
        const active = row.getValue('is_active') as boolean;
        return <Badge variant={active ? 'success' : 'secondary'}>{active ? 'نشط' : 'غير نشط'}</Badge>;
      },
    },
    {
      id: 'actions', header: 'الإجراءات',
      cell: ({ row }) => {
        const user = row.original;
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0"><MoreHorizontal className="h-4 w-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem asChild><Link href={`/users/${user.id}`}><Eye className="mr-2 h-4 w-4" /> عرض</Link></DropdownMenuItem>
              <DropdownMenuItem onClick={() => { setEditingItem(user); setFormData({ email: user.email, username: user.username, full_name: user.full_name, full_name_ar: user.full_name_ar || '', role_id: user.role_id || '', password: '' }); setDialogOpen(true); }}><Edit className="mr-2 h-4 w-4" /> تعديل</DropdownMenuItem>
              <DropdownMenuItem className="text-destructive" onClick={() => { setDeletingItem(user); setDeleteOpen(true); }}><Trash2 className="mr-2 h-4 w-4" /> حذف</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  const fetchRoles = useCallback(async () => {
    try {
      const res = await api.get('/roles/active');
      setRoles(res.data.items || []);
    } catch (err: any) {
      console.error('Failed to load roles');
    }
  }, []);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, page_size: 10 };
      if (search) params.search = search;
      const res = await api.get('/users', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل المستخدمين');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => {
    fetchRoles();
    fetchData();
  }, [fetchRoles, fetchData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload: Record<string, any> = { ...formData };
      if (!payload.password) delete payload.password;
      if (!payload.role_id) delete payload.role_id;

      if (editingItem) {
        await api.put(`/users/${editingItem.id}`, payload);
        toast.success('تم تحديث المستخدم بنجاح');
      } else {
        await api.post('/users', payload);
        toast.success('تم إنشاء المستخدم بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData({ email: '', username: '', full_name: '', full_name_ar: '', role_id: '', password: '' });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/users/${deletingItem.id}`);
      toast.success('تم حذف المستخدم بنجاح');
      setDeleteOpen(false);
      setDeletingItem(null);
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحذف');
    }
  };

  const handleExport = async () => {
    try {
      const res = await api.post('/export/excel', {
        data,
        columns: ['full_name', 'full_name_ar', 'email', 'role', 'is_active', 'created_at'],
        filename: 'users',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'users.xlsx';
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Users"
        titleAr="المستخدمون"
        description="Manage system users and their roles"
        descriptionAr="إدارة مستخدمي النظام وأدوارهم"
        actions={
          <div className="flex gap-2">
            <Button variant="outline" className="font-arabic" onClick={handleExport}>
              <FileSpreadsheet className="ml-2 h-4 w-4" /> تصدير Excel
            </Button>
            <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData({ email: '', username: '', full_name: '', full_name_ar: '', role_id: '', password: '' }); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> مستخدم جديد
            </Button>
          </div>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable columns={columns} data={data} searchKey="full_name" searchPlaceholder="بحث بالاسم..." totalItems={total} loading={loading} onPageChange={setPage} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل المستخدم' : 'مستخدم جديد'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>البريد الإلكتروني</Label>
              <Input type="email" value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} required dir="ltr" />
            </div>
            <div className="space-y-2">
              <Label>اسم المستخدم</Label>
              <Input value={formData.username} onChange={(e) => setFormData({ ...formData, username: e.target.value })} required dir="ltr" />
            </div>
            <div className="space-y-2">
              <Label>الاسم الكامل</Label>
              <Input value={formData.full_name} onChange={(e) => setFormData({ ...formData, full_name: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>الاسم بالعربي</Label>
              <Input value={formData.full_name_ar} onChange={(e) => setFormData({ ...formData, full_name_ar: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>الدور</Label>
              <Select value={formData.role_id} onValueChange={(v) => setFormData({ ...formData, role_id: v })}>
                <SelectTrigger><SelectValue placeholder="اختر الدور" /></SelectTrigger>
                <SelectContent>
                  {roles.map((role) => (
                    <SelectItem key={role.id} value={role.id}>{role.name_ar || role.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>{editingItem ? 'كلمة المرور (اترك فارغة للإبقاء)' : 'كلمة المرور'}</Label>
              <Input type="password" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} required={!editingItem} dir="ltr" />
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
