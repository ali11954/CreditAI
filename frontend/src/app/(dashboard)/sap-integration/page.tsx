'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Database, RefreshCw, CheckCircle, AlertTriangle, Clock, MoreHorizontal, Play, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/lib/api';

export default function SAPIntegrationPage() {
  const [syncJobs, setSyncJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [syncingId, setSyncingId] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/sap/sync-status');
      setSyncJobs(res.data.items || []);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل حالة المزامنة');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSync = async (type: string, id?: string) => {
    const syncId = id || type;
    setSyncingId(syncId);
    try {
      await api.post(`/sap/sync/${type}/${id || ''}`);
      toast.success('تم بدء المزامنة بنجاح');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء المزامنة');
    } finally {
      setSyncingId(null);
    }
  };

  const handleSyncAll = async () => {
    setSyncingId('all');
    try {
      await api.post('/sap/sync/all');
      toast.success('تم بدء مزامنة جميع البيانات');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء المزامنة');
    } finally {
      setSyncingId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  const successCount = syncJobs.filter(j => j.status === 'success').length;
  const pendingCount = syncJobs.filter(j => j.status === 'pending').length;
  const errorCount = syncJobs.filter(j => j.status === 'error').length;
  const totalRecords = syncJobs.reduce((sum, j) => sum + (j.records || 0), 0);

  return (
    <div className="space-y-6">
      <PageHeader
        title="SAP Integration"
        titleAr="تكامل SAP"
        description="SAP ERP integration management"
        descriptionAr="إدارة التكامل مع نظام SAP"
        actions={
          <Button className="font-arabic" onClick={handleSyncAll} disabled={syncingId === 'all'}>
            {syncingId === 'all' ? (
              <Loader2 className="ml-2 h-4 w-4 animate-spin" />
            ) : (
              <RefreshCw className="ml-2 h-4 w-4" />
            )}
            {syncingId === 'all' ? 'جاري المزامنة...' : 'تشغيل المزامنة'}
          </Button>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <CheckCircle className="h-8 w-8 text-green-500" />
              <div>
                <p className="text-2xl font-bold">{successCount}</p>
                <p className="text-sm text-muted-foreground font-arabic">نجاح</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Clock className="h-8 w-8 text-yellow-500" />
              <div>
                <p className="text-2xl font-bold">{pendingCount}</p>
                <p className="text-sm text-muted-foreground font-arabic">معلق</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <AlertTriangle className="h-8 w-8 text-red-500" />
              <div>
                <p className="text-2xl font-bold">{errorCount}</p>
                <p className="text-sm text-muted-foreground font-arabic">خطأ</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Database className="h-8 w-8 text-blue-500" />
              <div>
                <p className="text-2xl font-bold">{totalRecords.toLocaleString('en-US')}</p>
                <p className="text-sm text-muted-foreground font-arabic">إجمالي السجلات</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="font-arabic">مهام المزامنة</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {syncJobs.map((job) => (
              <div key={job.id} className="flex items-center justify-between rounded-md border p-4">
                <div className="flex items-center gap-3">
                  {job.status === 'success' ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : job.status === 'error' ? (
                    <AlertTriangle className="h-5 w-5 text-red-500" />
                  ) : (
                    <Clock className="h-5 w-5 text-yellow-500" />
                  )}
                  <div>
                    <p className="font-medium font-arabic">{job.name}</p>
                    <p className="text-sm text-muted-foreground font-arabic">
                      آخر مزامنة: {job.last_sync || '-'} | {job.records || 0} سجل
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={job.status === 'success' ? 'success' : job.status === 'error' ? 'destructive' : 'warning'}>
                    {job.status === 'success' ? 'نجاح' : job.status === 'error' ? 'خطأ' : 'معلق'}
                  </Badge>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="h-8 w-8 p-0">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleSync(job.type || job.name, job.id)}>
                        <Play className="mr-2 h-4 w-4" /> مزامنة
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>
            ))}
            {syncJobs.length === 0 && (
              <p className="text-center text-muted-foreground font-arabic py-8">لا توجد مهام مزامنة</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
