declare module 'react-signature-canvas' {
  import * as React from 'react';

  interface SignatureCanvasProps {
    canvasProps?: React.CanvasHTMLAttributes<HTMLCanvasElement>;
    clearOnResize?: boolean;
    backgroundColor?: string;
    penColor?: string;
    dotSize?: number;
    minWidth?: number;
    maxWidth?: number;
    velocityFilterWeight?: number;
    onEnd?: () => void;
    onBegin?: () => void;
    velocityFilterWeight?: number;
  }

  export default class SignatureCanvas extends React.Component<SignatureCanvasProps> {
    clear(): void;
    isEmpty(): boolean;
    fromDataURL(dataUrl: string): void;
    toDataURL(): string;
  }
}
