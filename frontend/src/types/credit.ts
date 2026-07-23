import { Timestamps, RiskLevel } from './common';

export type CreditStatus = 'draft' | 'pending' | 'under_review' | 'approved' | 'rejected' | 'expired';

export interface CreditApplication extends Timestamps {
  id: string;
  customerId: string;
  customerName: string;
  amount: number;
  currency: string;
  term: number;
  purpose: string;
  status: CreditStatus;
  riskLevel?: RiskLevel;
  creditScore?: number;
  collateralType?: string;
  collateralValue?: number;
  annualRevenue?: number;
  requestedBy: string;
  reviewedBy?: string;
  approvedBy?: string;
  approvedAt?: string;
  rejectionReason?: string;
  notes?: string;
  documentsCount: number;
}

export interface CreditLimit extends Timestamps {
  id: string;
  customerId: string;
  customerName: string;
  totalLimit: number;
  usedLimit: number;
  availableLimit: number;
  currency: string;
  riskLevel: RiskLevel;
  lastReviewDate: string;
  nextReviewDate: string;
  status: 'active' | 'suspended' | 'expired';
}

export interface Payment extends Timestamps {
  id: string;
  applicationId: string;
  customerId: string;
  customerName: string;
  amount: number;
  currency: string;
  paymentDate: string;
  paymentMethod: string;
  reference?: string;
  status: 'pending' | 'confirmed' | 'rejected';
  notes?: string;
  confirmedBy?: string;
  confirmedAt?: string;
}

export interface CreateCreditApplicationInput {
  customerId: string;
  amount: number;
  currency: string;
  term: number;
  purpose: string;
  collateralType?: string;
  collateralValue?: number;
  annualRevenue?: number;
  notes?: string;
}

export interface ApprovalDecision {
  applicationId: string;
  decision: 'approve' | 'reject';
  reason: string;
  conditions?: string[];
  creditLimit?: number;
  interestRate?: number;
  term?: number;
}
