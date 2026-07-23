'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

interface PageHeaderProps {
  title: string;
  titleAr?: string;
  description?: string;
  descriptionAr?: string;
  actions?: React.ReactNode;
  children?: React.ReactNode;
}

export function PageHeader({
  title,
  titleAr,
  description,
  descriptionAr,
  actions,
  children,
}: PageHeaderProps) {
  return (
    <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 className="text-2xl font-bold tracking-tight font-arabic">
          {titleAr || title}
        </h1>
        {(descriptionAr || description) && (
          <p className="mt-1 text-sm text-muted-foreground font-arabic">
            {descriptionAr || description}
          </p>
        )}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
      {children}
    </div>
  );
}
