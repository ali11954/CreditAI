'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import dynamic from 'next/dynamic';
import api from '@/lib/api';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface ChartCardProps {
  title: string;
  titleEn?: string;
  type?: 'line' | 'area' | 'bar';
  className?: string;
  endpoint?: string;
}

export function ChartCard({
  title,
  titleEn,
  type = 'area',
  className,
  endpoint,
}: ChartCardProps) {
  const [chartData, setChartData] = useState<{ categories: string[]; values: number[] }>({
    categories: [],
    values: [],
  });

  useEffect(() => {
    if (!endpoint) return;
    const fetchData = async () => {
      try {
        const res = await api.get(endpoint);
        setChartData({
          categories: res.data.categories || [],
          values: res.data.values || [],
        });
      } catch {
        setChartData({ categories: [], values: [] });
      }
    };
    fetchData();
  }, [endpoint]);

  const options = {
    chart: {
      id: 'basic-chart',
      toolbar: { show: false },
      fontFamily: 'IBM Plex Sans Arabic, sans-serif',
    },
    xaxis: {
      categories: chartData.categories.length > 0 ? chartData.categories : ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو'],
    },
    colors: [type === 'bar' ? '#3b82f6' : '#22c55e'],
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.4,
        opacityTo: 0.1,
      },
    },
  };

  const series = [
    {
      name: title,
      data: chartData.values.length > 0 ? chartData.values : [],
    },
  ];

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="font-arabic">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {chartData.values.length === 0 && !endpoint ? (
          <div className="flex items-center justify-center h-[300px] text-muted-foreground font-arabic">
            لا توجد بيانات
          </div>
        ) : (
          <Chart options={options} series={series} type={type} height={300} />
        )}
      </CardContent>
    </Card>
  );
}
