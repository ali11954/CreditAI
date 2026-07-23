'use client';

import { useState, useEffect, useCallback } from 'react';
import { PageHeader } from '@/components/layout/page-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import api from '@/lib/api';

export default function SettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [settings, setSettings] = useState({
    system_name: 'CreditAI Enterprise',
    language: 'ar',
    timezone: 'asia/jerusalem',
    two_factor_auth: false,
    data_encryption: true,
    session_timeout: 60,
    email_notifications: true,
    system_notifications: true,
    credit_alerts: true,
    sap_integration: true,
    email_service: true,
  });

  const fetchSettings = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.get('/settings/system');
      if (res.data) {
        setSettings(prev => ({ ...prev, ...res.data }));
      }
    } catch (err: any) {
      setError('فشل في تحميل الإعدادات');
      toast.error('فشل في تحميل إعدادات النظام');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchSettings(); }, [fetchSettings]);

  const handleSave = async (tab: string) => {
    setSaving(true);
    try {
      await api.put('/settings/system', settings);
      toast.success('تم حفظ الإعدادات بنجاح');
    } catch (err: any) {
      toast.error('حدث خطأ أثناء الحفظ');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Settings"
        titleAr="الإعدادات"
        description="System configuration"
        descriptionAr="إعدادات النظام"
      />

      {error && <div className="text-destructive text-sm font-arabic">{error}</div>}

      <Tabs defaultValue="general" className="w-full">
        <TabsList>
          <TabsTrigger value="general" className="font-arabic">عام</TabsTrigger>
          <TabsTrigger value="security" className="font-arabic">الأمان</TabsTrigger>
          <TabsTrigger value="notifications" className="font-arabic">الإشعارات</TabsTrigger>
          <TabsTrigger value="integrations" className="font-arabic">التكامل</TabsTrigger>
        </TabsList>
        <TabsContent value="general" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">معلومات النظام</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label className="font-arabic">اسم النظام</Label>
                  <Input value={settings.system_name} onChange={(e) => setSettings({ ...settings, system_name: e.target.value })} />
                </div>
                <div className="space-y-2">
                  <Label className="font-arabic">اللغة الافتراضية</Label>
                  <Select value={settings.language} onValueChange={(v) => setSettings({ ...settings, language: v })}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ar">العربية</SelectItem>
                      <SelectItem value="en">English</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="space-y-2">
                <Label className="font-arabic">المنطقة الزمنية</Label>
                <Select value={settings.timezone} onValueChange={(v) => setSettings({ ...settings, timezone: v })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="asia/jerusalem">القدس (GMT+2)</SelectItem>
                    <SelectItem value="asia/dubai">دبي (GMT+4)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <Button className="font-arabic" onClick={() => handleSave('general')} disabled={saving}>
                {saving ? <Loader2 className="ml-2 h-4 w-4 animate-spin" /> : null}
                حفظ التغييرات
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="security" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">إعدادات الأمان</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium font-arabic">المصادقة الثنائية</p>
                  <p className="text-sm text-muted-foreground font-arabic">تتفعيل للحسابات الجديدة</p>
                </div>
                <Switch checked={settings.two_factor_auth} onCheckedChange={(v) => setSettings({ ...settings, two_factor_auth: v })} />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium font-arabic">تشفير البيانات</p>
                  <p className="text-sm text-muted-foreground font-arabic">تشفير البيانات الحساسة</p>
                </div>
                <Switch checked={settings.data_encryption} onCheckedChange={(v) => setSettings({ ...settings, data_encryption: v })} />
              </div>
              <div className="space-y-2">
                <Label className="font-arabic">مدة انتهاء الجلسة (دقائق)</Label>
                <Input type="number" value={settings.session_timeout} onChange={(e) => setSettings({ ...settings, session_timeout: parseInt(e.target.value) || 60 })} className="w-32" />
              </div>
              <Button className="font-arabic" onClick={() => handleSave('security')} disabled={saving}>
                {saving ? <Loader2 className="ml-2 h-4 w-4 animate-spin" /> : null}
                حفظ
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="notifications" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">إعدادات الإشعارات</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <p className="font-medium font-arabic">إشعارات البريد الإلكتروني</p>
                <Switch checked={settings.email_notifications} onCheckedChange={(v) => setSettings({ ...settings, email_notifications: v })} />
              </div>
              <div className="flex items-center justify-between">
                <p className="font-medium font-arabic">إشعارات النظام</p>
                <Switch checked={settings.system_notifications} onCheckedChange={(v) => setSettings({ ...settings, system_notifications: v })} />
              </div>
              <div className="flex items-center justify-between">
                <p className="font-medium font-arabic">تنبيهات الائتمان</p>
                <Switch checked={settings.credit_alerts} onCheckedChange={(v) => setSettings({ ...settings, credit_alerts: v })} />
              </div>
              <Button className="font-arabic" onClick={() => handleSave('notifications')} disabled={saving}>
                {saving ? <Loader2 className="ml-2 h-4 w-4 animate-spin" /> : null}
                حفظ
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
        <TabsContent value="integrations" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="font-arabic">التكاملات</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between rounded-md border p-4">
                <div>
                  <p className="font-medium font-arabic">تكامل SAP</p>
                  <p className="text-sm text-muted-foreground font-arabic">مزامنة البيانات مع نظام SAP</p>
                </div>
                <Switch checked={settings.sap_integration} onCheckedChange={(v) => setSettings({ ...settings, sap_integration: v })} />
              </div>
              <div className="flex items-center justify-between rounded-md border p-4">
                <div>
                  <p className="font-medium font-arabic">خدمة البريد الإلكتروني</p>
                  <p className="text-sm text-muted-foreground font-arabic">إرسال الإشعارات عبر البريد</p>
                </div>
                <Switch checked={settings.email_service} onCheckedChange={(v) => setSettings({ ...settings, email_service: v })} />
              </div>
              <Button className="font-arabic" onClick={() => handleSave('integrations')} disabled={saving}>
                {saving ? <Loader2 className="ml-2 h-4 w-4 animate-spin" /> : null}
                حفظ
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
