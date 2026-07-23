'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { DataTable } from '@/components/data-table/data-table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Download, FileText, FileSpreadsheet, Loader2 } from 'lucide-react';
import { ColumnDef } from '@tanstack/react-table';
import { toast } from 'sonner';
import api from '@/lib/api';

interface AuditLog {
  id: string;
  user: string;
  action: string;
  entity: string;
  entity_id: string;
  timestamp: string;
  ip_address: string;
}

export default function AuditPage() {
  const [data, setData] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState('');

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params: Record<string, any> = { page, limit: 10 };
      if (search) params.search = search;
      const res = await api.get('/audit/trail', { params });
      setData(res.data.items || []);
      setTotal(res.data.total || 0);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل سجل التدقيق');
    } finally {
      setLoading(false);
    }
  }, [page, search]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleExport = async (format: 'excel' | 'pdf') => {
    try {
      const res = await api.post(`/export/${format}`, {
        data,
        columns: ['user', 'action', 'entity', 'entity_id', 'timestamp', 'ip_address'],
        filename: 'audit_log',
      }, { responseType: 'blob' });
      const blob = new Blob([res.data]);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `audit_log.${format === 'excel' ? 'xlsx' : 'pdf'}`;
      a.click();
      toast.success('تم التصدير بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التصدير');
    }
  };

  const columns: ColumnDef<AuditLog>[] = [
    { accessorKey: 'user', header: 'المستخدم', cell: ({ row }) => <span className="font-arabic">{row.getValue('user')}</span> },
    { accessorKey: 'action', header: 'الإجراء', cell: ({ row }) => <span className="font-arabic">{row.getValue('action')}</span> },
    { accessorKey: 'entity', header: 'الكيان', cell: ({ row }) => <span className="font-arabic">{row.getValue('entity')}</span> },
    { accessorKey: 'entity_id', header: 'المعرف' },
    { accessorKey: 'timestamp', header: 'التاريخ والوقت' },
    { accessorKey: 'ip_address', header: 'IP' },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Audit Log"
        titleAr="سجل التدقيق"
        description="System audit trail"
        descriptionAr="سجل تدقيق النظام"
        actions={
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
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <DataTable columns={columns} data={data} searchKey="user" searchPlaceholder="بحث بالمستخدم..." totalItems={total} loading={loading} onPageChange={setPage} />
    </div>
  );
}
