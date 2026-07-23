'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Clock, FileWarning } from 'lucide-react';
import { cn } from '@/lib/utils';
import api from '@/lib/api';
import { Loader2 } from 'lucide-react';

interface Alert {
  id: string;
  title: string;
  description: string;
  type: string;
  count?: number;
}

const iconMap: Record<string, any> = {
  warning: AlertTriangle,
  destructive: FileWarning,
  info: Clock,
};

export function AlertsWidget({ className }: { className?: string }) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await api.get('/dashboards/alerts');
        setAlerts(res.data || []);
      } catch {
        setAlerts([]);
      } finally {
        setLoading(false);
      }
    };
    fetchAlerts();
  }, []);

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="font-arabic">التحذيرات</CardTitle>
          <Badge variant="destructive">{alerts.length}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin" />
          </div>
        ) : alerts.length === 0 ? (
          <p className="text-center text-muted-foreground py-8 font-arabic">لا يوجد تحذيرات</p>
        ) : (
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
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
