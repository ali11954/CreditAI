'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, TrendingDown, LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatCardProps {
  title: string;
  titleEn?: string;
  value: string;
  change: string;
  changeType: 'positive' | 'negative' | 'neutral';
  icon: LucideIcon;
  className?: string;
}

export function StatCard({
  title,
  titleEn,
  value,
  change,
  changeType,
  icon: Icon,
  className,
}: StatCardProps) {
  return (
    <Card className={cn('hover-lift', className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium font-arabic">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className="flex items-center gap-1 text-xs">
          {changeType === 'positive' ? (
            <TrendingUp className="h-3 w-3 text-green-500" />
          ) : changeType === 'negative' ? (
            <TrendingDown className="h-3 w-3 text-red-500" />
          ) : null}
          <span
            className={cn(
              changeType === 'positive' && 'text-green-500',
              changeType === 'negative' && 'text-red-500',
              changeType === 'neutral' && 'text-muted-foreground'
            )}
          >
            {change}
          </span>
          <span className="text-muted-foreground font-arabic">من الشهر الماضي</span>
        </div>
      </CardContent>
    </Card>
  );
}
