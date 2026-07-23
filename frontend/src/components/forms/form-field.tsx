'use client';

import * as React from 'react';
import { FieldPath, FieldValues, UseFormReturn } from 'react-hook-form';
import { Label } from '@/components/ui/label';
import { cn } from '@/lib/utils';

interface FormFieldProps<T extends FieldValues> {
  form: UseFormReturn<T>;
  name: FieldPath<T>;
  label: string;
  labelAr?: string;
  description?: string;
  required?: boolean;
  children: (field: any) => React.ReactNode;
  className?: string;
}

export function FormField<T extends FieldValues>({
  form,
  name,
  label,
  labelAr,
  description,
  required,
  children,
  className,
}: FormFieldProps<T>) {
  const error = form.formState.errors[name];

  return (
    <div className={cn('space-y-2', className)}>
      <Label htmlFor={name} className="font-arabic">
        {labelAr || label}
        {required && <span className="mr-1 text-destructive">*</span>}
      </Label>
      {children(form.register(name))}
      {description && (
        <p className="text-xs text-muted-foreground font-arabic">{description}</p>
      )}
      {error && (
        <p className="text-sm text-destructive font-arabic">
          {error.message as string}
        </p>
      )}
    </div>
  );
}
