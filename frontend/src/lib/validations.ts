import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('البريد الإلكتروني غير صحيح'),
  password: z.string().min(6, 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'),
  rememberMe: z.boolean().default(false),
});

export const userSchema = z.object({
  firstName: z.string().min(2, 'الاسم الأول مطلوب'),
  lastName: z.string().min(2, 'اسم العائلة مطلوب'),
  email: z.string().email('البريد الإلكتروني غير صحيح'),
  role: z.string().min(1, 'الدور مطلوب'),
  department: z.string().optional(),
  phone: z.string().optional(),
  isActive: z.boolean().default(true),
});

export const customerSchema = z.object({
  companyName: z.string().min(2, 'اسم الشركة مطلوب'),
  registrationNumber: z.string().min(1, 'رقم السجل التجاري مطلوب'),
  taxId: z.string().min(1, 'الرقم الضريبي مطلوب'),
  industry: z.string().min(1, 'القطاع مطلوب'),
  contactPerson: z.string().min(2, 'اسم جهة الاتصال مطلوب'),
  email: z.string().email('البريد الإلكتروني غير صحيح'),
  phone: z.string().min(10, 'رقم الهاتف غير صحيح'),
  address: z.string().min(5, 'العنوان مطلوب'),
  city: z.string().min(2, 'المدينة مطلوبة'),
  country: z.string().min(2, 'الدولة مطلوبة'),
});

export const creditApplicationSchema = z.object({
  customerId: z.string().min(1, 'العميل مطلوب'),
  amount: z.number().min(1, 'المبلغ مطلوب'),
  currency: z.string().default('ILS'),
  term: z.number().min(1, 'المدة مطلوبة'),
  purpose: z.string().min(2, 'الغرض مطلوب'),
  collateralType: z.string().optional(),
  collateralValue: z.number().optional(),
  annualRevenue: z.number().optional(),
  notes: z.string().optional(),
});

export const paymentSchema = z.object({
  applicationId: z.string().min(1),
  amount: z.number().min(1, 'المبلغ مطلوب'),
  paymentDate: z.string().min(1, 'تاريخ الدفع مطلوب'),
  paymentMethod: z.string().min(1, 'طريقة الدفع مطلوبة'),
  reference: z.string().optional(),
  notes: z.string().optional(),
});

export const documentSchema = z.object({
  title: z.string().min(1, 'عنوان الوثيقة مطلوب'),
  type: z.string().min(1, 'نوع الوثيقة مطلوب'),
  customerId: z.string().optional(),
  applicationId: z.string().optional(),
  description: z.string().optional(),
});

export type LoginInput = z.infer<typeof loginSchema>;
export type UserInput = z.infer<typeof userSchema>;
export type CustomerInput = z.infer<typeof customerSchema>;
export type CreditApplicationInput = z.infer<typeof creditApplicationSchema>;
export type PaymentInput = z.infer<typeof paymentSchema>;
export type DocumentInput = z.infer<typeof documentSchema>;
