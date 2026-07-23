'use client';

import { ColumnDef } from '@tanstack/react-table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { MoreHorizontal, ArrowUpDown, Eye, Edit, Trash2 } from 'lucide-react';
import Link from 'next/link';

interface CustomerRow {
  id: string;
  customer_code: string;
  name: string;
  name_ar: string;
  email: string;
  phone: string;
  business_type: string;
  risk_category: string;
  credit_score: number;
  status: string;
}

export const customerColumns: ColumnDef<CustomerRow>[] = [
  {
    id: 'select',
    header: ({ table }) => (
      <input
        type="checkbox"
        checked={table.getIsAllPageRowsSelected()}
        onChange={(e) => table.toggleAllPageRowsSelected(e.target.checked)}
        className="h-4 w-4"
      />
    ),
    cell: ({ row }) => (
      <input
        type="checkbox"
        checked={row.getIsSelected()}
        onChange={(e) => row.toggleSelected(e.target.checked)}
        className="h-4 w-4"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: 'customer_code',
    header: 'كود العميل',
  },
  {
    accessorKey: 'name',
    header: ({ column }) => (
      <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}>
        اسم الشركة <ArrowUpDown className="mr-2 h-4 w-4" />
      </Button>
    ),
    cell: ({ row }) => (
      <Link href={`/customers/${row.original.id}`} className="font-medium hover:underline font-arabic">
        {row.getValue('name')}
      </Link>
    ),
  },
  {
    accessorKey: 'name_ar',
    header: 'الاسم بالعربي',
    cell: ({ row }) => <span className="font-arabic">{row.getValue('name_ar')}</span>,
  },
  {
    accessorKey: 'business_type',
    header: 'نوع النشاط',
    cell: ({ row }) => <span className="font-arabic">{row.getValue('business_type')}</span>,
  },
  {
    accessorKey: 'risk_category',
    header: 'فئة المخاطرة',
    cell: ({ row }) => {
      const risk = row.getValue('risk_category') as string;
      const variants: Record<string, 'success' | 'warning' | 'destructive' | 'info'> = {
        low: 'success',
        medium: 'warning',
        high: 'destructive',
        critical: 'destructive',
      };
      const labels: Record<string, string> = {
        low: 'منخفض',
        medium: 'متوسط',
        high: 'مرتفع',
        critical: 'حرج',
      };
      return <Badge variant={variants[risk] || 'info'}>{labels[risk] || risk}</Badge>;
    },
  },
  {
    accessorKey: 'credit_score',
    header: 'الدرجة الائتمانية',
  },
  {
    accessorKey: 'status',
    header: 'الحالة',
    cell: ({ row }) => {
      const status = row.getValue('status') as string;
      const variants: Record<string, 'default' | 'secondary' | 'destructive' | 'success' | 'warning'> = {
        active: 'success',
        inactive: 'secondary',
        pending: 'warning',
        blocked: 'destructive',
      };
      const labels: Record<string, string> = {
        active: 'نشط',
        inactive: 'غير نشط',
        pending: 'معلق',
        blocked: 'محظور',
      };
      return <Badge variant={variants[status] || 'default'}>{labels[status] || status}</Badge>;
    },
  },
  {
    id: 'actions',
    header: 'الإجراءات',
    cell: ({ row }) => {
      const customer = row.original;
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem asChild>
              <Link href={`/customers/${customer.id}`}>
                <Eye className="mr-2 h-4 w-4" /> عرض
              </Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
];

interface UserRow {
  id: string;
  email: string;
  username: string;
  full_name: string;
  full_name_ar: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export const userColumns: ColumnDef<UserRow>[] = [
  {
    id: 'select',
    header: ({ table }) => (
      <input
        type="checkbox"
        checked={table.getIsAllPageRowsSelected()}
        onChange={(e) => table.toggleAllPageRowsSelected(e.target.checked)}
        className="h-4 w-4"
      />
    ),
    cell: ({ row }) => (
      <input
        type="checkbox"
        checked={row.getIsSelected()}
        onChange={(e) => row.toggleSelected(e.target.checked)}
        className="h-4 w-4"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: 'full_name',
    header: ({ column }) => (
      <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}>
        الاسم <ArrowUpDown className="mr-2 h-4 w-4" />
      </Button>
    ),
    cell: ({ row }) => {
      const user = row.original;
      return (
        <Link href={`/users/${user.id}`} className="font-medium hover:underline font-arabic">
          {user.full_name}
        </Link>
      );
    },
  },
  {
    accessorKey: 'full_name_ar',
    header: 'الاسم بالعربي',
    cell: ({ row }) => <span className="font-arabic">{row.getValue('full_name_ar')}</span>,
  },
  {
    accessorKey: 'email',
    header: 'البريد الإلكتروني',
  },
  {
    accessorKey: 'role',
    header: 'الدور',
    cell: ({ row }) => {
      const roles: Record<string, string> = {
        admin: 'مدير',
        manager: 'مدير قسم',
        analyst: 'محلل',
        collections: 'تحصيل',
        legal: 'قانوني',
        viewer: 'مشاهد',
      };
      return roles[row.getValue('role') as string] || row.getValue('role');
    },
  },
  {
    accessorKey: 'is_active',
    header: 'الحالة',
    cell: ({ row }) => {
      const isActive = row.getValue('is_active') as boolean;
      return (
        <Badge variant={isActive ? 'success' : 'secondary'}>
          {isActive ? 'نشط' : 'غير نشط'}
        </Badge>
      );
    },
  },
  {
    id: 'actions',
    header: 'الإجراءات',
    cell: ({ row }) => {
      const user = row.original;
      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem asChild>
              <Link href={`/users/${user.id}`}>
                <Eye className="mr-2 h-4 w-4" /> عرض
              </Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
];
