import { Timestamps, Status } from './common';

export interface User extends Timestamps {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  department?: string;
  phone?: string;
  avatar?: string;
  isActive: boolean;
  lastLogin?: string;
  mfaEnabled: boolean;
}

export type UserRole = 'admin' | 'manager' | 'analyst' | 'collections' | 'legal' | 'viewer';

export interface Role {
  id: string;
  name: string;
  nameAr: string;
  description: string;
  permissions: Permission[];
  createdAt: string;
}

export interface Permission {
  id: string;
  module: string;
  action: 'create' | 'read' | 'update' | 'delete' | 'approve';
}

export interface CreateUserInput {
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  department?: string;
  phone?: string;
  password: string;
}

export interface UpdateUserInput {
  firstName?: string;
  lastName?: string;
  role?: UserRole;
  department?: string;
  phone?: string;
  isActive?: boolean;
}
