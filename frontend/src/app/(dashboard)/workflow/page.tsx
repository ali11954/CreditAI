'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { GitBranch, Plus, Play, Pause, Settings, MoreHorizontal, Eye, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/lib/api';

export default function WorkflowPage() {
  const [workflows, setWorkflows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/workflow/templates');
      setWorkflows(res.data.items || []);
    } catch (err: any) {
      setError('فشل في تحميل البيانات');
      toast.error('فشل في تحميل سير العمل');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleToggleStatus = async (id: string, currentStatus: string) => {
    try {
      const newStatus = currentStatus === 'active' ? 'paused' : 'active';
      await api.put(`/workflow/templates/${id}`, { status: newStatus });
      toast.success('تم تحديث الحالة بنجاح');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء التحديث');
    }
  };

  const handleStartWorkflow = async (id: string) => {
    try {
      await api.post(`/workflow/templates/${id}/start`);
      toast.success('تم بدء سير العمل بنجاح');
      fetchData();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء بدء سير العمل');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Workflow"
        titleAr="سير العمل"
        description="Automation workflows"
        descriptionAr="أتمتة سير العمل"
        actions={
          <Button className="font-arabic">
            <Plus className="ml-2 h-4 w-4" /> سير عمل جديد
          </Button>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <div className="grid gap-4 md:grid-cols-2">
        {workflows.map((wf) => (
          <Card key={wf.id}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <GitBranch className="h-5 w-5 text-primary" />
                  <CardTitle className="font-arabic">{wf.name}</CardTitle>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={wf.status === 'active' ? 'success' : 'secondary'}>
                    {wf.status === 'active' ? 'نشط' : 'متوقف'}
                  </Badge>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="h-8 w-8 p-0">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleStartWorkflow(wf.id)}>
                        <Play className="mr-2 h-4 w-4" /> تشغيل
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleToggleStatus(wf.id, wf.status)}>
                        {wf.status === 'active' ? <Pause className="mr-2 h-4 w-4" /> : <Play className="mr-2 h-4 w-4" />}
                        {wf.status === 'active' ? 'إيقاف' : 'تشغيل'}
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between text-sm text-muted-foreground mb-4">
                <span className="font-arabic">{wf.steps_count || wf.steps || 0} خطوات</span>
                <span className="font-arabic">{wf.runs_count || wf.runs || 0} تشغيل</span>
                <span className="font-arabic">آخر تشغيل: {wf.last_run || '-'}</span>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="font-arabic" onClick={() => handleToggleStatus(wf.id, wf.status)}>
                  {wf.status === 'active' ? <Pause className="ml-1 h-3 w-3" /> : <Play className="ml-1 h-3 w-3" />}
                  {wf.status === 'active' ? 'إيقاف' : 'تشغيل'}
                </Button>
                <Button variant="ghost" size="sm">
                  <Settings className="h-3 w-3" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
        {workflows.length === 0 && (
          <Card className="col-span-full">
            <CardContent className="pt-6">
              <p className="text-center text-muted-foreground font-arabic">لا توجد سير عمل</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
