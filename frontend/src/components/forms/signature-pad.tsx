'use client';

import * as React from 'react';
import SignatureCanvas from 'react-signature-canvas';
import { Button } from '@/components/ui/button';
import { Eraser } from 'lucide-react';

interface SignaturePadProps {
  onSave?: (dataUrl: string) => void;
  width?: number;
  height?: number;
  className?: string;
}

export function SignaturePad({
  onSave,
  width = 400,
  height = 200,
  className,
}: SignaturePadProps) {
  const canvasRef = React.useRef<SignatureCanvas>(null);

  const handleClear = () => {
    canvasRef.current?.clear();
  };

  const handleSave = () => {
    if (canvasRef.current) {
      const dataUrl = canvasRef.current.toDataURL();
      onSave?.(dataUrl);
    }
  };

  return (
    <div className={cn('space-y-2', className)}>
      <div className="rounded-md border bg-white">
        <SignatureCanvas
          ref={canvasRef}
          canvasProps={{ width, height, className: 'w-full' }}
          backgroundColor="rgb(255, 255, 255)"
        />
      </div>
      <div className="flex gap-2">
        <Button variant="outline" size="sm" onClick={handleClear} className="font-arabic">
          <Eraser className="mr-2 h-4 w-4" /> مسح
        </Button>
        <Button size="sm" onClick={handleSave} className="font-arabic">
          حفظ التوقيع
        </Button>
      </div>
    </div>
  );
}

function cn(...classes: (string | undefined | false)[]) {
  return classes.filter(Boolean).join(' ');
}
