'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { getInitials } from '@/lib/utils';

const activities = [
  {
    id: 1,
    user: 'أحمد محمد',
    action: 'أقرض طلب ائتمان جديد',
    entity: 'شركة الأمل',
    time: 'منذ 5 دقائق',
    type: 'success',
  },
  {
    id: 2,
    user: 'سارة علي',
    action: 'رفضت طلب ائتمان',
    entity: 'مؤسسة النور',
    time: 'منذ 15 دقيقة',
    type: 'destructive',
  },
  {
    id: 3,
    user: 'محمد خالد',
    action: 'أضاف وثيقة جديدة',
    entity: 'عميل جديد',
    time: 'منذ 30 دقيقة',
    type: 'info',
  },
  {
    id: 4,
    user: 'فاطمة أحمد',
    action: 'أكملت مراجعة',
    entity: 'طلب #1234',
    time: 'منذ ساعة',
    type: 'warning',
  },
  {
    id: 5,
    user: 'عمر حسن',
    action: 'أنشأ تقرير',
    entity: 'تقرير شهري',
    time: 'منذ ساعتين',
    type: 'secondary',
  },
];

export function RecentActivity({ className }: { className?: string }) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="font-arabic">النشاط الأخير</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-start gap-4">
              <Avatar className="h-8 w-8">
                <AvatarFallback className="text-xs font-arabic">
                  {getInitials(activity.user)}
                </AvatarFallback>
              </Avatar>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-arabic">
                  <span className="font-medium">{activity.user}</span>{' '}
                  {activity.action}
                </p>
                <div className="flex items-center gap-2">
                  <p className="text-xs text-muted-foreground font-arabic">{activity.entity}</p>
                  <span className="text-xs text-muted-foreground">•</span>
                  <p className="text-xs text-muted-foreground font-arabic">{activity.time}</p>
                </div>
              </div>
              <Badge variant={activity.type as any} className="shrink-0">
                {activity.type === 'success' && 'مقبول'}
                {activity.type === 'destructive' && 'مرفوض'}
                {activity.type === 'info' && 'جديد'}
                {activity.type === 'warning' && 'معلق'}
                {activity.type === 'secondary' && 'تقرير'}
              </Badge>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
