'use client';

import api from './api';

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  full_name_ar?: string;
  phone?: string;
  avatar?: string;
  is_active: boolean;
  is_superuser: boolean;
  mfa_enabled?: boolean;
  last_login?: string;
  created_at?: string;
}

export interface AuthResponse {
  user?: User;
  access_token: string;
  refresh_token: string;
  token_type?: string;
  expires_in?: number;
  mfaRequired?: boolean;
  pendingToken?: string;
}

export const authService = {
  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', { email, password, username: null });
    return response.data;
  },

  async verifyMfa(token: string, code: string): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/verify-mfa', { token, code });
    return response.data;
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout');
    if (typeof window !== 'undefined') {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  },

  async getProfile(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await api.put<User>('/auth/profile', data);
    return response.data;
  },

  getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('accessToken');
  },

  setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
  },

  clearTokens(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },

  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('accessToken');
  },
};
