'use client';

import { useState } from 'react';
import {
  HelpCircle,
  Users,
  Shield,
  Building2,
  ShoppingCart,
  CreditCard,
  Banknote,
  Scale,
  FolderOpen,
  BarChart3,
  CheckCircle,
  AlertTriangle,
  Brain,
  GitBranch,
  Database,
  Settings,
  DollarSign,
  FileText,
  BookOpen,
  BookMarked,
  Keyboard,
  ArrowRight,
  Zap,
  Target,
  TrendingUp,
  ShieldCheck,
  Layers,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Badge } from '@/components/ui/badge';
import { useLanguage } from '@/contexts/language-context';
import { cn } from '@/lib/utils';

const t = {
  ar: {
    helpButton: 'دليل المساعدة',
    dialogTitle: 'دليل منصة CreditAI Enterprise',
    overview: 'نظرة عامة',
    modules: 'الوحدات',
    policies: 'السياسات والإجراءات',
    quickRef: 'مرجع سريع',
    systemOverview: 'نظرة عامة على النظام',
    platformName: 'CreditAI Enterprise',
    platformDesc:
      'منصة متكاملة لإدارة الائتمان والتحصيل مدعومة بالذكاء الاصطناعي. توفر المنصة أدوات شاملة لإدارة العملاء، طلبات الائتمان، التحصيل، الامتثال، والتقارير التحليلية في بيئة آمنة وموثوقة.',
    keyCapabilities: 'القدرات الأساسية',
    cap1: 'إدارة دورة حياة العميل بالكامل',
    cap2: 'أتمتة القرارات الائتمانية بالذكاء الاصطناعي',
    cap3: 'تتبع التحصيل والتدفق النقدي',
    cap4: 'الامتثال التنظيمي (AML/CFT)',
    cap5: 'تقارير تحليلية وتقارير إدارية',
    cap6: 'تكامل مع أنظمة SAP',
    modulesTitle: 'دليل الوحدات',
    policiesTitle: 'السياسات والإجراءات العالمية',
    quickRefTitle: 'المرجع السريع',
    modulesList: [
      {
        name: 'إدارة المستخدمين',
        nameEn: 'User Management',
        icon: 'Users',
        desc: 'إدارة حسابات المستخدمين والأدوار والصلاحيات',
        features: [
          'إنشاء وتعديل وحذف المستخدمين',
          'إدارة الأدوار المخصصة والصلاحيات',
          'تتبع نشاط المستخدمين وسجل التدقيق',
          'دعم المصادقة متعددة العوامل',
        ],
      },
      {
        name: 'إدارة العملاء',
        nameEn: 'Customer Management',
        icon: 'Building2',
        desc: 'إدارة شاملة لبيانات العملاء وعمليات KYC',
        features: [
          'تسجيل بيانات العميل الأساسية والقانونية',
          'إدارة مستندات KYC (التعريف بالعميل)',
          'تقييم المخاطر الأولية',
          'تتبع تاريخ التعاملات',
        ],
      },
      {
        name: 'المبيعات',
        nameEn: 'Sales',
        icon: 'ShoppingCart',
        desc: 'إدارة فواتير المبيعات والبيانات التجارية',
        features: [
          'إنشاء وإدارة فواتير المبيعات',
          'استيراد البيانات من ملفات CSV/Excel',
          'تقارير المبيعات الشهرية والسنوية',
          'إدارة الخصومات ومرتجعات المبيعات',
        ],
      },
      {
        name: 'القرارات الائتمانية',
        nameEn: 'Credit Decisions',
        icon: 'CreditCard',
        desc: 'نظام متكامل لطلب وتحليل واعتماد الائتمان',
        features: [
          'تقديم طلبات الائتمان إلكترونياً',
          'تحليل الائتمان بالذكاء الاصطناعي',
          'اعتماد الطلبات عبر لجنة الائتمان',
          'إدارة حدود الائتمان والمتابعة الدورية',
        ],
      },
      {
        name: 'التحصيل والتدفق النقدي',
        nameEn: 'Collections & Cash Flow',
        icon: 'Banknote',
        desc: 'تتبع وإدارة عمليات التحصيل والتدفق النقدي',
        features: [
          'متابعة العملاء المتأخرين (30/60/90 يوم)',
          'إدارة الوعود بالدفع والتقسيط',
          'حسابات التسوية وشطب الديون',
          'تقارير التدفق النقدي اليومية',
        ],
      },
      {
        name: 'الإجراءات القانونية',
        nameEn: 'Legal Actions',
        icon: 'Scale',
        desc: 'إدارة الإجراءات القانونية والإجراءات القضائية',
        features: [
          'فتح وإدارة القضايا القانونية',
          'تتبع مراحل القضية والمستندات',
          'إدارة المحامين والممثلين القانونيين',
          'تقارير الحالة القانونية',
        ],
      },
      {
        name: 'إدارة الوثائق',
        nameEn: 'Document Management',
        icon: 'FolderOpen',
        desc: 'نظام إدارة الوثائق والمستندات الإلكترونية',
        features: [
          'رفع وتخزين الوثائق بأمان',
          'تصنيف الوثائق حسب النوع والعميل',
          'البحث السريع في المستندات',
          'تتبع انتهاء صلاحية الوثائق',
        ],
      },
      {
        name: 'التقارير والتحليلات',
        nameEn: 'Reports & Analytics',
        icon: 'BarChart3',
        desc: 'تقارير تحليلية شاملة ولوحات معلومات تفاعلية',
        features: [
          'لوحات معلومات تفاعلية للمديرين',
          'تقارير مخصصة قابلة للتصدير',
          'تحليل الاتجاهات والأنماط',
          'تقارير الامتثال والمخاطر',
        ],
      },
      {
        name: 'الامتثال والمخاطر',
        nameEn: 'Compliance & Risk',
        icon: 'CheckCircle',
        desc: 'إدارة الامتثال التنظيمي وتقييم المخاطر',
        features: [
          'التحقق من هوية العميل (KYC)',
          'مكافحة غسل الأموال (AML/CFT)',
          'فحص القوائم السوداء وال柬埔طة (PEP)',
          'إدارة حالات الامتثال والمخالفة',
        ],
      },
      {
        name: 'مركز الذكاء الاصطناعي',
        nameEn: 'AI Center',
        icon: 'Brain',
        desc: 'نماذج الذكاء الاصطناعي لتقييم المخاطر والتنبؤ',
        features: [
          'نماذج تقييم الائتمان الذكية',
          'تنبؤات باحتمال التخلف عن السداد',
          'تحليل المخاطر المتقدم',
          'تحسين مستمر للنماذج',
        ],
      },
      {
        name: 'سير العمل',
        nameEn: 'Workflow',
        icon: 'GitBranch',
        desc: 'أتمتة سير العمل وعمليات الاعتماد',
        features: [
          'تعريف سير العمل المخصص',
          'أتمتة مراحل الاعتماد',
          'تتبع حالة الطلبات',
          'إشعارات وتذكيرات تلقائية',
        ],
      },
      {
        name: 'تكامل SAP',
        nameEn: 'SAP Integration',
        icon: 'Database',
        desc: 'تكامل سلس مع نظام ERP SAP',
        features: [
          'مزامنة بيانات العملاء',
          'استيراد فواتير المبيعات',
          'تحديثات الحسابات المدينة والدائنة',
          'تقارير التكامل وال-sync',
        ],
      },
      {
        name: 'النظام',
        nameEn: 'System',
        icon: 'Settings',
        desc: 'إعدادات النظام والإعدادات العامة',
        features: [
          'إدارة العملات وأسعار الصرف',
          'إعدادات النظام العامة',
          'إدارة الإشعارات',
          'النسخ الاحتياطي واستعادة البيانات',
        ],
      },
    ],
    policiesContent: {
      sales: 'سياسات المبيعات',
      salesItems: [
        {
          title: 'شروط الائتمان',
          content:
            'يتم تحديد شروط الائتمان بناءً على تقييم المخاطر للمعميل. تشمل المدة الزمنية (30/60/90 يوم) والحد الأقصى لمبلغ الائتمان ونسبة الفائدة المطبقة.',
        },
        {
          title: 'أسعار التسعير',
          content:
            'تُحدد الأسعار حسب فئات العملاء وحجم التعاملات. توجد خصومات خاصة للعملاء الاستراتيجيين وفقاً لموافقة الإدارة.',
        },
        {
          title: 'سير عمل الاعتماد',
          content:
            'كل فاتورة تمر بمراحل: إنشاء → مراجعة → اعتماد → إصدار. المبالغ فوق الحد المحدد تتطلب اعتماد لجنة الائتمان.',
        },
        {
          title: 'إدارة الفواتير',
          content:
            'تتبع الفواتير من الإصدار حتى السداد الكامل. إمكانية استيراد الفواتير من ملفات CSV وتصدير التقارير.',
        },
        {
          title: 'سياسة المرتجعات والخصومات',
          content:
            'تُقبل المرتجعات بموافقة إدارة المبيعات. الخصومات تتطلب توثيقاً مسبقاً واعتماد المدير المالي للمبالغ الكبيرة.',
        },
      ],
      collections: 'إجراءات التحصيل',
      collectionsItems: [
        {
          title: 'مراحل التحصيل',
          content:
            'المرحلة الأولى (1-30 يوم): تذكير ودي. المرحلة الثانية (31-60 يوم): إنذار رسمي. المرحلة الثالثة (61-90 يوم): إنذار نهائي وتسليم للقانوني.',
        },
        {
          title: 'إجراءات التصعيد',
          content:
            'تصعيد تلقائي حسب المدة: فريق التحصيل → المدير → الإدارة التنفيذية → الإدارة القانونية.',
        },
        {
          title: 'الوعود بالدفع',
          content:
            'تسجيل الوعود بالدفع مع التاريخ والمبلغ. متابعة تلقائية عند موعد الوفاء. تحديث حالة الوعود في النظام.',
        },
        {
          title: 'موافقة التسوية',
          content:
            'التسويات أقل من 10% تتطلب موافقة المدير. تسويات 10-25% تتطلب موافقة المدير المالي. تسويات أكثر من 25% تتطلب موافقة مجلس الإدارة.',
        },
        {
          title: 'سياسة الشطب',
          content:
            'يُشطب الدين بعد استنفاف جميع إجراءات التحصيل والقانوني. يتطلب توثيقاً كاملاً واعتماداً إدارياً متعدد المراحل.',
        },
      ],
      credit: 'سياسات الائتمان',
      creditItems: [
        {
          title: 'معايير تقييم الائتمان',
          content:
            'التحليل المالي: النسب المالية الرئيسية (السيولة، الرفع المالي، الربحية). التحليل غير المالي: سمعة العميل، تاريخ التعامل، القطاع.',
        },
        {
          title: 'نموذج التقييم',
          content:
            'يستخدم النظام نموذج ذكاء اصطناعي مدمج يأخذ في الاعتبار أكثر من 50 متغيراً. يُحدّث النموذج دورياً بناءً على بيانات الأداء.',
        },
        {
          title: 'مصفوفة سلطة الاعتماد',
          content:
            'المدير: حتى 500,000$. المدير المالي: حتى 2,000,000$. لجنة الائتمان: حتى 10,000,000$. مجلس الإدارة: أكثر من 10,000,000$.',
        },
        {
          title: 'حدود التعرض',
          content:
            'الحد الأقصى لكل عميل: 15% من رأس المال. الحد الأقصى لكل قطاع: 30% من إجمالي المحفظة. مراجعة الحدود كل 6 أشهر.',
        },
        {
          title: 'متطلبات الضمانات',
          content:
            'ضمانات مالية: كفالة بنكية، خطاب ضمان. ضمانات عقارية: تقييم مستقل، تأمين. ضمانات شخصية: كفالة شخصية.',
        },
        {
          title: 'دورية المراجعة',
          content:
            'مراجعة شاملة كل 6 أشهر للعملاء الحاليين. مراجعة فورية عند تغير الظروف المالية. تحديث التقييم والحدود سنوياً.',
        },
      ],
      risk: 'سياسات المخاطر',
      riskItems: [
        {
          title: 'فئات المخاطر',
          content:
            'منخفضة: عملاء بسجل مالي ممتاز وضمانات كافية. متوسطة: عملاء مستقرون مع بعض المخاطر. عالية: عملاء بسجل مالي ضعيف أو قطاع متأثر. حرجة: عملاء متأخرون أو في إفلاس.',
        },
        {
          title: 'حدود التركيز',
          content:
            'الحد الأقصى لعميل واحد: 15% من رأس المال. الحد الأقصى لقطاع واحد: 30%. الحد الأقصى لمنطقة جغرافية واحدة: 25%.',
        },
        {
          title: 'اختبار الضغط',
          content:
            'اختبار سنوي لسيناريوهات مختلفة: انخفاض الإيرادات 20%، ارتفاع أسعار الفائدة 5%، تراجع سوقي 30%. تحليل الأثر على المحفظة الإئتمانية.',
        },
        {
          title: 'امتثال AML/CFT',
          content:
            'التوافق مع معايير بازل III. فحص القوائم السوداء دورياً. تقارير المعاملات المشبوهة. تعليمات الموظفين السنوية.',
        },
        {
          title: 'الخسائر الائتمانية المتوقعة (IFRS 9)',
          content:
            'حساب Provision بناءً على المرحلة الأولى (12 شهر) والمرحلة الثانية (العمر الإئتماني). نماذج احتمالية للتوقعات.',
        },
        {
          title: 'منهجية Provision',
          content:
            '1-30 يوم: 1%. 31-60 يوم: 5%. 61-90 يوم: 20%. 91-180 يوم: 50%. أكثر من 180 يوم: 100%.',
        },
      ],
    },
    shortcuts: {
      title: 'اختصارات لوحة المفاتيح',
      items: [
        { keys: 'Ctrl + K', action: 'فتح البحث السريع' },
        { keys: 'Ctrl + N', action: 'إنشاء سجل جديد' },
        { keys: 'Ctrl + S', action: 'حفظ التغييرات' },
        { keys: 'Ctrl + E', action: 'تصدير البيانات' },
        { keys: 'Esc', action: 'إغلاق النافذة المنبثقة' },
        { keys: '?', action: 'فتح دليل المساعدة' },
      ],
    },
    navTips: {
      title: 'نصائح التنقل',
      items: [
        'استخدم الشريط الجانبي للتنقل بين الوحدات',
        'البحث السريع في أعلى الصفحة للعثور على سجل معين',
        'النقر على "?" في أي وقت لفتح هذا الدليل',
        'استخدم الفلاتر لتحديد البيانات المعروضة',
        'تصدير التقارير بصيغ PDF أو Excel',
      ],
    },
  },
  en: {
    helpButton: 'Help Guide',
    dialogTitle: 'CreditAI Enterprise Guide',
    overview: 'Overview',
    modules: 'Modules',
    policies: 'Policies & Procedures',
    quickRef: 'Quick Reference',
    systemOverview: 'System Overview',
    platformName: 'CreditAI Enterprise',
    platformDesc:
      'A comprehensive credit management and collections platform powered by AI. The platform provides tools for customer management, credit applications, collections, compliance, and analytics reports in a secure and reliable environment.',
    keyCapabilities: 'Key Capabilities',
    cap1: 'Full customer lifecycle management',
    cap2: 'AI-powered credit decision automation',
    cap3: 'Collections and cash flow tracking',
    cap4: 'Regulatory compliance (AML/CFT)',
    cap5: 'Analytics and management reports',
    cap6: 'SAP system integration',
    modulesTitle: 'Module Guide',
    policiesTitle: 'Global Policies & Procedures',
    quickRefTitle: 'Quick Reference',
    modulesList: [
      {
        name: 'Users Management',
        nameEn: 'User Management',
        icon: 'Users',
        desc: 'Manage user accounts, roles, and permissions',
        features: [
          'Create, edit, and delete users',
          'Manage custom roles and permissions',
          'Track user activity and audit log',
          'Multi-factor authentication support',
        ],
      },
      {
        name: 'Customer Management',
        nameEn: 'Customer Management',
        icon: 'Building2',
        desc: 'Comprehensive customer data and KYC management',
        features: [
          'Register basic and legal customer data',
          'Manage KYC documents',
          'Initial risk assessment',
          'Transaction history tracking',
        ],
      },
      {
        name: 'Sales',
        nameEn: 'Sales',
        icon: 'ShoppingCart',
        desc: 'Sales invoice and commercial data management',
        features: [
          'Create and manage sales invoices',
          'Import data from CSV/Excel files',
          'Monthly and annual sales reports',
          'Manage discounts and returns',
        ],
      },
      {
        name: 'Credit Decisions',
        nameEn: 'Credit Decisions',
        icon: 'CreditCard',
        desc: 'Complete system for credit request, analysis, and approval',
        features: [
          'Submit credit requests electronically',
          'AI-powered credit analysis',
          'Committee approval workflow',
          'Credit limits and periodic review',
        ],
      },
      {
        name: 'Collections & Cash Flow',
        nameEn: 'Collections & Cash Flow',
        icon: 'Banknote',
        desc: 'Track and manage collection and cash flow processes',
        features: [
          'Follow up with overdue customers (30/60/90 days)',
          'Manage payment promises and installments',
          'Settlement and write-off calculations',
          'Daily cash flow reports',
        ],
      },
      {
        name: 'Legal Actions',
        nameEn: 'Legal Actions',
        icon: 'Scale',
        desc: 'Manage legal and judicial procedures',
        features: [
          'Open and manage legal cases',
          'Track case stages and documents',
          'Manage lawyers and legal representatives',
          'Legal status reports',
        ],
      },
      {
        name: 'Document Management',
        nameEn: 'Document Management',
        icon: 'FolderOpen',
        desc: 'Electronic document and file management system',
        features: [
          'Secure document upload and storage',
          'Document classification by type and customer',
          'Quick document search',
          'Document expiry tracking',
        ],
      },
      {
        name: 'Reports & Analytics',
        nameEn: 'Reports & Analytics',
        icon: 'BarChart3',
        desc: 'Comprehensive analytics reports and interactive dashboards',
        features: [
          'Interactive management dashboards',
          'Customizable exportable reports',
          'Trend and pattern analysis',
          'Compliance and risk reports',
        ],
      },
      {
        name: 'Compliance & Risk',
        nameEn: 'Compliance & Risk',
        icon: 'CheckCircle',
        desc: 'Regulatory compliance and risk assessment management',
        features: [
          'Know Your Customer (KYC)',
          'Anti-Money Laundering (AML/CFT)',
          'Blacklist and PEP screening',
          'Compliance case management',
        ],
      },
      {
        name: 'AI Center',
        nameEn: 'AI Center',
        icon: 'Brain',
        desc: 'AI models for risk assessment and prediction',
        features: [
          'Smart credit scoring models',
          'Default probability predictions',
          'Advanced risk analysis',
          'Continuous model improvement',
        ],
      },
      {
        name: 'Workflow',
        nameEn: 'Workflow',
        icon: 'GitBranch',
        desc: 'Workflow and approval process automation',
        features: [
          'Define custom workflows',
          'Approval stage automation',
          'Request status tracking',
          'Automatic notifications and reminders',
        ],
      },
      {
        name: 'SAP Integration',
        nameEn: 'SAP Integration',
        icon: 'Database',
        desc: 'Seamless integration with SAP ERP system',
        features: [
          'Customer data synchronization',
          'Sales invoice import',
          'Debit/credit account updates',
          'Integration and sync reports',
        ],
      },
      {
        name: 'System',
        nameEn: 'System',
        icon: 'Settings',
        desc: 'System settings and general configurations',
        features: [
          'Currency and exchange rate management',
          'General system settings',
          'Notification management',
          'Data backup and recovery',
        ],
      },
    ],
    policiesContent: {
      sales: 'Sales Policies',
      salesItems: [
        {
          title: 'Credit Terms',
          content:
            'Credit terms are determined based on customer risk assessment. Includes time period (30/60/90 days), maximum credit amount, and applicable interest rates.',
        },
        {
          title: 'Pricing',
          content:
            'Prices are set according to customer categories and transaction volumes. Special discounts are available for strategic customers with management approval.',
        },
        {
          title: 'Approval Workflow',
          content:
            'Each invoice passes through stages: Creation → Review → Approval → Issuance. Amounts above the set threshold require credit committee approval.',
        },
        {
          title: 'Invoice Management',
          content:
            'Track invoices from issuance to full payment. Ability to import invoices from CSV files and export reports.',
        },
        {
          title: 'Returns & Discounts Policy',
          content:
            'Returns are accepted with sales management approval. Discounts require prior documentation and CFO approval for large amounts.',
        },
      ],
      collections: 'Collection Procedures',
      collectionsItems: [
        {
          title: 'Collection Stages',
          content:
            'Stage 1 (1-30 days): Friendly reminder. Stage 2 (31-60 days): Formal warning. Stage 3 (61-90 days): Final warning and legal handover.',
        },
        {
          title: 'Escalation Procedures',
          content:
            'Automatic escalation by duration: Collection team → Manager → Executive management → Legal department.',
        },
        {
          title: 'Promises to Pay',
          content:
            'Record payment promises with date and amount. Automatic follow-up on due date. Update promise status in the system.',
        },
        {
          title: 'Settlement Approval',
          content:
            'Settlements under 10% require manager approval. Settlements 10-25% require CFO approval. Settlements over 25% require board approval.',
        },
        {
          title: 'Write-off Policy',
          content:
            'Debt is written off after exhausting all collection and legal measures. Requires complete documentation and multi-level administrative approval.',
        },
      ],
      credit: 'Credit Policies',
      creditItems: [
        {
          title: 'Assessment Criteria',
          content:
            'Financial analysis: Key financial ratios (liquidity, leverage, profitability). Non-financial analysis: Customer reputation, transaction history, sector.',
        },
        {
          title: 'Scoring Model',
          content:
            'The system uses an integrated AI model considering over 50 variables. The model is updated periodically based on performance data.',
        },
        {
          title: 'Approval Authority Matrix',
          content:
            'Manager: Up to $500K. CFO: Up to $2M. Credit Committee: Up to $10M. Board: Over $10M.',
        },
        {
          title: 'Exposure Limits',
          content:
            'Maximum per customer: 15% of capital. Maximum per sector: 30% of total portfolio. Limits reviewed every 6 months.',
        },
        {
          title: 'Collateral Requirements',
          content:
            'Financial guarantees: Bank guarantees, letters of credit. Real estate guarantees: Independent appraisal, insurance. Personal guarantees: Personal surety.',
        },
        {
          title: 'Review Frequency',
          content:
            'Comprehensive review every 6 months for existing customers. Immediate review upon change in financial circumstances. Annual limit updates.',
        },
      ],
      risk: 'Risk Policies',
      riskItems: [
        {
          title: 'Risk Categories',
          content:
            'Low: Customers with excellent financial record and adequate guarantees. Medium: Stable customers with some risks. High: Customers with weak financial record or affected sector. Critical: Defaulting or bankrupt customers.',
        },
        {
          title: 'Concentration Limits',
          content:
            'Maximum per customer: 15% of capital. Maximum per sector: 30%. Maximum per geographic region: 25%.',
        },
        {
          title: 'Stress Testing',
          content:
            'Annual testing of various scenarios: 20% revenue decline, 5% interest rate increase, 30% market downturn. Impact analysis on credit portfolio.',
        },
        {
          title: 'AML/CFT Compliance',
          content:
            'Basel III standards compliance. Periodic blacklist screening. Suspicious transaction reports. Annual employee training.',
        },
        {
          title: 'IFRS 9 Expected Credit Loss',
          content:
            'Provision calculation based on Stage 1 (12 months) and Stage 2 (lifetime). Probabilistic models for forecasts.',
        },
        {
          title: 'Provision Methodology',
          content:
            '1-30 days: 1%. 31-60 days: 5%. 61-90 days: 20%. 91-180 days: 50%. Over 180 days: 100%.',
        },
      ],
    },
    shortcuts: {
      title: 'Keyboard Shortcuts',
      items: [
        { keys: 'Ctrl + K', action: 'Open quick search' },
        { keys: 'Ctrl + N', action: 'Create new record' },
        { keys: 'Ctrl + S', action: 'Save changes' },
        { keys: 'Ctrl + E', action: 'Export data' },
        { keys: 'Esc', action: 'Close modal' },
        { keys: '?', action: 'Open help guide' },
      ],
    },
    navTips: {
      title: 'Navigation Tips',
      items: [
        'Use the sidebar to navigate between modules',
        'Quick search at the top of the page to find specific records',
        'Click "?" at any time to open this guide',
        'Use filters to narrow down displayed data',
        'Export reports in PDF or Excel format',
      ],
    },
  },
};

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  Users,
  Shield,
  Building2,
  ShoppingCart,
  CreditCard,
  Banknote,
  Scale,
  FolderOpen,
  BarChart3,
  CheckCircle,
  AlertTriangle,
  Brain,
  GitBranch,
  Database,
  Settings,
  DollarSign,
  FileText,
};

