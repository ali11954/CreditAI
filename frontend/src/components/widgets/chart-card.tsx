'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface ChartCardProps {
  title: string;
  titleEn?: string;
  type?: 'line' | 'area' | 'bar';
  className?: string;
}

export function ChartCard({
  title,
  titleEn,
  type = 'area',
  className,
}: ChartCardProps) {
  const options = {
    chart: {
      id: 'basic-chart',
      toolbar: { show: false },
      fontFamily: 'IBM Plex Sans Arabic, sans-serif',
    },
    xaxis: {
      categories: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو'],
    },
    colors: ['#3b82f6'],
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
      name: 'القيمة',
      data: [30, 40, 35, 50, 49, 60, 70],
    },
  ];

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="font-arabic">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <Chart options={options} series={series} type={type} height={300} />
      </CardContent>
    </Card>
  );
}
