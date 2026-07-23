'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Clock, FileWarning } from 'lucide-react';
import { cn } from '@/lib/utils';

const alerts = [
  {
    id: 1,
    title: 'طلب ائتمان ينتظر المراجعة',
    description: 'طلب من شركة الأمل بقيمة ₪ 500,000',
    type: 'warning',
    time: 'منذ ساعة',
  },
  {
    id: 2,
    title: 'دفعة متأخرة',
    description: 'عميل النور تجاوز موعد الدفع بـ 30 يوم',
    type: 'destructive',
    time: 'منذ 3 ساعات',
  },
  {
    id: 3,
    title: 'وثائق منتهية الصلاحية',
    description: '3 وثائق تحتاج تجديد',
    type: 'info',
    time: 'اليوم',
  },
  {
    id: 4,
    title: 'حد الائتمانقارب الاكتمال',
    description: 'عميل使用 85% من الحد',
    type: 'warning',
    time: 'أمس',
  },
];

const iconMap: Record<string, any> = {
  warning: AlertTriangle,
  destructive: FileWarning,
  info: Clock,
};

export function AlertsWidget({ className }: { className?: string }) {
  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="font-arabic">التحذيرات</CardTitle>
          <Badge variant="destructive">{alerts.length}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {alerts.map((alert) => {
            const Icon = iconMap[alert.type] || AlertTriangle;
            return (
              <div
                key={alert.id}
                className={cn(
                  'flex items-start gap-3 rounded-lg border p-3 transition-colors hover:bg-muted/50'
                )}
              >
                <Icon
                  className={cn(
                    'mt-0.5 h-4 w-4 shrink-0',
                    alert.type === 'destructive' && 'text-destructive',
                    alert.type === 'warning' && 'text-yellow-500',
                    alert.type === 'info' && 'text-blue-500'
                  )}
                />
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-medium font-arabic">{alert.title}</p>
                  <p className="text-xs text-muted-foreground font-arabic">
                    {alert.description}
                  </p>
                  <p className="text-xs text-muted-foreground font-arabic">{alert.time}</p>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
