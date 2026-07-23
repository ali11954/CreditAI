'use client';

import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { FileUpload } from '@/components/forms/file-upload';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';

interface UploadDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  folder?: string;
  accept?: string;
  multiple?: boolean;
  onUpload: (files: File[]) => Promise<void>;
}

export function UploadDialog({
  open,
  onOpenChange,
  folder,
  accept = '*',
  multiple = false,
  onUpload,
}: UploadDialogProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    if (files.length === 0) {
      toast.error('يرجى اختيار ملف واحد على الأقل');
      return;
    }
    setIsUploading(true);
    try {
      await onUpload(files);
      toast.success('تم الرفع بنجاح');
      setFiles([]);
      onOpenChange(false);
    } catch {
      toast.error('حدث خطأ أثناء رفع الملفات');
    } finally {
      setIsUploading(false);
    }
  };

  const handleClose = () => {
    if (!isUploading) {
      setFiles([]);
      onOpenChange(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>رفع الملفات</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <FileUpload
            accept={accept}
            multiple={multiple}
            onFilesChange={setFiles}
          />
        </div>
        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={handleClose}
            disabled={isUploading}
          >
            إلغاء
          </Button>
          <Button onClick={handleUpload} disabled={isUploading || files.length === 0}>
            {isUploading ? (
              <>
                <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                جاري الرفع...
              </>
            ) : (
              'رفع'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
