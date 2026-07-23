'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Edit, ArrowRight, Loader2 } from 'lucide-react';
import Link from 'next/link';
import { toast } from 'sonner';
import api from '@/lib/api';

export default function UserDetailPage() {
  const params = useParams();
  const userId = params.id;
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      try {
        const res = await api.get(`/users/${userId}`);
        setUser(res.data);
      } catch (err: any) {
        setError('فشل في تحميل بيانات المستخدم');
        toast.error('فشل في تحميل بيانات المستخدم');
      } finally {
        setLoading(false);
      }
    };
    if (userId) fetchUser();
  }, [userId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (error) {
    return <div className="text-destructive text-center font-arabic">{error}</div>;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="User Details"
        titleAr="تفاصيل المستخدم"
        actions={
          <div className="flex gap-2">
            <Link href="/users">
              <Button variant="outline" className="font-arabic">
                <ArrowRight className="ml-2 h-4 w-4" /> رجوع
              </Button>
            </Link>
            <Button className="font-arabic">
              <Edit className="ml-2 h-4 w-4" /> تعديل
            </Button>
          </div>
        }
      />

      <Tabs defaultValue="overview" className="w-full">
        <TabsList>
          <TabsTrigger value="overview" className="font-arabic">نظرة عامة</TabsTrigger>
          <TabsTrigger value="permissions" className="font-arabic">الصلاحيات</TabsTrigger>
          <TabsTrigger value="activity" className="font-arabic">النشاط</TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">المعلومات الشخصية</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الاسم</p>
                <p className="font-medium font-arabic">{user?.full_name || '-'}</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الاسم بالعربي</p>
                <p className="font-medium font-arabic">{user?.full_name_ar || '-'}</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">البريد الإلكتروني</p>
                <p className="font-medium" dir="ltr">{user?.email || '-'}</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">اسم المستخدم</p>
                <p className="font-medium">{user?.username || '-'}</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الدور</p>
                <Badge>{user?.role || '-'}</Badge>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الحالة</p>
                <Badge variant={user?.is_active ? 'success' : 'secondary'}>
                  {user?.is_active ? 'نشط' : 'غير نشط'}
                </Badge>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">تاريخ الإنشاء</p>
                <p className="font-medium font-arabic">{user?.created_at || '-'}</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="permissions">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">الصلاحيات</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground font-arabic">صلاحيات المستخدم بناء على دوره: {user?.role}</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="activity">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">سجل النشاط</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground font-arabic">آخر أنشطة المستخدم</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
