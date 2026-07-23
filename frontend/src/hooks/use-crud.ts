'use client';

import { useState, useCallback } from 'react';
import { apiClient, ListParams, ListResponse } from '@/lib/api-client';
import { toast } from 'sonner';

export function useCrud<T extends { id: string }>(endpoint: string) {
  const [items, setItems] = useState<T[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [sort, setSort] = useState('');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');
  const [limit] = useState(10);

  const fetchItems = useCallback(
    async (params?: ListParams) => {
      setIsLoading(true);
      setError(null);
      try {
        const queryParams: ListParams = {
          page: params?.page ?? page,
          limit: params?.limit ?? limit,
          search: params?.search ?? search,
          status: params?.status ?? status,
          sort: params?.sort ?? sort,
          order: params?.order ?? order,
        };
        const response = await apiClient.list<T>(endpoint, queryParams);
        setItems(response.items);
        setTotal(response.total);
        setPage(response.page);
        setPages(response.pages);
      } catch (err: any) {
        const message = err?.response?.data?.message || 'حدث خطأ أثناء تحميل البيانات';
        setError(message);
        toast.error(message);
      } finally {
        setIsLoading(false);
      }
    },
    [endpoint, page, limit, search, status, sort, order]
  );

  const getItem = useCallback(
    async (id: string): Promise<T | null> => {
      try {
        return await apiClient.get<T>(endpoint, id);
      } catch (err: any) {
        const message = err?.response?.data?.message || 'حدث خطأ أثناء تحميل العنصر';
        toast.error(message);
        return null;
      }
    },
    [endpoint]
  );

  const createItem = useCallback(
    async (data: any): Promise<T | null> => {
      try {
        const result = await apiClient.create<T>(endpoint, data);
        toast.success('تم الإنشاء بنجاح');
        await fetchItems({ page: 1 });
        return result;
      } catch (err: any) {
        const message = err?.response?.data?.message || 'حدث خطأ أثناء الإنشاء';
        toast.error(message);
        return null;
      }
    },
    [endpoint, fetchItems]
  );

  const updateItem = useCallback(
    async (id: string, data: any): Promise<T | null> => {
      try {
        const result = await apiClient.update<T>(endpoint, id, data);
        toast.success('تم التحديث بنجاح');
        await fetchItems();
        return result;
      } catch (err: any) {
        const message = err?.response?.data?.message || 'حدث خطأ أثناء التحديث';
        toast.error(message);
        return null;
      }
    },
    [endpoint, fetchItems]
  );

  const deleteItem = useCallback(
    async (id: string): Promise<boolean> => {
      try {
        await apiClient.delete(endpoint, id);
        toast.success('تم الحذف بنجاح');
        await fetchItems();
        return true;
      } catch (err: any) {
        const message = err?.response?.data?.message || 'حدث خطأ أثناء الحذف';
        toast.error(message);
        return false;
      }
    },
    [endpoint, fetchItems]
  );

  const refresh = useCallback(() => {
    return fetchItems();
  }, [fetchItems]);

  return {
    items,
    total,
    page,
    pages,
    isLoading,
    error,
    search,
    status,
    sort,
    order,
    fetchItems,
    getItem,
    createItem,
    updateItem,
    deleteItem,
    setPage,
    setSearch,
    setStatus,
    setSort,
    setOrder,
    refresh,
  };
}
