'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Receipt, Plus, Search, Eye, Send, FileDown, QrCode } from 'lucide-react';
import api from '@/lib/api';

interface Invoice {
  id: string;
  invoice_number: string;
  customer_name: string;
  invoice_date: string;
  due_date: string;
  total_amount: number;
  paid_amount: number;
  balance: number;
  status: string;
}

export default function InvoicingPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [showNew, setShowNew] = useState(false);

  useEffect(() => { loadInvoices(); }, []);

  const loadInvoices = async () => {
    try {
      const res = await api.get('/collections/invoices');
      setInvoices(res.data.items || []);
    } catch { setInvoices([]); } finally { setLoading(false); }
  };

  const filtered = invoices.filter(inv => {
    const ms = !search || inv.customer_name?.toLowerCase().includes(search.toLowerCase()) || inv.invoice_number?.toLowerCase().includes(search.toLowerCase());
    const mf = statusFilter === 'all' || inv.status === statusFilter;
    return ms && mf;
  });

  const statusColor = (s: string) => {
    switch (s) {
      case 'paid': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'overdue': return 'bg-red-100 text-red-800';
      case 'partial': return 'bg-blue-100 text-blue-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
            <Receipt className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold font-arabic">الفواتير</h1>
            <p className="text-sm text-muted-foreground font-arabic">إنشاء وإدارة الفواتير الإلكترونية</p>
          </div>
        </div>
        <Dialog open={showNew} onOpenChange={setShowNew}>
          <DialogTrigger asChild>
            <Button className="font-arabic"><Plus className="mr-2 h-4 w-4" />فاتورة جديدة</Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader><DialogTitle className="font-arabic">إنشاء فاتورة جديدة</DialogTitle></DialogHeader>
            <div className="grid grid-cols-2 gap-4 py-4">
              <div className="space-y-2"><Label className="font-arabic">العميل</Label><Input placeholder="اسم العميل" /></div>
              <div className="space-y-2"><Label className="font-arabic">رقم الفاتورة</Label><Input placeholder="INV-001" /></div>
              <div className="space-y-2"><Label className="font-arabic">تاريخ الفاتورة</Label><Input type="date" /></div>
              <div className="space-y-2"><Label className="font-arabic">تاريخ الاستحقاق</Label><Input type="date" /></div>
              <div className="space-y-2"><Label className="font-arabic">المبلغ</Label><Input type="number" placeholder="0" /></div>
              <div className="space-y-2"><Label className="font-arabic">الضريبة</Label><Input type="number" placeholder="15%" /></div>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input placeholder="بحث..." className="pl-10 font-arabic" value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-40 font-arabic"><SelectValue placeholder="الحالة" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">الكل</SelectItem>
            <SelectItem value="draft">مسودة</SelectItem>
            <SelectItem value="pending">معلقة</SelectItem>
            <SelectItem value="paid">مدفوعة</SelectItem>
            <SelectItem value="overdue">متاخرة</SelectItem>
            <SelectItem value="partial">جزئية</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="font-arabic">رقم الفاتورة</TableHead>
                <TableHead className="font-arabic">العميل</TableHead>
                <TableHead className="font-arabic">التاريخ</TableHead>
                <TableHead className="font-arabic">الاستحقاق</TableHead>
                <TableHead className="font-arabic">المبلغ</TableHead>
                <TableHead className="font-arabic">المدفوع</TableHead>
                <TableHead className="font-arabic">المتبقي</TableHead>
                <TableHead className="font-arabic">الحالة</TableHead>
                <TableHead className="font-arabic">إجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow><TableCell colSpan={9} className="text-center py-8 font-arabic">جاري التحميل...</TableCell></TableRow>
              ) : filtered.length === 0 ? (
                <TableRow><TableCell colSpan={9} className="text-center py-8 font-arabic">لا توجد فواتير</TableCell></TableRow>
              ) : filtered.map(inv => (
                <TableRow key={inv.id}>
                  <TableCell className="font-mono text-sm">{inv.invoice_number}</TableCell>
                  <TableCell className="font-arabic">{inv.customer_name}</TableCell>
                  <TableCell>{inv.invoice_date}</TableCell>
                  <TableCell>{inv.due_date}</TableCell>
                  <TableCell className="font-arabic">{inv.total_amount?.toLocaleString()}</TableCell>
                  <TableCell className="font-arabic text-green-600">{inv.paid_amount?.toLocaleString()}</TableCell>
                  <TableCell className="font-arabic text-red-600">{inv.balance?.toLocaleString()}</TableCell>
                  <TableCell><Badge className={statusColor(inv.status)}>{inv.status}</Badge></TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon" title="عرض"><Eye className="h-4 w-4" /></Button>
                      <Button variant="ghost" size="icon" title="PDF"><FileDown className="h-4 w-4" /></Button>
                      <Button variant="ghost" size="icon" title="إرسال"><Send className="h-4 w-4" /></Button>
                    </div>
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
