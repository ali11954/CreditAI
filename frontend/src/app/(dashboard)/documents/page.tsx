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
import { Plus, Download, MoreHorizontal, Eye, Edit, Trash2, FileText, FileSpreadsheet, Upload } from 'lucide-react';
import { ColumnDef } from '@tanstack/react-table';
import { CustomerSelect } from '@/components/ui/customer-select';
import { toast } from 'sonner';
import api from '@/lib/api';

interface Document {
  id: string;
  title: string;
  type: string;
  customer_id: string;
  customer_name?: string;
  uploaded_by: string;
  uploaded_at: string;
  file_size: string;
  file_url?: string;
}

export default function DocumentsPage() {
  const [data, setData] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<Document | null>(null);
  const [deletingItem, setDeletingItem] = useState<Document | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    type: 'contract',
    customer_id: '',
  });

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, limit: 10 };
      if (search) params.search = search;
      const res = await api.get('/documents', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل الوثائق');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile && !editingItem) {
      toast.error('يرجى اختيار ملف');
      return;
    }
    try {
      const formDataObj = new FormData();
      formDataObj.append('title', formData.title);
      formDataObj.append('type', formData.type);
      formDataObj.append('customer_id', formData.customer_id);
      if (selectedFile) formDataObj.append('file', selectedFile);

      if (editingItem) {
        await api.put(`/documents/${editingItem.id}`, formDataObj, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        toast.success('تم تحديث الوثيقة بنجاح');
      } else {
        await api.post('/documents', formDataObj, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        toast.success('تم رفع الوثيقة بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setSelectedFile(null);
      setFormData({ title: '', type: 'contract', customer_id: '' });
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الرفع');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/documents/${deletingItem.id}`);
      toast.success('تم حذف الوثيقة بنجاح');
      setDeleteOpen(false);
      setDeletingItem(null);
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحذف');
    }
  };

  const handleDownload = async (doc: Document) => {
    try {
      const res = await api.get(`/documents/${doc.id}/download`, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = doc.title;
      a.click();
      toast.success('تم التحميل بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التحميل');
    }
  };

  const handleExport = async (format: 'excel' | 'pdf') => {
    try {
      const res = await api.post(`/export/${format}`, {
        data,
        columns: ['title', 'type', 'customer_name', 'uploaded_by', 'uploaded_at', 'file_size'],
        filename: 'documents',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `documents.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const columns: ColumnDef<Document>[] = [
    {
      accessorKey: 'title',
      header: 'العنوان',
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <FileText className="h-4 w-4 text-muted-foreground" />
          <span className="font-arabic">{row.getValue('title')}</span>
        </div>
      ),
    },
    {
      accessorKey: 'type',
      header: 'النوع',
      cell: ({ row }) => {
        const types: Record<string, string> = { contract: 'عقد', statement: 'كشف حساب', id: 'هوية', other: 'أخرى' };
        return <span className="font-arabic">{types[row.getValue('type') as string] || row.getValue('type')}</span>;
      },
    },
    { accessorKey: 'customer_name', header: 'العميل', cell: ({ row }) => <span className="font-arabic">{row.getValue('customer_name') || row.original.customer_id}</span> },
    { accessorKey: 'uploaded_by', header: 'رفعه', cell: ({ row }) => <span className="font-arabic">{row.getValue('uploaded_by')}</span> },
    { accessorKey: 'uploaded_at', header: 'التاريخ' },
    { accessorKey: 'file_size', header: 'الحجم' },
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
            <DropdownMenuItem onClick={() => handleDownload(row.original)}>
              <Download className="mr-2 h-4 w-4" /> تحميل
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => { setEditingItem(row.original); setFormData({ title: row.original.title, type: row.original.type, customer_id: row.original.customer_id }); setDialogOpen(true); }}>
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
        title="Documents"
        titleAr="الوثائق"
        description="Manage system documents"
        descriptionAr="إدارة وثائق النظام"
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
            <Button className="font-arabic" onClick={() => { setEditingItem(null); setSelectedFile(null); setFormData({ title: '', type: 'contract', customer_id: '' }); setDialogOpen(true); }}>
              <Plus className="ml-2 h-4 w-4" /> رفع وثيقة
            </Button>
          </div>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable columns={columns} data={data} searchKey="title" searchPlaceholder="بحث بالعنوان..." totalItems={total} loading={loading} onPageChange={setPage} />

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل الوثيقة' : 'رفع وثيقة جديدة'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleUpload} className="space-y-4">
            <div className="space-y-2">
              <Label>العنوان</Label>
              <Input value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>النوع</Label>
              <Select value={formData.type} onValueChange={(v) => setFormData({ ...formData, type: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="contract">عقد</SelectItem>
                  <SelectItem value="statement">كشف حساب</SelectItem>
                  <SelectItem value="id">هوية</SelectItem>
                  <SelectItem value="other">أخرى</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>العميل</Label>
              <CustomerSelect value={formData.customer_id} onChange={(v) => setFormData({ ...formData, customer_id: v })} />
            </div>
            <div className="space-y-2">
              <Label>الملف</Label>
              <Input type="file" onChange={(e) => setSelectedFile(e.target.files?.[0] || null)} />
            </div>
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>إلغاء</Button>
              <Button type="submit">{editingItem ? 'تحديث' : 'رفع'}</Button>
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