export function HelpGuide() {
  const { locale, isRtl } = useLanguage();
  const [open, setOpen] = useState(false);
  const content = t[locale];

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon" className="relative" aria-label={content.helpButton}>
          <HelpCircle className="h-5 w-5" />
        </Button>
      </DialogTrigger>
      <DialogContent
        className={cn(
          'flex h-[90vh] max-h-[90vh] w-full flex-col p-0 sm:max-w-2xl md:max-w-3xl lg:max-w-4xl',
          isRtl && 'font-arabic'
        )}
      >
        <DialogHeader className="flex flex-row items-center justify-between border-b px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <BookOpen className="h-5 w-5 text-primary" />
            </div>
            <div>
              <DialogTitle className="text-lg">{content.dialogTitle}</DialogTitle>
              <p className="text-xs text-muted-foreground">{content.platformName}</p>
            </div>
          </div>
        </DialogHeader>

        <Tabs defaultValue="overview" className="flex flex-1 flex-col overflow-hidden">
          <div className="border-b px-6">
            <TabsList className="h-auto w-full justify-start gap-1 bg-transparent p-0">
              <TabsTrigger
                value="overview"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <BookOpen className="mr-2 h-4 w-4" />
                {content.overview}
              </TabsTrigger>
              <TabsTrigger
                value="modules"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <Layers className="mr-2 h-4 w-4" />
                {content.modules}
              </TabsTrigger>
              <TabsTrigger
                value="policies"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <BookMarked className="mr-2 h-4 w-4" />
                {content.policies}
              </TabsTrigger>
              <TabsTrigger
                value="quickref"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <Keyboard className="mr-2 h-4 w-4" />
                {content.quickRef}
              </TabsTrigger>
            </TabsList>
          </div>

          <ScrollArea className="flex-1">
            {/* OVERVIEW TAB */}
            <TabsContent value="overview" className="mt-0 p-6">
              <div className="space-y-6">
                <div className="rounded-lg border bg-card p-6">
                  <div className="mb-4 flex items-center gap-3">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                      <Zap className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">{content.platformName}</h3>
                      <p className="text-sm text-muted-foreground">{content.systemOverview}</p>
                    </div>
                  </div>
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {content.platformDesc}
                  </p>
                </div>

                <div>
                  <h4 className="mb-3 text-sm font-semibold">{content.keyCapabilities}</h4>
                  <div className="grid gap-2 sm:grid-cols-2">
                    {[content.cap1, content.cap2, content.cap3, content.cap4, content.cap5, content.cap6].map(
                      (cap, i) => (
                        <div
                          key={i}
                          className="flex items-start gap-2 rounded-md border p-3 text-sm"
                        >
                          <CheckCircle className="mt-0.5 h-4 w-4 shrink-0 text-green-500" />
                          <span>{cap}</span>
                        </div>
                      )
                    )}
                  </div>
                </div>
              </div>
            </TabsContent>

            {/* MODULES TAB */}
            <TabsContent value="modules" className="mt-0 p-6">
              <Accordion type="multiple" className="space-y-2">
                {content.modulesList.map((mod, i) => {
                  const Icon = iconMap[mod.icon] || FileText;
                  return (
                    <AccordionItem key={i} value={`module-${i}`} className="rounded-lg border px-4">
                      <AccordionTrigger className="py-3 text-sm font-medium hover:no-underline">
                        <div className="flex items-center gap-3">
                          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary/10">
                            <Icon className="h-4 w-4 text-primary" />
                          </div>
                          <div className="text-start">
                            <span className="font-semibold">{mod.name}</span>
                            <p className="text-xs text-muted-foreground">{mod.desc}</p>
                          </div>
                        </div>
                      </AccordionTrigger>
                      <AccordionContent>
                        <ul className="space-y-2 pb-2 ps-11">
                          {mod.features.map((f, j) => (
                            <li key={j} className="flex items-start gap-2 text-sm text-muted-foreground">
                              <ArrowRight className="mt-1 h-3 w-3 shrink-0 text-primary" />
                              <span>{f}</span>
                            </li>
                          ))}
                        </ul>
                      </AccordionContent>
                    </AccordionItem>
                  );
                })}
              </Accordion>
            </TabsContent>

            {/* POLICIES TAB */}
            <TabsContent value="policies" className="mt-0 p-6">
              <div className="space-y-6">
                {/* Sales Policies */}
                <div>
                  <div className="mb-3 flex items-center gap-2">
                    <ShoppingCart className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{content.policiesContent.sales}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {content.policiesContent.salesItems.map((item, i) => (
                      <AccordionItem key={i} value={`sales-${i}`} className="rounded-md border px-4">
                        <AccordionTrigger className="py-2.5 text-sm font-medium hover:no-underline">
                          {item.title}
                        </AccordionTrigger>
                        <AccordionContent>
                          <p className="pb-2 text-sm leading-relaxed text-muted-foreground">
                            {item.content}
                          </p>
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </div>

                <div className="h-px bg-border" />

                {/* Collections Procedures */}
                <div>
                  <div className="mb-3 flex items-center gap-2">
                    <Banknote className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{content.policiesContent.collections}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {content.policiesContent.collectionsItems.map((item, i) => (
                      <AccordionItem key={i} value={`collections-${i}`} className="rounded-md border px-4">
                        <AccordionTrigger className="py-2.5 text-sm font-medium hover:no-underline">
                          {item.title}
                        </AccordionTrigger>
                        <AccordionContent>
                          <p className="pb-2 text-sm leading-relaxed text-muted-foreground">
                            {item.content}
                          </p>
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </div>

                <div className="h-px bg-border" />

                {/* Credit Policies */}
                <div>
                  <div className="mb-3 flex items-center gap-2">
                    <CreditCard className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{content.policiesContent.credit}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {content.policiesContent.creditItems.map((item, i) => (
                      <AccordionItem key={i} value={`credit-${i}`} className="rounded-md border px-4">
                        <AccordionTrigger className="py-2.5 text-sm font-medium hover:no-underline">
                          {item.title}
                        </AccordionTrigger>
                        <AccordionContent>
                          <p className="pb-2 text-sm leading-relaxed text-muted-foreground">
                            {item.content}
                          </p>
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </div>

                <div className="h-px bg-border" />

                {/* Risk Policies */}
                <div>
                  <div className="mb-3 flex items-center gap-2">
                    <ShieldCheck className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{content.policiesContent.risk}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {content.policiesContent.riskItems.map((item, i) => (
                      <AccordionItem key={i} value={`risk-${i}`} className="rounded-md border px-4">
                        <AccordionTrigger className="py-2.5 text-sm font-medium hover:no-underline">
                          {item.title}
                        </AccordionTrigger>
                        <AccordionContent>
                          <p className="pb-2 text-sm leading-relaxed text-muted-foreground">
                            {item.content}
                          </p>
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </div>
              </div>
            </TabsContent>

            {/* QUICK REFERENCE TAB */}
            <TabsContent value="quickref" className="mt-0 p-6">
              <div className="space-y-6">
                {/* Keyboard Shortcuts */}
                <div className="rounded-lg border bg-card p-5">
                  <div className="mb-4 flex items-center gap-2">
                    <Keyboard className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{content.shortcuts.title}</h4>
                  </div>
                  <div className="space-y-2">
                    {content.shortcuts.items.map((item, i) => (
                      <div key={i} className="flex items-center justify-between rounded-md border p-3">
                        <span className="text-sm text-muted-foreground">{item.action}</span>
                        <Badge variant="secondary" className="font-mono text-xs">
                          {item.keys}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Navigation Tips */}
                <div className="rounded-lg border bg-card p-5">
                  <div className="mb-4 flex items-center gap-2">
                    <Target className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{content.navTips.title}</h4>
                  </div>
                  <ul className="space-y-2">
                    {content.navTips.items.map((tip, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                        <TrendingUp className="mt-1 h-3.5 w-3.5 shrink-0 text-primary" />
                        <span>{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </TabsContent>
          </ScrollArea>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
