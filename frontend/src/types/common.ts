export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ApiResponse<T = any> {
  data: T;
  message?: string;
  success: boolean;
}

export interface SelectOption {
  label: string;
  value: string;
}

export interface ColumnDef<T> {
  id: string;
  header: string;
  headerAr: string;
  accessorKey: keyof T;
  cell?: (row: T) => React.ReactNode;
  sortable?: boolean;
  filterable?: boolean;
  visible?: boolean;
}

export type SortDirection = 'asc' | 'desc';

export interface SortState {
  column: string;
  direction: SortDirection;
}

export interface FilterState {
  column: string;
  value: string;
  operator: 'equals' | 'contains' | 'gt' | 'lt' | 'gte' | 'lte';
}

export interface PaginationState {
  page: number;
  pageSize: number;
  total: number;
}

export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export type Status = 'active' | 'inactive' | 'pending' | 'blocked';

export interface Timestamps {
  createdAt: string;
  updatedAt: string;
}

export interface AuditLog {
  id: string;
  userId: string;
  userName: string;
  action: string;
  entity: string;
  entityId: string;
  changes: Record<string, { old: any; new: any }>;
  timestamp: string;
  ipAddress: string;
}
