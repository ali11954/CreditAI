'use client';

import { useState, useEffect } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import api from '@/lib/api';

interface Currency {
  id: string;
  code: string;
  name: string;
  name_ar: string;
  symbol: string;
  is_base: boolean;
  exchange_rate: number;
}

interface CurrencySelectProps {
  value?: string;
  onChange?: (value: string) => void;
  placeholder?: string;
  showSymbol?: boolean;
  disabled?: boolean;
}

export function CurrencySelect({ value, onChange, placeholder = "اختر العملة", showSymbol = false, disabled = false }: CurrencySelectProps) {
  const [currencies, setCurrencies] = useState<Currency[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCurrencies();
  }, []);

  const fetchCurrencies = async () => {
    try {
      const res = await api.get('/currencies/active');
      setCurrencies(res.data);
    } catch (error) {
      console.error('Failed to fetch currencies');
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
        {currencies.map((currency) => (
          <SelectItem key={currency.id} value={currency.id}>
            {showSymbol ? `${currency.name_ar} (${currency.symbol})` : `${currency.name_ar} - ${currency.code}`}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

export function formatCurrency(amount: number, currencyCode: string, lang: string = 'ar'): string {
  const currencies: Record<string, { symbol: string; name: string; name_ar: string }> = {
    YER_N: { symbol: '﷼', name: 'Yemeni Rial (North)', name_ar: 'ريال يمني شمالي' },
    YER_S: { symbol: '﷼', name: 'Yemeni Rial (South)', name_ar: 'ريال يمني جنوبي' },
    SAR: { symbol: '﷼', name: 'Saudi Riyal', name_ar: 'ريال سعودي' },
    USD: { symbol: '$', name: 'US Dollar', name_ar: 'دولار أمريكي' },
  };

  const currency = currencies[currencyCode] || { symbol: '', name: currencyCode, name_ar: currencyCode };
  const formatted = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
    numberingSystem: 'latn',
  }).format(amount);

  return lang === 'ar' ? `${formatted} ${currency.symbol}` : `${currency.symbol} ${formatted}`;
}

export default CurrencySelect;
