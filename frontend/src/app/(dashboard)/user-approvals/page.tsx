'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import api from '@/lib/api';
import { CheckCircle, XCircle, Clock, Users } from 'lucide-react';

interface PendingUser {
  id: string;
  email: string;
  username: string;
  full_name: string;
  created_at: string;
}

export default function UserApprovalsPage() {
  const [users, setUsers] = useState<PendingUser[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  const fetchPending = async () => {
    try {
      const res = await api.get('/auth/pending-users');
      setUsers(res.data);
    } catch (err: any) {
      toast({ title: 'خطأ', description: 'فشل تحميل المستخدمين', variant: 'destructive' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchPending(); }, []);

  const approve = async (userId: string) => {
    try {
      await api.post(`/auth/approve-user/${userId}`);
      toast({ title: 'تم', description: 'تمت الموافقة على المستخدم', variant: 'default' });
      setUsers(users.filter(u => u.id !== userId));
    } catch (err: any) {
      toast({ title: 'خطأ', description: 'فشل الموافقة', variant: 'destructive' });
    }
  };

  const reject = async (userId: string) => {
    try {
      await api.post(`/auth/reject-user/${userId}?reason=Rejected by admin`);
      toast({ title: 'تم', description: 'تم رفض المستخدم', variant: 'default' });
      setUsers(users.filter(u => u.id !== userId));
    } catch (err: any) {
      toast({ title: 'خطأ', description: 'فشل الرفض', variant: 'destructive' });
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
          <Users className="h-5 w-5 text-primary" />
        </div>
        <div>
          <h1 className="text-2xl font-bold font-arabic">موافقة المستخدمين</h1>
          <p className="text-sm text-muted-foreground font-arabic">إدارة طلبات التسجيل الجديدة</p>
        </div>
      </div>

      {loading ? (
        <Card>
          <CardContent className="py-10 text-center">
            <Clock className="mx-auto h-8 w-8 animate-spin text-muted-foreground" />
            <p className="mt-2 text-sm text-muted-foreground font-arabic">جاري التحميل...</p>
          </CardContent>
        </Card>
      ) : users.length === 0 ? (
        <Card>
          <CardContent className="py-10 text-center">
            <CheckCircle className="mx-auto h-8 w-8 text-green-500" />
            <p className="mt-2 text-sm text-muted-foreground font-arabic">لا توجد طلبات معلقة</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {users.map((user) => (
            <Card key={user.id}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg font-arabic">{user.full_name}</CardTitle>
                    <CardDescription className="font-arabic">
                      {user.email} | @{user.username}
                    </CardDescription>
                  </div>
                  <Badge variant="outline" className="text-amber-600">
                    <Clock className="mr-1 h-3 w-3" />
                    معلق
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="mb-3 text-xs text-muted-foreground font-arabic">
                  طلب التسجيل: {new Date(user.created_at).toLocaleDateString('ar-SA')}
                </p>
                <div className="flex gap-2">
                  <Button size="sm" className="bg-green-600 hover:bg-green-700 font-arabic" onClick={() => approve(user.id)}>
                    <CheckCircle className="mr-1 h-4 w-4" />
                    موافقة
                  </Button>
                  <Button size="sm" variant="destructive" className="font-arabic" onClick={() => reject(user.id)}>
                    <XCircle className="mr-1 h-4 w-4" />
                    رفض
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
