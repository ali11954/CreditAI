'use client';

import * as React from 'react';
import { Search, Check, ChevronsUpDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
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

interface SearchSelectProps {
  options: Option[];
  value?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  searchPlaceholder?: string;
  className?: string;
  disabled?: boolean;
}

export function SearchSelect({
  options,
  value,
  onChange,
  placeholder = 'اختر...',
  searchPlaceholder = 'بحث...',
  className,
  disabled,
}: SearchSelectProps) {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');

  const filtered = options.filter((o) =>
    o.label.toLowerCase().includes(search.toLowerCase())
  );

  const selectedLabel = options.find((o) => o.value === value)?.label;

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          className={cn(
            'w-full justify-between font-arabic',
            !value && 'text-muted-foreground',
            className
          )}
          disabled={disabled}
        >
          {selectedLabel || placeholder}
          <ChevronsUpDown className="h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-full p-0">
        <div className="p-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder={searchPlaceholder}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-8 font-arabic"
            />
          </div>
        </div>
        <div className="max-h-64 overflow-auto">
          {filtered.length === 0 ? (
            <div className="p-4 text-center text-sm text-muted-foreground font-arabic">
              لا توجد نتائج
            </div>
          ) : (
            filtered.map((option) => (
              <button
                key={option.value}
                className={cn(
                  'flex w-full items-center gap-2 px-3 py-2 text-sm hover:bg-muted font-arabic',
                  value === option.value && 'bg-muted'
                )}
                onClick={() => {
                  onChange?.(option.value);
                  setOpen(false);
                  setSearch('');
                }}
              >
                <Check
                  className={cn(
                    'h-4 w-4',
                    value === option.value ? 'opacity-100' : 'opacity-0'
                  )}
                />
                {option.label}
              </button>
            ))
          )}
        </div>
      </PopoverContent>
    </Popover>
  );
}
