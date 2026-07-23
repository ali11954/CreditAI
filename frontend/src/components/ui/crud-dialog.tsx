'use client';

import { useEffect, useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Checkbox } from '@/components/ui/checkbox';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Loader2 } from 'lucide-react';

export type FieldType = 'text' | 'number' | 'email' | 'phone' | 'select' | 'date' | 'textarea' | 'checkbox';

export interface FieldOption {
  label: string;
  value: string;
}

export interface FieldConfig {
  key: string;
  label: string;
  labelAr: string;
  type: FieldType;
  placeholder?: string;
  placeholderAr?: string;
  required?: boolean;
  options?: FieldOption[];
  defaultValue?: any;
  disabled?: boolean;
  className?: string;
}

interface CrudDialogProps<T> {
  mode: 'create' | 'edit';
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  titleAr: string;
  fields: FieldConfig[];
  data?: Partial<T>;
  onSubmit: (data: any) => Promise<void>;
}

export function CrudDialog<T>({
  mode,
  open,
  onOpenChange,
  title,
  titleAr,
  fields,
  data,
  onSubmit,
}: CrudDialogProps<T>) {
  const [formData, setFormData] = useState<Record<string, any>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (open) {
      const initial: Record<string, any> = {};
      fields.forEach((field) => {
        if (mode === 'edit' && data && (data as any)[field.key] !== undefined) {
          initial[field.key] = (data as any)[field.key];
        } else {
          initial[field.key] = field.defaultValue ?? '';
        }
      });
      setFormData(initial);
    }
  }, [open, mode, data, fields]);

  const handleChange = (key: string, value: any) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onSubmit(formData);
      onOpenChange(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderField = (field: FieldConfig) => {
    const value = formData[field.key] ?? '';

    switch (field.type) {
      case 'textarea':
        return (
          <Textarea
            id={field.key}
            value={value}
            onChange={(e) => handleChange(field.key, e.target.value)}
            placeholder={field.placeholderAr || field.placeholder}
            disabled={field.disabled}
            className={field.className}
          />
        );

      case 'select':
        return (
          <Select
            value={value}
            onValueChange={(v) => handleChange(field.key, v)}
            disabled={field.disabled}
          >
            <SelectTrigger className={field.className}>
              <SelectValue placeholder={field.placeholderAr || field.placeholder} />
            </SelectTrigger>
            <SelectContent>
              {field.options?.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        );

      case 'checkbox':
        return (
          <div className="flex items-center gap-2">
            <Checkbox
              id={field.key}
              checked={!!value}
              onCheckedChange={(checked) => handleChange(field.key, checked)}
              disabled={field.disabled}
            />
            <Label htmlFor={field.key} className="cursor-pointer">
              {field.labelAr}
            </Label>
          </div>
        );

      case 'number':
        return (
          <Input
            id={field.key}
            type="number"
            value={value}
            onChange={(e) => handleChange(field.key, e.target.value ? Number(e.target.value) : '')}
            placeholder={field.placeholderAr || field.placeholder}
            disabled={field.disabled}
            className={field.className}
          />
        );

      case 'date':
        return (
          <Input
            id={field.key}
            type="date"
            value={value}
            onChange={(e) => handleChange(field.key, e.target.value)}
            disabled={field.disabled}
            className={field.className}
          />
        );

      default:
        return (
          <Input
            id={field.key}
            type={field.type === 'email' ? 'email' : field.type === 'phone' ? 'tel' : 'text'}
            value={value}
            onChange={(e) => handleChange(field.key, e.target.value)}
            placeholder={field.placeholderAr || field.placeholder}
            disabled={field.disabled}
            className={field.className}
          />
        );
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>
            {mode === 'create' ? `إضافة ${titleAr}` : `تعديل ${titleAr}`}
          </DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          {fields.map((field) => (
            <div key={field.key} className="space-y-2">
              {field.type !== 'checkbox' && (
                <Label htmlFor={field.key}>
                  {field.labelAr}
                  {field.required && <span className="mr-1 text-destructive">*</span>}
                </Label>
              )}
              {renderField(field)}
            </div>
          ))}
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isSubmitting}
            >
              إلغاء
            </Button>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                  جاري الحفظ...
                </>
              ) : mode === 'create' ? (
                'إضافة'
              ) : (
                'حفظ'
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
