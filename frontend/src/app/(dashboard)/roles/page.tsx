'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from '@/components/ui/alert-dialog';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Plus, Shield, Users, MoreHorizontal, Edit, Trash2, Loader2, Key } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/lib/api';

const PERMISSION_MODULES = {
  'customers': { ar: 'العملاء', permissions: ['read', 'create', 'update', 'delete', 'export'] },
  'credit_applications': { ar: 'طلبات الائتمان', permissions: ['read', 'create', 'update', 'delete', 'approve', 'export'] },
  'credit_limits': { ar: 'الحدود الائتمانية', permissions: ['read', 'create', 'update', 'delete', 'export'] },
  'collections': { ar: 'التحصيل', permissions: ['read', 'create', 'update', 'delete', 'assign', 'export'] },
  'legal_cases': { ar: 'القضايا القانونية', permissions: ['read', 'create', 'update', 'delete', 'assign', 'export'] },
  'documents': { ar: 'المستندات', permissions: ['read', 'create', 'update', 'delete', 'upload', 'ocr', 'export'] },
  'reports': { ar: 'التقارير', permissions: ['read', 'create', 'execute', 'export'] },
  'settings': { ar: 'الإعدادات', permissions: ['read', 'update'] },
  'branches': { ar: 'الفروع', permissions: ['read', 'create', 'update', 'delete'] },
  'departments': { ar: 'الأقسام', permissions: ['read', 'create', 'update', 'delete'] },
  'teams': { ar: 'الفرق', permissions: ['read', 'create', 'update', 'delete'] },
  'users': { ar: 'المستخدمين', permissions: ['read', 'create', 'update', 'delete'] },
  'roles': { ar: 'الأدوار', permissions: ['read', 'create', 'update', 'delete'] },
  'audit': { ar: 'سجل المراجعة', permissions: ['read', 'export'] },
  'compliance': { ar: 'الامتثال', permissions: ['read', 'create', 'update', 'export'] },
  'exposure': { ar: 'التعرض', permissions: ['read', 'export'] },
  'notifications': { ar: 'الإشعارات', permissions: ['read', 'create', 'update', 'delete'] },
  'delegations': { ar: 'التفويضات', permissions: ['read', 'create', 'update', 'delete'] },
  'currencies': { ar: 'العملات', permissions: ['read', 'create', 'update', 'delete'] },
  'sales': { ar: 'المبيعات', permissions: ['read', 'create', 'update', 'delete', 'import', 'export'] },
};

