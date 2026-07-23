'use client';

import { useState, useCallback } from 'react';
import api, { ApiResponse, PaginatedResponse } from '@/lib/api';

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function useApi<T>() {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(async (fn: () => Promise<ApiResponse<T>>) => {
    setState({ data: null, loading: true, error: null });
    try {
      const response = await fn();
      setState({ data: response.data, loading: false, error: null });
      return response.data;
    } catch (err: any) {
      const message = err.response?.data?.message || err.message || 'حدث خطأ';
      setState({ data: null, loading: false, error: message });
      throw err;
    }
  }, []);

  const get = useCallback(
    (url: string, params?: Record<string, any>) =>
      execute(() => api.get<ApiResponse<T>>(url, { params }).then((r) => r.data)),
    [execute]
  );

  const post = useCallback(
    (url: string, data?: any) =>
      execute(() => api.post<ApiResponse<T>>(url, data).then((r) => r.data)),
    [execute]
  );

  const put = useCallback(
    (url: string, data?: any) =>
      execute(() => api.put<ApiResponse<T>>(url, data).then((r) => r.data)),
    [execute]
  );

  const del = useCallback(
    (url: string) =>
      execute(() => api.delete<ApiResponse<T>>(url).then((r) => r.data)),
    [execute]
  );

  return { ...state, execute, get, post, put, del };
}

export function usePaginatedApi<T>() {
  const [state, setState] = useState<{
    data: T[];
    total: number;
    loading: boolean;
    error: string | null;
  }>({
    data: [],
    total: 0,
    loading: false,
    error: null,
  });

  const fetch = useCallback(async (url: string, params?: Record<string, any>) => {
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      const response = await api.get<ApiResponse<PaginatedResponse<T>>>(url, { params });
      const { data, total } = response.data.data;
      setState({ data, total, loading: false, error: null });
      return response.data.data;
    } catch (err: any) {
      const message = err.response?.data?.message || err.message || 'حدث خطأ';
      setState((s) => ({ ...s, loading: false, error: message }));
      throw err;
    }
  }, []);

  return { ...state, fetch };
}
