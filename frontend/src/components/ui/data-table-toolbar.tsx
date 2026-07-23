'use client';

import { useState, useEffect, useCallback } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Search, Plus, RefreshCw } from 'lucide-react';
import { ExportButtons } from '@/components/ui/export-buttons';

interface StatusOption {
  label: string;
  value: string;
}

interface DataTableToolbarProps {
  search: string;
  onSearchChange: (value: string) => void;
  status: string;
  onStatusChange: (value: string) => void;
  statusOptions?: StatusOption[];
  onAddNew?: () => void;
  addNewLabel?: string;
  addNewLabelAr?: string;
  onRefresh?: () => void;
  exportData?: any[];
  exportColumns?: { key: string; label: string }[];
  exportFilename?: string;
  exportTitle?: string;
  exportEndpoint?: string;
}

export function DataTableToolbar({
  search,
  onSearchChange,
  status,
  onStatusChange,
  statusOptions = [],
  onAddNew,
  addNewLabel = 'Add New',
  addNewLabelAr = 'إضافة جديد',
  onRefresh,
  exportData = [],
  exportColumns,
  exportFilename,
  exportTitle,
  exportEndpoint,
}: DataTableToolbarProps) {
  const [searchInput, setSearchInput] = useState(search);

  useEffect(() => {
    setSearchInput(search);
  }, [search]);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchInput !== search) {
        onSearchChange(searchInput);
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [searchInput, search, onSearchChange]);

  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-1 items-center gap-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="بحث..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="pl-9"
          />
        </div>
        {statusOptions.length > 0 && (
          <Select value={status} onValueChange={onStatusChange}>
            <SelectTrigger className="w-[160px]">
              <SelectValue placeholder="الحالة" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">جميع الحالات</SelectItem>
              {statusOptions.map((opt) => (
                <SelectItem key={opt.value} value={opt.value}>
                  {opt.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        )}
        {onRefresh && (
          <Button variant="outline" size="icon" onClick={onRefresh}>
            <RefreshCw className="h-4 w-4" />
          </Button>
        )}
      </div>
      <div className="flex items-center gap-2">
        {exportData.length > 0 && exportEndpoint && exportColumns && exportFilename && (
          <ExportButtons
            data={exportData}
            columns={exportColumns}
            filename={exportFilename}
            title={exportTitle || exportFilename}
            endpoint={exportEndpoint}
          />
        )}
        {onAddNew && (
          <Button onClick={onAddNew}>
            <Plus className="ml-1 h-4 w-4" />
            {addNewLabelAr}
          </Button>
        )}
      </div>
    </div>
  );
}
