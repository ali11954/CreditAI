'use client';

import { useState, useEffect } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import api from '@/lib/api';

interface Customer {
  id: string;
  customer_code: string;
  name: string;
  name_ar?: string;
}

interface CustomerSelectProps {
  value?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
}

export function CustomerSelect({ value, onChange, placeholder = "اختر العميل", disabled = false }: CustomerSelectProps) {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const res = await api.get('/customers/', { params: { page: 1, page_size: 100 } });
      setCustomers(res.data.items || []);
    } catch (error) {
      console.error('Failed to fetch customers');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Select value={value} onValueChange={onChange} disabled={disabled || loading}>
      <SelectTrigger className="w-full">
        <SelectValue placeholder={loading ? "جاري التحميل..." : placeholder} />
      </SelectTrigger>
      <SelectContent>
        {customers.map((customer) => (
          <SelectItem key={customer.id} value={customer.id}>
            {customer.customer_code} - {customer.name_ar || customer.name}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

export default CustomerSelect;
