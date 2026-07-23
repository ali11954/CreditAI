'use client';

import * as React from 'react';
import { Check, ChevronsUpDown, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { cn } from '@/lib/utils';

interface Option {
  label: string;
  value: string;
}

interface MultiSelectProps {
  options: Option[];
  value: string[];
  onChange: (value: string[]) => void;
  placeholder?: string;
  className?: string;
}

export function MultiSelect({
  options,
  value,
  onChange,
  placeholder = 'اختر...',
  className,
}: MultiSelectProps) {
  const [open, setOpen] = React.useState(false);

  const selectedLabels = options.filter((o) => value.includes(o.value));

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className={cn(
            'w-full justify-between font-arabic',
            value.length === 0 && 'text-muted-foreground'
          )}
        >
          {value.length > 0 ? `${value.length} محدد` : placeholder}
          <ChevronsUpDown className="h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0">
        <div className="max-h-64 overflow-auto">
          {options.map((option) => {
            const isSelected = value.includes(option.value);
            return (
              <button
                key={option.value}
                className={cn(
                  'flex w-full items-center gap-2 px-3 py-2 text-sm hover:bg-muted font-arabic',
                  isSelected && 'bg-muted'
                )}
                onClick={() => {
                  if (isSelected) {
                    onChange(value.filter((v) => v !== option.value));
                  } else {
                    onChange([...value, option.value]);
                  }
                }}
              >
                <div
                  className={cn(
                    'flex h-4 w-4 items-center justify-center rounded-sm border',
                    isSelected ? 'bg-primary text-primary-foreground' : 'opacity-50'
                  )}
                >
                  {isSelected && <Check className="h-3 w-3" />}
                </div>
                {option.label}
              </button>
            );
          })}
        </div>
      </PopoverContent>
    </Popover>
  );
}