export default function RolesPage() {
  const [roles, setRoles] = useState<any[]>([]);
  const [permissions, setPermissions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [permissionsDialogOpen, setPermissionsDialogOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<any>(null);
  const [deletingItem, setDeletingItem] = useState<any>(null);
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([]);
  const [formData, setFormData] = useState({
    name: '',
    name_ar: '',
    description: '',
  });

  const fetchRoles = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/roles');
      setRoles(res.data.items || []);
    } catch (err: any) {
      setError('فشل في تحميل الأدوار');
      toast.error('فشل في تحميل الأدوار');
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchPermissions = useCallback(async () => {
    try {
      const res = await api.get('/roles/all-permissions');
      setPermissions(res.data.items || []);
    } catch (err: any) {
      // Permissions not seeded yet, use default module list
      const allPerms: any[] = [];
      Object.entries(PERMISSION_MODULES).forEach(([module, config]) => {
        config.permissions.forEach((action) => {
          allPerms.push({
            name: `${module}:${action}`,
            module,
            action,
          });
        });
      });
      setPermissions(allPerms);
    }
  }, []);

  useEffect(() => {
    fetchRoles();
    fetchPermissions();
  }, [fetchRoles, fetchPermissions]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await api.put(`/roles/${editingItem.id}`, formData);
        toast.success('تم تحديث الدور بنجاح');
      } else {
        await api.post('/roles', formData);
        toast.success('تم إنشاء الدور بنجاح');
      }
      setDialogOpen(false);
      setEditingItem(null);
      setFormData({ name: '', name_ar: '', description: '' });
      fetchRoles();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    }
  };

  const handleDelete = async () => {
    if (!deletingItem) return;
    try {
      await api.delete(`/roles/${deletingItem.id}`);
      toast.success('تم حذف الدور بنجاح');
      setDeleteOpen(false);
      setDeletingItem(null);
      fetchRoles();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحذف');
    }
  };

  const handleOpenPermissions = (role: any) => {
    setEditingItem(role);
    setSelectedPermissions(role.permissions || []);
    setPermissionsDialogOpen(true);
  };

  const handleSavePermissions = async () => {
    if (!editingItem) return;
    try {
      await api.put(`/roles/${editingItem.id}/permissions`, { permissions: selectedPermissions });
      toast.success('تم تحديث الصلاحيات بنجاح');
      setPermissionsDialogOpen(false);
      setEditingItem(null);
      fetchRoles();
    } catch (err: any) {
      toast.error('حدث خطأ أثناء حفظ الصلاحيات');
    }
  };

  const togglePermission = (permName: string) => {
    setSelectedPermissions((prev) =>
      prev.includes(permName) ? prev.filter((p) => p !== permName) : [...prev, permName]
    );
  };

  const toggleModulePermissions = (module: string, actions: string[]) => {
    const allModulePerms = actions.map((a) => `${module}:${a}`);
    const allSelected = allModulePerms.every((p) => selectedPermissions.includes(p));
    if (allSelected) {
      setSelectedPermissions((prev) => prev.filter((p) => !p.startsWith(`${module}:`)));
    } else {
      setSelectedPermissions((prev) => [...new Set([...prev, ...allModulePerms])]);
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
        title="Roles & Permissions"
        titleAr="الأدوار والصلاحيات"
        description="Manage user roles and their permissions"
        descriptionAr="إدارة أدوار المستخدمين وصلاحياتهم"
        actions={
          <Button className="font-arabic" onClick={() => { setEditingItem(null); setFormData({ name: '', name_ar: '', description: '' }); setDialogOpen(true); }}>
            <Plus className="ml-2 h-4 w-4" /> دور جديد
          </Button>
        }
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {roles.map((role) => (
          <Card key={role.id} className="hover-lift">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-primary" />
                  <CardTitle className="font-arabic">{role.name_ar || role.name}</CardTitle>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="h-8 w-8 p-0">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem onClick={() => { setEditingItem(role); setFormData({ name: role.name || '', name_ar: role.name_ar || '', description: role.description || '' }); setDialogOpen(true); }}>
                      <Edit className="mr-2 h-4 w-4" /> تعديل
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleOpenPermissions(role)}>
                      <Key className="mr-2 h-4 w-4" /> الصلاحيات
                    </DropdownMenuItem>
                    <DropdownMenuItem className="text-destructive" onClick={() => { setDeletingItem(role); setDeleteOpen(true); }}>
                      <Trash2 className="mr-2 h-4 w-4" /> حذف
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm text-muted-foreground font-arabic">{role.description || 'لا يوجد وصف'}</p>
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-1 text-muted-foreground">
                  <Users className="h-4 w-4" />
                  <span className="font-arabic">{role.users_count || 0} مستخدم</span>
                </div>
                <Badge variant="secondary" className="font-arabic">
                  {(role.permissions || []).includes('*') ? 'كل الصلاحيات' : `${(role.permissions || []).length} صلاحية`}
                </Badge>
              </div>
              <div className="flex flex-wrap gap-1">
                {(role.permissions || []).slice(0, 3).map((perm: string) => (
                  <Badge key={perm} variant="outline" className="text-xs font-arabic">{perm}</Badge>
                ))}
                {(role.permissions || []).length > 3 && (
                  <Badge variant="outline" className="text-xs font-arabic">+{(role.permissions || []).length - 3}</Badge>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic">
          <DialogHeader>
            <DialogTitle>{editingItem ? 'تعديل الدور' : 'دور جديد'}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label>الاسم (إنجليزي)</Label>
              <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required dir="ltr" />
            </div>
            <div className="space-y-2">
              <Label>الاسم بالعربي</Label>
              <Input value={formData.name_ar} onChange={(e) => setFormData({ ...formData, name_ar: e.target.value })} />
            </div>
            <div className="space-y-2">
              <Label>الوصف</Label>
              <Textarea value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
            </div>
            <div className="flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => setDialogOpen(false)}>إلغاء</Button>
              <Button type="submit">{editingItem ? 'تحديث' : 'حفظ'}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      <Dialog open={permissionsDialogOpen} onOpenChange={setPermissionsDialogOpen}>
        <DialogContent className="font-arabic max-w-3xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>صلاحيات الدور: {editingItem?.name_ar || editingItem?.name}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b">
              <Checkbox
                id="select-all"
                checked={selectedPermissions.includes('*')}
                onCheckedChange={(checked) => {
                  if (checked) {
                    setSelectedPermissions(['*']);
                  } else {
                    setSelectedPermissions([]);
                  }
                }}
              />
              <Label htmlFor="select-all" className="font-bold">كل الصلاحيات (*)</Label>
            </div>

            {Object.entries(PERMISSION_MODULES).map(([module, config]) => {
              const modulePerms = config.permissions.map((a) => `${module}:${a}`);
              const selectedCount = modulePerms.filter((p) => selectedPermissions.includes(p)).length;
              const allSelected = modulePerms.every((p) => selectedPermissions.includes(p));

              return (
                <div key={module} className="space-y-2">
                  <div className="flex items-center gap-2 pb-1 border-b">
                    <Checkbox
                      id={`module-${module}`}
                      checked={allSelected}
                      onCheckedChange={() => toggleModulePermissions(module, config.permissions)}
                    />
                    <Label htmlFor={`module-${module}`} className="font-bold">{config.ar} ({module})</Label>
                    <Badge variant="secondary" className="mr-auto text-xs">{selectedCount}/{config.permissions.length}</Badge>
                  </div>
                  <div className="grid grid-cols-3 gap-2 mr-6">
                    {config.permissions.map((action) => {
                      const permName = `${module}:${action}`;
                      const actionLabels: Record<string, string> = {
                        read: 'عرض',
                        create: 'إنشاء',
                        update: 'تعديل',
                        delete: 'حذف',
                        approve: 'اعتماد',
                        assign: 'تعيين',
                        export: 'تصدير',
                        upload: 'رفع',
                        ocr: 'تمييز',
                        import: 'استيراد',
                        execute: 'تنفيذ',
                      };
                      return (
                        <div key={action} className="flex items-center gap-2">
                          <Checkbox
                            id={`perm-${permName}`}
                            checked={selectedPermissions.includes(permName)}
                            onCheckedChange={() => togglePermission(permName)}
                          />
                          <Label htmlFor={`perm-${permName}`} className="text-sm">{actionLabels[action] || action}</Label>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}

            <div className="flex justify-end gap-2 pt-4 border-t">
              <Button type="button" variant="outline" onClick={() => setPermissionsDialogOpen(false)}>إلغاء</Button>
              <Button onClick={handleSavePermissions}>حفظ الصلاحيات</Button>
            </div>
          </div>
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
