'use client';

import { useState } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Brain, TrendingUp, AlertTriangle, BarChart3, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/lib/api';
import { CustomerSelect } from '@/components/ui/customer-select';

const aiFeatures = [
  { id: 'analyze-customer', title: 'تحليل المخاطر', titleEn: 'Risk Analysis', description: 'تحليل ذكي لمستويات المخاطر بناء على البيانات التاريخية', icon: Brain, color: 'text-purple-500', accuracy: '94%', endpoint: '/ai/analyze-customer' },
  { id: 'credit-score', title: 'التنبؤ بالتحصيل', titleEn: 'Collection Prediction', description: 'التنبؤ باحتمالية التحصيل لكل عميل', icon: TrendingUp, color: 'text-green-500', accuracy: '87%', endpoint: '/ai/credit-score' },
  { id: 'risk-assessment', title: 'كشف الاحتيال', titleEn: 'Fraud Detection', description: 'كشف المعاملات المشبوهة والاحتيال', icon: AlertTriangle, color: 'text-red-500', accuracy: '91%', endpoint: '/ai/risk-assessment' },
  { id: 'segmentation', title: 'تصنيف العملاء', titleEn: 'Customer Segmentation', description: 'تصنيف العملاء بناء على سلوكهم الائتماني', icon: BarChart3, color: 'text-blue-500', accuracy: '89%', endpoint: '/ai/analyze-customer' },
];

export default function AICenterPage() {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedFeature, setSelectedFeature] = useState<any>(null);
  const [customerId, setCustomerId] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!customerId || !selectedFeature) {
      toast.error('يرجى اختيار العميل');
      return;
    }
    setAnalyzing(true);
    setResult(null);
    try {
      const res = await api.post(selectedFeature.endpoint, { customer_id: customerId });
      setResult(res.data);
      toast.success('تم التحليل بنجاح');
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'خطأ غير معروف';
      toast.error('حدث خطأ: ' + msg);
      console.error('AI Analysis error:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const openDialog = (feature: any) => {
    setSelectedFeature(feature);
    setCustomerId('');
    setResult(null);
    setDialogOpen(true);
  };

  const renderResult = (data: any) => {
    if (!data) return null;
    const entries = Object.entries(data).filter(([k]) => !k.startsWith('_'));
    return (
      <div className="space-y-2">
        {entries.map(([key, value]) => {
          if (value === null || value === undefined) return null;
          if (typeof value === 'object' && !Array.isArray(value)) {
            return (
              <div key={key} className="border rounded p-2">
                <p className="text-xs font-bold text-muted-foreground mb-1">{key}</p>
                <div className="pl-2">{renderResult(value)}</div>
              </div>
            );
          }
          if (Array.isArray(value)) {
            return (
              <div key={key} className="border rounded p-2">
                <p className="text-xs font-bold text-muted-foreground mb-1">{key}</p>
                <ul className="pl-4 list-disc text-sm">
                  {value.map((v: any, i: number) => (
                    <li key={i}>{typeof v === 'object' ? JSON.stringify(v) : String(v)}</li>
                  ))}
                </ul>
              </div>
            );
          }
          return (
            <div key={key} className="flex justify-between text-sm border-b pb-1">
              <span className="text-muted-foreground">{key}</span>
              <span className="font-medium">{String(value)}</span>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="AI Center"
        titleAr="مركز الذكاء الاصطناعي"
        description="AI-powered analytics and insights"
        descriptionAr="تحليلات ورؤى مدعومة بالذكاء الاصطناعي"
      />

      <div className="grid gap-4 md:grid-cols-2">
        {aiFeatures.map((feature) => {
          const Icon = feature.icon;
          return (
            <Card key={feature.id} className="hover-lift">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Icon className={`h-8 w-8 ${feature.color}`} />
                    <div>
                      <CardTitle className="font-arabic">{feature.title}</CardTitle>
                      <p className="text-xs text-muted-foreground">{feature.titleEn}</p>
                    </div>
                  </div>
                  <Badge variant="success">{feature.accuracy}</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground font-arabic mb-4">{feature.description}</p>
                <Button variant="outline" className="w-full font-arabic" onClick={() => openDialog(feature)}>
                  تشغيل التحليل
                </Button>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="font-arabic max-w-lg">
          <DialogHeader>
            <DialogTitle>{selectedFeature?.title || 'تحليل'}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label>العميل *</Label>
              <CustomerSelect value={customerId} onChange={(v) => setCustomerId(v)} />
            </div>
            <Button className="w-full font-arabic" onClick={handleAnalyze} disabled={analyzing || !customerId}>
              {analyzing ? (
                <>
                  <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                  جاري التحليل...
                </>
              ) : (
                'تشغيل التحليل'
              )}
            </Button>
            {result && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm font-arabic">نتائج التحليل</CardTitle>
                </CardHeader>
                <CardContent className="max-h-96 overflow-y-auto">
                  {renderResult(result)}
                </CardContent>
              </Card>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
