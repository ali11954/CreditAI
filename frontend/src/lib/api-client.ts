'use client';

import api from '@/lib/api';

export interface ListParams {
  page?: number;
  limit?: number;
  search?: string;
  status?: string;
  sort?: string;
  order?: 'asc' | 'desc';
}

export interface ListResponse<T> {
  items: T[];
  total: number;
  page: number;
  pages: number;
}

export interface UploadResponse {
  filename: string;
  filepath: string;
  size: number;
}

export interface UploadMultipleResponse {
  uploaded: UploadResponse[];
  errors: { filename: string; error: string }[];
}

function toQueryString(params?: Record<string, any>): string {
  if (!params) return '';
  const entries = Object.entries(params).filter(
    ([, v]) => v !== undefined && v !== null && v !== ''
  );
  if (entries.length === 0) return '';
  return '?' + new URLSearchParams(entries.map(([k, v]) => [k, String(v)])).toString();
}

export const apiClient = {
  async list<T>(endpoint: string, params?: ListParams): Promise<ListResponse<T>> {
    const qs = toQueryString(params as Record<string, any>);
    const response = await api.get<ListResponse<T>>(`${endpoint}${qs}`);
    return response.data;
  },

  async get<T>(endpoint: string, id: string): Promise<T> {
    const response = await api.get<T>(`${endpoint}/${id}`);
    return response.data;
  },

  async create<T>(endpoint: string, data: any): Promise<T> {
    const response = await api.post<T>(endpoint, data);
    return response.data;
  },

  async update<T>(endpoint: string, id: string, data: any): Promise<T> {
    const response = await api.put<T>(`${endpoint}/${id}`, data);
    return response.data;
  },

  async delete(endpoint: string, id: string): Promise<void> {
    await api.delete(`${endpoint}/${id}`);
  },

  async exportExcel(
    endpoint: string,
    data: any[],
    columns?: { key: string; label: string }[],
    filename?: string
  ): Promise<Blob> {
    const response = await api.post(
      `${endpoint}/export/excel`,
      { data, columns, filename },
      { responseType: 'blob' }
    );
    return response.data as Blob;
  },

  async exportPdf(
    endpoint: string,
    data: any[],
    columns?: { key: string; label: string }[],
    filename?: string,
    title?: string
  ): Promise<Blob> {
    const response = await api.post(
      `${endpoint}/export/pdf`,
      { data, columns, filename, title },
      { responseType: 'blob' }
    );
    return response.data as Blob;
  },

  async exportCsv(
    endpoint: string,
    data: any[],
    columns?: { key: string; label: string }[],
    filename?: string
  ): Promise<Blob> {
    const response = await api.post(
      `${endpoint}/export/csv`,
      { data, columns, filename },
      { responseType: 'blob' }
    );
    return response.data as Blob;
  },

  async upload(file: File, folder?: string): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (folder) formData.append('folder', folder);
    const response = await api.post<UploadResponse>('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  async uploadMultiple(files: File[], folder?: string): Promise<UploadMultipleResponse> {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    if (folder) formData.append('folder', folder);
    const response = await api.post<UploadMultipleResponse>('/upload/multiple', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
};

export function downloadBlob(blob: Blob, filename: string) {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
}
