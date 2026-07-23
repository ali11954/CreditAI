'use client';

import { useParams } from 'next/navigation';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Edit, ArrowRight, FileText, CreditCard, Building2 } from 'lucide-react';
import Link from 'next/link';

export default function CustomerDetailPage() {
  const params = useParams();
  const customerId = params.id;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Customer Details"
        titleAr="تفاصيل العميل"
        actions={
          <div className="flex gap-2">
            <Link href="/customers">
              <Button variant="outline" className="font-arabic">
                <ArrowRight className="ml-2 h-4 w-4" /> رجوع
              </Button>
            </Link>
            <Button className="font-arabic">
              <Edit className="ml-2 h-4 w-4" /> تعديل
            </Button>
          </div>
        }
      />

      <div className="grid gap-6 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Building2 className="h-8 w-8 text-primary" />
              <div>
                <p className="text-2xl font-bold">5</p>
                <p className="text-sm text-muted-foreground font-arabic">العملاء</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <FileText className="h-8 w-8 text-blue-500" />
              <div>
                <p className="text-2xl font-bold">12</p>
                <p className="text-sm text-muted-foreground font-arabic">الطلبات</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <CreditCard className="h-8 w-8 text-green-500" />
              <div>
                <p className="text-2xl font-bold">₪ 2.5M</p>
                <p className="text-sm text-muted-foreground font-arabic">الحد الائتماني</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Building2 className="h-8 w-8 text-yellow-500" />
              <div>
                <p className="text-2xl font-bold">₪ 1.8M</p>
                <p className="text-sm text-muted-foreground font-arabic">المستخدم</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList>
          <TabsTrigger value="overview" className="font-arabic">نظرة عامة</TabsTrigger>
          <TabsTrigger value="credit" className="font-arabic">الائتمان</TabsTrigger>
          <TabsTrigger value="documents" className="font-arabic">الوثائق</TabsTrigger>
          <TabsTrigger value="payments" className="font-arabic">المدفوعات</TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">معلومات الشركة</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 md:grid-cols-2">
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">اسم الشركة</p>
                <p className="font-medium font-arabic">شركة الأمل</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">رقم السجل التجاري</p>
                <p className="font-medium" dir="ltr">12345678</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">جهة الاتصال</p>
                <p className="font-medium font-arabic">خالد محمد</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">الحالة</p>
                <Badge variant="success">نشط</Badge>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">مستوى المخاطر</p>
                <Badge variant="success">منخفض</Badge>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground font-arabic">النتيجة الائتمانية</p>
                <p className="font-medium">750</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="credit">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">طلبات الائتمان</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground font-arabic">قائمة طلبات الائتمان لهذا العميل</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="documents">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">الوثائق</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground font-arabic">الوثائق المرفقة بالعميل</p>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="payments">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">المدفوعات</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground font-arabic">سجل المدفوعات</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
