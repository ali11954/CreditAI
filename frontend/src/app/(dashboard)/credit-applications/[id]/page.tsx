'use client';

import { useParams } from 'next/navigation';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ArrowRight, Check, X, FileText } from 'lucide-react';
import Link from 'next/link';

export default function CreditApplicationDetailPage() {
  const params = useParams();

  return (
    <div className="space-y-6">
      <PageHeader
        title="Application Details"
        titleAr="تفاصيل الطلب"
        actions={
          <div className="flex gap-2">
            <Link href="/credit-applications">
              <Button variant="outline" className="font-arabic">
                <ArrowRight className="ml-2 h-4 w-4" /> رجوع
              </Button>
            </Link>
            <Button variant="outline" className="font-arabic text-green-600 hover:text-green-700">
              <Check className="ml-2 h-4 w-4" /> موافقة
            </Button>
            <Button variant="outline" className="font-arabic text-destructive hover:text-destructive">
              <X className="ml-2 h-4 w-4" /> رفض
            </Button>
          </div>
        }
      />

      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-3xl font-bold">₪ 500,000</p>
              <p className="text-sm text-muted-foreground font-arabic">المبلغ المطلوب</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-3xl font-bold">24 شهر</p>
              <p className="text-sm text-muted-foreground font-arabic">المدة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-center">
              <Badge variant="warning" className="text-lg">معلق</Badge>
              <p className="mt-2 text-sm text-muted-foreground font-arabic">الحالة</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="details" className="w-full">
        <TabsList>
          <TabsTrigger value="details" className="font-arabic">التفاصيل</TabsTrigger>
          <TabsTrigger value="documents" className="font-arabic">الوثائق</TabsTrigger>
          <TabsTrigger value="analysis" className="font-arabic">التحليل</TabsTrigger>
          <TabsTrigger value="history" className="font-arabic">السجل</TabsTrigger>
        </TabsList>
        <TabsContent value="details" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">معلومات العميل</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">اسم الشركة</p>
                <p className="font-medium font-arabic">شركة الأمل</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الغرض من الائتمان</p>
                <p className="font-medium font-arabic">توسيع الأعمال</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الضمان</p>
                <p className="font-medium font-arabic">عقارات</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الإيرادات السنوية</p>
                <p className="font-medium">₪ 2,000,000</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="documents">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">الوثائق المرفقة</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="flex items-center justify-between rounded-md border p-3">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    <span className="font-arabic">كشف حساب بنكي</span>
                  </div>
                  <Button variant="ghost" size="sm" className="font-arabic">تحميل</Button>
                </div>
                <div className="flex items-center justify-between rounded-md border p-3">
                  <div className="flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    <span className="font-arabic">إثبات الدخل</span>
                  </div>
                  <Button variant="ghost" size="sm" className="font-arabic">تحميل</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="analysis">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">تحليل المخاطر</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground font-arabic">تحليل الذكاء الاصطناعي للمخاطر</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="history">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">سجل الطلبات</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground font-arabic">سجل التغييرات والتحديثات</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
