'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { downloadBlob, apiClient } from '@/lib/api-client';
import { toast } from 'sonner';
import { FileSpreadsheet, FileText, FileDown, Loader2 } from 'lucide-react';

interface ExportButtonsProps {
  data: any[];
  columns: { key: string; label: string }[];
  filename: string;
  title: string;
  endpoint: string;
}

export function ExportButtons({
  data,
  columns,
  filename,
  title,
  endpoint,
}: ExportButtonsProps) {
  const [exporting, setExporting] = useState<'excel' | 'pdf' | 'csv' | null>(null);

  const handleExport = async (format: 'excel' | 'pdf' | 'csv') => {
    if (data.length === 0) {
      toast.error('لا توجد بيانات للتصدير');
      return;
    }
    setExporting(format);
    try {
      let blob: Blob;
      switch (format) {
        case 'excel':
          blob = await apiClient.exportExcel(endpoint, data, columns, filename);
          downloadBlob(blob, `${filename}.xlsx`);
          break;
        case 'pdf':
          blob = await apiClient.exportPdf(endpoint, data, columns, filename, title);
          downloadBlob(blob, `${filename}.pdf`);
          break;
        case 'csv':
          blob = await apiClient.exportCsv(endpoint, data, columns, filename);
          downloadBlob(blob, `${filename}.csv`);
          break;
      }
      toast.success('تم التصدير بنجاح');
    } catch {
      toast.error('حدث خطأ أثناء التصدير');
    } finally {
      setExporting(null);
    }
  };

  return (
    <div className="flex items-center gap-1">
      <Button
        variant="outline"
        size="sm"
        onClick={() => handleExport('excel')}
        disabled={exporting !== null}
      >
        {exporting === 'excel' ? (
          <Loader2 className="ml-1 h-4 w-4 animate-spin" />
        ) : (
          <FileSpreadsheet className="ml-1 h-4 w-4" />
        )}
        Excel
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={() => handleExport('pdf')}
        disabled={exporting !== null}
      >
        {exporting === 'pdf' ? (
          <Loader2 className="ml-1 h-4 w-4 animate-spin" />
        ) : (
          <FileText className="ml-1 h-4 w-4" />
        )}
        PDF
      </Button>
      <Button
        variant="outline"
        size="sm"
        onClick={() => handleExport('csv')}
        disabled={exporting !== null}
      >
        {exporting === 'csv' ? (
          <Loader2 className="ml-1 h-4 w-4 animate-spin" />
        ) : (
          <FileDown className="ml-1 h-4 w-4" />
        )}
        CSV
      </Button>
    </div>
  );
}
