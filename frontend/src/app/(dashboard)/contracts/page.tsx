'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { FileSignature, Plus, Search, Eye, Edit, Calendar, AlertTriangle } from 'lucide-react';
import api from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

interface Contract {
  id: string;
  contract_number: string;
  customer_name: string;
  title: string;
  contract_type: string;
  start_date: string;
  end_date: string;
  total_amount: number;
  status: string;
  created_at: string;
}

export default function ContractsPage() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [showNew, setShowNew] = useState(false);
  const { toast } = useToast();

  useEffect(() => { loadContracts(); }, []);

  const loadContracts = async () => {
    try {
      const res = await api.get('/credit-applications/');
      setContracts(res.data.items || []);
    } catch {
      setContracts([]);
    } finally {
      setLoading(false);
    }
  };

  const filtered = contracts.filter(c => {
    const matchSearch = !search || c.customer_name?.toLowerCase().includes(search.toLowerCase()) || c.contract_number?.toLowerCase().includes(search.toLowerCase());
    const matchStatus = statusFilter === 'all' || c.status === statusFilter;
    return matchSearch && matchStatus;
  });

  const statusColor = (s: string) => {
    switch (s) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'expired': return 'bg-red-100 text-red-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
            <FileSignature className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold font-arabic">إدارة العقود</h1>
            <p className="text-sm text-muted-foreground font-arabic">إنشاء وإدارة ومتابعة العقود</p>
          </div>
        </div>
        <Dialog open={showNew} onOpenChange={setShowNew}>
          <DialogTrigger asChild>
            <Button className="font-arabic"><Plus className="mr-2 h-4 w-4" />عقد جديد</Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader><DialogTitle className="font-arabic">إنشاء عقد جديد</DialogTitle></DialogHeader>
            <div className="grid grid-cols-2 gap-4 py-4">
              <div className="space-y-2"><Label className="font-arabic">رقم العقد</Label><Input placeholder="CTR-001" /></div>
              <div className="space-y-2"><Label className="font-arabic">العميل</Label><Input placeholder="اسم العميل" /></div>
              <div className="col-span-2 space-y-2"><Label className="font-arabic">عنوان العقد</Label><Input placeholder="عنوان العقد" /></div>
              <div className="space-y-2"><Label className="font-arabic">نوع العقد</Label>
                <Select><SelectTrigger><SelectValue placeholder="اختر النوع" /></SelectTrigger>
                  <SelectContent><SelectItem value="sales">بيع</SelectItem><SelectItem value="service">خدمة</SelectItem><SelectItem value="supply">توريد</SelectItem></SelectContent>
                </Select>
              </div>
              <div className="space-y-2"><Label className="font-arabic">المبلغ الإجمالي</Label><Input type="number" placeholder="0" /></div>
              <div className="space-y-2"><Label className="font-arabic">تاريخ البداية</Label><Input type="date" /></div>
              <div className="space-y-2"><Label className="font-arabic">تاريخ النهاية</Label><Input type="date" /></div>
              <div className="col-span-2 space-y-2"><Label className="font-arabic">ملاحظات</Label><Textarea placeholder="تفاصيل العقد" /></div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="بحث بالاسم أو رقم العقد..." className="pl-10 font-arabic" value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-40 font-arabic"><SelectValue placeholder="الحالة" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">الكل</SelectItem>
            <SelectItem value="active">نشط</SelectItem>
            <SelectItem value="pending">معلق</SelectItem>
            <SelectItem value="expired">منتهي</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="font-arabic">رقم العقد</TableHead>
                <TableHead className="font-arabic">العميل</TableHead>
                <TableHead className="font-arabic">النوع</TableHead>
                <TableHead className="font-arabic">المبلغ</TableHead>
                <TableHead className="font-arabic">تاريخ البداية</TableHead>
                <TableHead className="font-arabic">تاريخ النهاية</TableHead>
                <TableHead className="font-arabic">الحالة</TableHead>
                <TableHead className="font-arabic">إجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow><TableCell colSpan={8} className="text-center py-8 font-arabic">جاري التحميل...</TableCell></TableRow>
              ) : filtered.length === 0 ? (
                <TableRow><TableCell colSpan={8} className="text-center py-8 font-arabic">لا توجد عقود</TableCell></TableRow>
              ) : filtered.map(c => (
                <TableRow key={c.id}>
                  <TableCell className="font-mono text-sm">{c.contract_number}</TableCell>
                  <TableCell className="font-arabic">{c.customer_name}</TableCell>
                  <TableCell className="font-arabic">{c.contract_type}</TableCell>
                  <TableCell className="font-arabic">{c.total_amount?.toLocaleString()}</TableCell>
                  <TableCell>{c.start_date}</TableCell>
                  <TableCell>{c.end_date}</TableCell>
                  <TableCell><Badge className={statusColor(c.status)}>{c.status}</Badge></TableCell>
                  <TableCell>
                    <Button variant="ghost" size="icon"><Eye className="h-4 w-4" /></Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
