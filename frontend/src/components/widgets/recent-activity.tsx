'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { getInitials } from '@/lib/utils';
import api from '@/lib/api';
import { Loader2 } from 'lucide-react';

interface Activity {
  id: string;
  user_name: string;
  action: string;
  entity: string;
  entity_type: string;
  time: string;
  type: string;
}

export function RecentActivity({ className }: { className?: string }) {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const res = await api.get('/dashboards/recent-activity');
        setActivities(res.data || []);
      } catch {
        setActivities([]);
      } finally {
        setLoading(false);
      }
    };
    fetchActivities();
  }, []);

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="font-arabic">النشاط الأخير</CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin" />
          </div>
        ) : activities.length === 0 ? (
          <p className="text-center text-muted-foreground py-8 font-arabic">لا يوجد نشاط حتى الآن</p>
        ) : (
          <div className="space-y-4">
            {activities.map((activity) => (
              <div key={activity.id} className="flex items-start gap-4">
                <Avatar className="h-8 w-8">
                  <AvatarFallback className="text-xs font-arabic">
                    {getInitials(activity.user_name)}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-arabic">
                    <span className="font-medium">{activity.user_name}</span>{' '}
                    {activity.action}
                  </p>
                  <div className="flex items-center gap-2">
                    <p className="text-xs text-muted-foreground font-arabic">{activity.entity}</p>
                    <span className="text-xs text-muted-foreground">•</span>
                    <p className="text-xs text-muted-foreground font-arabic">{activity.time}</p>
                  </div>
                </div>
                <Badge variant={activity.type as any} className="shrink-0">
                  {activity.entity_type}
                </Badge>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
