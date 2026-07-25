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
import { ClipboardList, Plus, Search, Eye, Truck, CheckCircle } from 'lucide-react';
import api from '@/lib/api';

interface SalesOrder {
  id: string;
  order_number: string;
  customer_name: string;
  order_date: string;
  delivery_date: string;
  total_amount: number;
  status: string;
}

export default function SalesOrdersPage() {
  const [orders, setOrders] = useState<SalesOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [showNew, setShowNew] = useState(false);

  useEffect(() => { loadOrders(); }, []);

  const loadOrders = async () => {
    try {
      const res = await api.get('/sales/');
      setOrders(res.data.items || []);
    } catch { setOrders([]); } finally { setLoading(false); }
  };

  const filtered = orders.filter(o => {
    const ms = !search || o.customer_name?.toLowerCase().includes(search.toLowerCase()) || o.order_number?.toLowerCase().includes(search.toLowerCase());
    const mf = statusFilter === 'all' || o.status === statusFilter;
    return ms && mf;
  });

  const statusColor = (s: string) => {
    switch (s) {
      case 'delivered': return 'bg-green-100 text-green-800';
      case 'approved': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'draft': return 'bg-gray-100 text-gray-800';
      case 'invoiced': return 'bg-purple-100 text-purple-800';
      case 'closed': return 'bg-emerald-100 text-emerald-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const statusLabel = (s: string) => {
    const labels: Record<string, string> = { draft: 'مسودة', pending: 'قيد المراجعة', approved: 'معتمد', released: 'محرر', delivered: 'تم التسليم', invoicing: 'تم الفوترة', invoiced: 'مفوتر', closed: 'مغلق' };
    return labels[s] || s;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
            <ClipboardList className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold font-arabic">أوامر البيع</h1>
            <p className="text-sm text-muted-foreground font-arabic">إدارة أوامر البيع من الإصدار إلى التسليم</p>
          </div>
        </div>
        <Dialog open={showNew} onOpenChange={setShowNew}>
          <DialogTrigger asChild>
            <Button className="font-arabic"><Plus className="mr-2 h-4 w-4" />أمر بيع جديد</Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl">
            <DialogHeader><DialogTitle className="font-arabic">أمر بيع جديد</DialogTitle></DialogHeader>
            <div className="grid grid-cols-2 gap-4 py-4">
              <div className="space-y-2"><Label className="font-arabic">العميل</Label><Input placeholder="اسم العميل" /></div>
              <div className="space-y-2"><Label className="font-arabic">رقم أمر البيع</Label><Input placeholder="SO-001" /></div>
              <div className="space-y-2"><Label className="font-arabic">تاريخ الأمر</Label><Input type="date" /></div>
              <div className="space-y-2"><Label className="font-arabic">تاريخ التسليم المتوقع</Label><Input type="date" /></div>
              <div className="space-y-2"><Label className="font-arabic">المخزن</Label><Input placeholder="المخزن" /></div>
              <div className="space-y-2"><Label className="font-arabic">السائق</Label><Input placeholder="اسم السائق" /></div>
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
            <SelectItem value="pending">قيد المراجعة</SelectItem>
            <SelectItem value="approved">معتمد</SelectItem>
            <SelectItem value="delivered">تم التسليم</SelectItem>
            <SelectItem value="invoiced">مفوتر</SelectItem>
            <SelectItem value="closed">مغلق</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="font-arabic">رقم الأمر</TableHead>
                <TableHead className="font-arabic">العميل</TableHead>
                <TableHead className="font-arabic">تاريخ الأمر</TableHead>
                <TableHead className="font-arabic">تاريخ التسليم</TableHead>
                <TableHead className="font-arabic">المبلغ</TableHead>
                <TableHead className="font-arabic">الحالة</TableHead>
                <TableHead className="font-arabic">إجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                <TableRow><TableCell colSpan={7} className="text-center py-8 font-arabic">جاري التحميل...</TableCell></TableRow>
              ) : filtered.length === 0 ? (
                <TableRow><TableCell colSpan={7} className="text-center py-8 font-arabic">لا توجد أوامر بيع</TableCell></TableRow>
              ) : filtered.map(o => (
                <TableRow key={o.id}>
                  <TableCell className="font-mono text-sm">{o.order_number}</TableCell>
                  <TableCell className="font-arabic">{o.customer_name}</TableCell>
                  <TableCell>{o.order_date}</TableCell>
                  <TableCell>{o.delivery_date}</TableCell>
                  <TableCell className="font-arabic">{o.total_amount?.toLocaleString()}</TableCell>
                  <TableCell><Badge className={statusColor(o.status)}>{statusLabel(o.status)}</Badge></TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <Button variant="ghost" size="icon"><Eye className="h-4 w-4" /></Button>
                      {o.status === 'approved' && <Button variant="ghost" size="icon"><Truck className="h-4 w-4" /></Button>}
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
