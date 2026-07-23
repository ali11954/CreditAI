import { Timestamps, Status, RiskLevel } from './common';

export interface Customer extends Timestamps {
  id: string;
  companyName: string;
  registrationNumber: string;
  taxId: string;
  industry: string;
  contactPerson: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  country: string;
  status: Status;
  riskLevel: RiskLevel;
  creditScore?: number;
  totalExposure: number;
  availableCredit: number;
  documentsCount: number;
  notes?: string;
}

export interface CustomerDocument {
  id: string;
  customerId: string;
  title: string;
  type: string;
  fileUrl: string;
  uploadedBy: string;
  uploadedAt: string;
  size: number;
  mimeType: string;
}

export interface CustomerContact {
  id: string;
  customerId: string;
  name: string;
  role: string;
  email: string;
  phone: string;
  isPrimary: boolean;
}

export interface CreateCustomerInput {
  companyName: string;
  registrationNumber: string;
  taxId: string;
  industry: string;
  contactPerson: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  country: string;
  notes?: string;
}

export interface UpdateCustomerInput {
  companyName?: string;
  contactPerson?: string;
  email?: string;
  phone?: string;
  address?: string;
  city?: string;
  country?: string;
  status?: Status;
  notes?: string;
}
