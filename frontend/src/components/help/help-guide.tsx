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
  FileSignature,
  ClipboardList,
  Truck,
  Receipt,
  Gavel,
  Search,
  MessageSquare,
  AlertOctagon,
  Eye,
  FileBarChart,
  BarChart2,
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

const content = {
  ar: {
    helpButton: 'دليل المساعدة',
    dialogTitle: 'دليل منصة CreditAI Enterprise — منصة Order-to-Cash المتكاملة',
    overview: 'نظرة عامة',
    modules: 'الوحدات',
    policies: 'السياسات والإجراءات',
    quickRef: 'مرجع سريع',
    systemOverview: 'نظرة عامة على النظام',
    platformName: 'CreditAI Enterprise',
    platformDesc:
      'منصة متكاملة لإدارة دورة الإيرادات (Order-to-Cash) على مستوى الأنظمة العالمية مثل SAP وOracle. تشمل إدارة العملاء، المبيعات، العقود، أوامر البيع، الفواتير، التحصيل، المديونيات، الائتمان، المخاطر، الامتثال، الإدارة القانونية، الوثائق، الذكاء الاصطناعي، التقارير، سير العمل، والتكامل مع ERP.',
    keyCapabilities: 'القدرات الأساسية',
    cap1: 'إدارة دورة حياة العميل بالكامل (CRM)',
    cap2: 'أتمتة المبيعات: عروض أسعار → أوامر بيع → تسليم → فواتير',
    cap3: 'طلب ائتمان (100+ حقل) مع تحليل AI ولجنة اعتماد',
    cap4: 'التحصيل الذكي مع جدول متابعة تلقائي',
    cap5: 'إدارة المديونيات مع Aging Report ومؤشرات DSO',
    cap6: 'كشف الاحتيال والتنبؤ بالتعثر بالذكاء الاصطناعي',
    cap7: 'KYC / AML / PEP / قوائم العقوبات كشرط مسبق',
    cap8: 'إدارة القضايا القانونية والإنذارات والمحاكم',
    cap9: 'نظام إدارة وثائق (DMS) متكامل',
    cap10: 'تكامل مع SAP وOracle وMicrosoft Dynamics',
    modulesTitle: 'دليل الوحدات — 17 وحدة متكاملة',
    policiesTitle: 'السياسات والإجراءات العالمية',
    quickRefTitle: 'المرجع السريع',
    modulesList: [
      {
        name: 'لوحة التحكم التنفيذية',
        nameEn: 'Executive Dashboard',
        icon: 'BarChart3',
        desc: 'لوحة معلومات تفاعلية للمديرين التنفيذين',
        features: [
          'إجمالي العملاء والمبيعات والمديونيات',
          'الديون المتأخرة والتحصيل اليومي والشهري',
          'متوسط فترة التحصيل (DSO) ونسبة الديون المعدومة',
          'نسبة الموافقات والرفض الائتماني',
          'أعلى 20 عميلاً حسب المبيعات والمديونية',
          'العملاء الأكثر خطورة والمتوقع تعثرهم (AI)',
          'تنبؤات التدفقات النقدية وأداء الفرق',
        ],
      },
      {
        name: 'إدارة العملاء (CRM)',
        nameEn: 'Customer Management (CRM)',
        icon: 'Building2',
        desc: 'إدارة شاملة لبيانات العملاء وجهات الاتصال والمستندات',
        features: [
          'رقم العميل، الاسم، الاسم التجاري، النشاط، القطاع، الدولة، المدينة',
          'الرقم الضريبي، السجل التجاري، رقم الهوية',
          'جهات اتصال: المدير، المدير المالي، المحاسب، مدير المشتريات',
          'مستندات العميل: سجل تجاري، بطاقة ضريبية، رخصة، عقد تأسيس',
          'الميزانيات و��්රි الحساب البنكي',
          'حالة العميل و تاريخ الإنشاء',
        ],
      },
      {
        name: 'إدارة المبيعات',
        nameEn: 'Sales Management',
        icon: 'ShoppingCart',
        desc: 'عرض الأسعار → أمر البيع → التسليم → الفاتورة',
        features: [
          'عروض الأسعار: رقم العرض، المنتجات، الأسعار، الخصومات، الضريبة، الصلاحية',
          'أوامر البيع: Draft → Pending → Approved → Released → Delivered → Invoiced → Closed',
          'التسليم: المخزن، الكمية، التاريخ، السائق، السيارة',
          'استيراد البيانات من CSV/Excel',
          'تقارير المبيعات الشهرية والسنوية',
        ],
      },
      {
        name: 'إدارة العقود',
        nameEn: 'Contract Management',
        icon: 'FileSignature',
        desc: 'إنشاء وإدارة ومتابعة العقود',
        features: [
          'إنشاء العقود من قوالب جاهزة',
          'تتبع حالة العقد (نشط، منتهي، معلق)',
          'تنبيهات انتهاء الصلاحية',
          'ربط العقود بالعملاء والفواتير',
          'أرشيف العقود الرقمي',
        ],
      },
      {
        name: 'أوامر البيع',
        nameEn: 'Sales Orders',
        icon: 'ClipboardList',
        desc: 'إدارة أوامر البيع من الإصدار إلى التسليم',
        features: [
          'إنشاء أمر بيع من عرض الأسعار مباشرة',
          'حالات: Draft → Pending → Approved → Released → Delivered → Invoiced → Closed',
          'متابعة التسليم والمخزون',
          'ربط بالأوامر السابقة والتاريخ',
          'تقارير أوامر البيع المفتوحة والمغلقة',
        ],
      },
      {
        name: 'الفواتير',
        nameEn: 'Invoicing',
        icon: 'Receipt',
        desc: 'إنشاء وإرسال الفواتير الإلكترونية',
        features: [
          'إنشاء فاتورة من أمر البيع مباشرة',
          'تصدير PDF مع QR Code',
          'حساب الضريبة تلقائياً',
          'إرسال بالبريد الإلكتروني وWhatsApp',
          'API للاستيراد والتصدير',
          'تتبع حالة الفاتورة (مدفوعة، معلقة، متأخرة)',
        ],
      },
      {
        name: 'الائتمان',
        nameEn: 'Credit Management',
        icon: 'CreditCard',
        desc: 'طلب ائتمان شامل (100+ حقل) مع تحليل ذكي ولجنة اعتماد',
        features: [
          'نموذج طلب ائتمان: بيانات الشركة، الملاك، الإدارة، الحسابات البنكية',
          'الموردون، العملاء، الإيرادات، المصروفات، الأرباح، الالتزامات',
          'القروض، الضمانات، العقود، الشيكات، الأحكام القضائية',
          'التصنيف الائتماني (AAA → CCC)',
          'تحليل AI: الميزانية، التدفقات النقدية، الأرباح، الديون، المخاطر، السجل',
          'درجة ائتمانية: 94/100 → توصية: الموافقة / حد 2,000,000 / مدة 90 يوم',
          'لجنة الائتمان: محلل → مدير ائتمان → مدير مالي → مدير تنفيذي',
        ],
      },
      {
        name: 'حدود الائتمان',
        nameEn: 'Credit Limits',
        icon: 'Target',
        desc: 'إدارة حدود الائتمان لكل عميل',
        features: [
          'الحد الحالي، المستخدم، المتبقي',
          'الحد المؤقت والزيادة المؤقتة مع تاريخ الانتهاء',
          'سجل تغييرات الحدود',
          'ربط بالفواتير المعلقة',
          'تنبيهات تجاوز الحد',
        ],
      },
      {
        name: 'التحصيل',
        nameEn: 'Collections',
        icon: 'Banknote',
        desc: 'جدول متابعة تلقائي مع تصعيد ذكي',
        features: [
          'قبل 7 أيام: رسالة تذكير',
          'قبل 3 أيام: اتصال هاتفي',
          'يوم الاستحقاق: إشعار رسمي',
          'بعد 7 أيام: متابعة مكثفة',
          'بعد 15 يوم: زيارة ميدانية',
          'بعد 30 يوم: إنذار رسمي',
          'بعد 60 يوم: تسليم للإجراءات القانونية',
          'أقساط، وعود دفع، تسويات، شطب',
        ],
      },
      {
        name: 'المديونيات',
        nameEn: 'Receivables & Aging',
        icon: 'BarChart2',
        desc: 'Aging Report ومؤشرات أداء التحصيل',
        features: [
          'Aging Report: 0-30 / 31-60 / 61-90 / 91-120 / 120+ يوم',
          'DSO: Average Collection Period',
          'Collection Rate: نسبة التحصيل الفعلية',
          'Bad Debt: نسبة الديون المعدومة',
          'Average Delay: متوسط أيام التأخر',
          'تقارير يومية وأسبوعية وشهرية',
        ],
      },
      {
        name: 'المخاطر',
        nameEn: 'Risk Management',
        icon: 'Shield',
        desc: 'Risk Register مع Heat Map وتحليل مخاطر متقدم',
        features: [
          'Risk Register: الخطر، الاحتمال، التأثير، المستوى',
          'Heat Map: حرجة / مرتفعة / متوسطة / منخفضة',
          'حدود التركيز: عميل 15%، قطاع 30%، منطقة 25%',
          'اختبار الضغط: انخفاض إيرادات 20%، ارتفاع فائدة 5%',
          'الخسائر المتوقعة (IFRS 9) مع Provision',
          'تصنيف AAA → CCC لكل عميل',
        ],
      },
      {
        name: 'الامتثال',
        nameEn: 'Compliance',
        icon: 'ShieldCheck',
        desc: 'KYC / AML / PEP / قوائم العقوبات كشرط مسبق',
        features: [
          'KYC: التحقق من هوية العميل بالكامل',
          'AML: مكافحة غسل الأموال وCFT',
          'PEP: فحص الأشخاص المعنيين سياسياً',
          'قوائم العقوبات: فحص دوري تلقائي',
          'العميل الحقيقي والمستفيد النهائي',
          'التوقيع الإلكتروني',
          'عناية Due Diligence لكل عميل',
        ],
      },
      {
        name: 'الإدارة القانونية',
        nameEn: 'Legal Management',
        icon: 'Gavel',
        desc: 'إدارة القضايا والإنذارات والمحاكم والتنفيذ',
        features: [
          'فتح وإدارة القضايا القانونية',
          'إنذارات رسمية وقانونية',
          'التسويات القانونية',
          'تتبع الجلسات والمحاكم',
          'إجراءات التنفيذ الجبري',
          'إدارة المحامين والممثلين القانونيين',
        ],
      },
      {
        name: 'إدارة الوثائق (DMS)',
        nameEn: 'Document Management (DMS)',
        icon: 'FolderOpen',
        desc: 'نظام إدارة وثائق متكامل لكل عميل',
        features: [
          'العقود، الفواتير، الشيكات، الضمانات، المراسلات',
          'رفع وتخزين بأمان مع تشفير',
          'تصنيف حسب النوع والعميل والحالة',
          'البحث السريع والتصفح',
          'تتبع انتهاء الصلاحية والتنبيهات',
        ],
      },
      {
        name: 'مركز الذكاء الاصطناعي',
        nameEn: 'AI Center',
        icon: 'Brain',
        desc: 'مركز قرار ذكي بـ 7 خدمات AI متكاملة',
        features: [
          'AI Credit Scoring: تحليل ائتماني تلقائي ودرجة 94/100',
          'AI Collection: اقتراح أفضل وقت وطريقة للتحصيل',
          'AI Risk: توقع التعثر قبل حدوثه',
          'AI Fraud Detection: كشف المعاملات المشبوهة والاحتيال',
          'AI Document Reader: قراءة العقود والميزانيات واستخراج البيانات',
          'AI Financial Analysis: تحليل القوائم المالية وإبراز المؤشرات',
          'AI Forecast: تنبؤ بالتدفقات النقدية واحتمالات السداد',
        ],
      },
      {
        name: 'التقارير والتحليلات',
        nameEn: 'Reports & Analytics',
        icon: 'BarChart3',
        desc: 'تقارير شاملة ولوحات معلومات تفاعلية',
        features: [
          'تقارير Aging Report و DSO',
          'تقارير المبيعات والمديونيات',
          'تقارير المخاطر والامتثال',
          'تقارير التحصيل اليومية والشهرية',
          'تصدير PDF / Excel / CSV',
          'لوحات معلومات تفاعلية للمديرين',
        ],
      },
      {
        name: 'سير العمل',
        nameEn: 'Workflow',
        icon: 'GitBranch',
        desc: 'أتمتة سير العمل وعمليات الاعتماد',
        features: [
          'تعريف سير عمل مخصص لكل وحدة',
          'أتمتة مراحل الاعتماد (محلل → مدير → مالي → تنفيذي)',
          'تتبع حالة الطلبات والقوالب',
          'إشعارات وتذكيرات تلقائية',
          'approve / reject مع تعليقات',
        ],
      },
      {
        name: 'التكامل مع ERP',
        nameEn: 'ERP Integration',
        icon: 'Database',
        desc: 'تكامل مع SAP وOracle وMicrosoft Dynamics',
        features: [
          'مزامنة بيانات العملاء (Business Partners)',
          'استيراد فواتير المبيعات والمشتريات',
          'تحديثات الحسابات المدينة والدائنة',
          'تقارير التكامل وسجلات المزامنة',
          'Queue للمزامنة غير المتزامنة',
          'API مفتوح لأي نظام ERP',
        ],
      },
      {
        name: 'الإعدادات والنظام',
        nameEn: 'Settings & System',
        icon: 'Settings',
        desc: 'الإعدادات العامة وإدارة العملات والأ modules',
        features: [
          'إدارة العملات وأسعار الصرف',
          'إعدادات النظام العامة',
          'إدارة الإشعارات والتفضيلات',
          'إدارة القوائم (Menus) والوحدات (Modules)',
          'النسخ الاحتياطي واستعادة البيانات',
          'سجل التدقيق (Audit Trail)',
        ],
      },
    ],
    policiesContent: {
      sales: 'سياسات المبيعات',
      salesItems: [
        {
          title: 'عرض الأسعار',
          content:
            'رقم العرض + العميل + المنتجات + الأسعار + الخصومات + الضريبة + الصلاحية. صلاحية العرض 30 يوماً. الخصومات فوق 10% تتطلب اعتماد المدير المالي.',
        },
        {
          title: 'أوامر البيع',
          content:
            'حالات: Draft → Pending → Approved → Released → Delivered → Invoiced → Closed. كل حالة تتطلب اعتماداً محدداً. أمر البيع ينشأ من عرض الأسعار مباشرة.',
        },
        {
          title: 'التسليم',
          content:
            'المخزن + الكمية + التاريخ + السائق + السيارة. تأكيد التسليم بتوقيع العميل. تحديث المخزون تلقائياً.',
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
          title: 'جدول المتابعة التلقائي',
          content:
            'قبل 7 أيام: رسالة. قبل 3 أيام: اتصال. يوم الاستحقاق: إشعار. بعد 7 أيام: متابعة. بعد 15 يوم: زيارة. بعد 30 يوم: إنذار. بعد 60 يوم: قانونية.',
        },
        {
          title: 'إجراءات التصعيد',
          content:
            'تصعيد تلقائي حسب المدة: فريق التحصيل → المدير → الإدارة التنفيذية → الإدارة القانونية.',
        },
        {
          title: 'الوعود بالدفع والأقساط',
          content:
            'تسجيل الوعود بالدفع مع التاريخ والمبلغ. جدولة الأقساط تلقائياً. متابعة عند موعد الوفاء.',
        },
        {
          title: 'سياسة التسوية',
          content:
            'التسويات أقل من 10%: موافقة المدير. 10-25%: موافقة المدير المالي. أكثر من 25%: موافقة مجلس الإدارة.',
        },
        {
          title: 'سياسة الشطب',
          content:
            'يُشطب الدين بعد استنفاف جميع إجراءات التحصيل والقانوني. يتطلب توثيقاً كاملاً واعتماداً متعدد المراحل.',
        },
      ],
      credit: 'سياسات الائتمان',
      creditItems: [
        {
          title: 'نموذج طلب الائتمان',
          content:
            'أكثر من 100 حقل: بيانات الشركة، الملاك، الإدارة، الحسابات البنكية، الموردون، العملاء، الإيرادات، المصروفات، الأرباح، الالتزامات، القروض، الضمانات، العقود، الشيكات، الأحكام القضائية.',
        },
        {
          title: 'تحليل الذكاء الاصطناعي',
          content:
            'AI يحلل: الميزانية، التدفقات النقدية، الأرباح، الديون، المخاطر، السجل. يعطي درجة (94/100) وتوصية (موافقة / رفض / مراجعة) مع حد ائتماني ومدة.',
        },
        {
          title: 'لجنة الائتمان',
          content:
            'Workflow: محلل ائتمان → مدير الائتمان → المدير المالي → المدير التنفيذي. كل مرحلة تتطلب موافقة مع تعليقات.',
        },
        {
          title: 'حدود التعرض',
          content:
            'الحد الأقصى لكل عميل: 15% من رأس المال. الحد الأقصى لكل قطاع: 30%. الحد الأقصى لمنطقة: 25%. مراجعة كل 6 أشهر.',
        },
        {
          title: 'متطلبات الضمانات',
          content:
            'ضمانات مالية: كفالة بنكية، خطاب ضمان. ضمانات عقارية: تقييم مستقل، تأمين. ضمانات شخصية: كفالة شخصية.',
        },
      ],
      risk: 'سياسات المخاطر',
      riskItems: [
        {
          title: 'Risk Register',
          content:
            'كل خطر له: الوصف، الاحتمال (عالي/متوسط/منخفض)، التأثير (عالي/متوسط/منخفض)، المستوى (حرج/مرتفع/متوسط/منخفض).',
        },
        {
          title: 'Heat Map',
          content:
            'مصفوفة 3×3: الاحتمال × التأثير. الحمراء = حرجة، البرتقالية = مرتفعة، الصفراء = متوسطة، الخضراء = منخفضة.',
        },
        {
          title: 'حدود التركيز',
          content:
            'عميل واحد: 15% من رأس المال. قطاع واحد: 30% من المحفظة. منطقة جغرافية: 25%. مراجعة كل 6 أشهر.',
        },
        {
          title: 'اختبار الضغط',
          content:
            'سيناريوهات: انخفاض إيرادات 20%، ارتفاع أسعار الفائدة 5%، تراجع سوقي 30%. تحليل الأثر على المحفظة الإئتمانية.',
        },
        {
          title: 'الخسائر المتوقعة (IFRS 9)',
          content:
            'Provision: 1-30 يوم: 1%. 31-60: 5%. 61-90: 20%. 91-180: 50%. 180+: 100%. نماذج احتمالية للتوقعات.',
        },
      ],
      compliance: 'سياسات الامتثال',
      complianceItems: [
        {
          title: 'KYC',
          content:
            'التحقق من هوية العميل بالكامل: رقم الهوية، السجل التجاري، الرقم الضريبي، العنوان، جهات الاتصال.',
        },
        {
          title: 'AML / CFT',
          content:
            'مكافحة غسل الأموال وتمويل الإرهاب. فحص المعاملات المشبوهة. تقارير المعاملات الكبيرة.',
        },
        {
          title: 'PEP وقوائم العقوبات',
          content:
            'فحص الأشخاص المعنيين سياسياً (PEP). فحص دوري لقوائم العقوبات الدولية والمحلية.',
        },
        {
          title: 'العميل الحقيقي والمستفيد النهائي',
          content:
            'تحديد الهوية الحقيقية وراء الشخصيات الاعتبارية. التأكد من المستفيد النهائي من كل معاملة.',
        },
        {
          title: 'عناية Due Diligence',
          content:
            'due diligence شامل لكل عميل قبل التعامل. مراجعة دورية كل 12 شهراً. مراجعة فورية عند تغير المخاطر.',
        },
      ],
      invoicing: 'سياسات الفواتير',
      invoicingItems: [
        {
          title: 'إنشاء الفاتورة',
          content:
            'فاتورة تنشأ من أمر البيع مباشرة. تتضمن المنتجات، الأسعار، الضريبة، الخصومات، الإجمالي.',
        },
        {
          title: 'PDF و QR Code',
          content:
            'كل فاتورة تُصدَر بصيغة PDF مع QR Code للتحقق. رابط تحقق إلكتروني.',
        },
        {
          title: 'الإرسال',
          content:
            'إرسال بالبريد الإلكتروني مباشرة. إرسال عبر WhatsApp. API لإرسال الفواتير لأي نظام.',
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
    integration: {
      title: 'خريطة التكامل',
      subtitle: 'تكامل الوحدات وتدفق البيانات بين الأنظمة',
      flow: {
        sales: 'المبيعات',
        collections: 'التحصيل',
        credit: 'الائتمان',
        risk: 'المخاطر',
        ai: 'الذكاء الاصطناعي',
        dashboard: 'لوحة التحكم',
        compliance: 'الامتثال',
      },
      connections: [
        { from: 'المبيعات', to: 'الفواتير', desc: 'عرض أسعار → أمر بيع → تسليم → فاتورة (PDF + QR + WhatsApp)' },
        { from: 'الفواتير', to: 'التحصيل', desc: 'فواتير المبيعات → حساب أيام التأخر → جدول متابعة تلقائي' },
        { from: 'المبيعات + الائتمان', to: 'المخاطر', desc: 'بيانات المبيعات + طلبات الائتمان → AI risk_score → تصنيف (AAA→CCC)' },
        { from: 'الائتمان', to: 'دورة كاملة', desc: 'طلب (100+ حقل) → تحليل AI → لجنة → تصويت → حدود + ضمانات' },
        { from: 'الامتثال', to: 'كل عميل', desc: 'KYC / AML / PEP / عقوبات → شرط مسبق للتعامل → عناية Due Diligence' },
        { from: 'المبيعات + الائتمان + المخاطر', to: 'لوحة التحكم', desc: 'إحصائيات حية: DSO، Collection Rate، Bad Debt، أعلى 20 عميل' },
        { from: 'AI Center', to: 'كل الوحدات', desc: '7 خدمات: Credit Scoring, Collection, Risk, Fraud, Document Reader, Analysis, Forecast' },
      ],
      status: [
        { module: 'المبيعات → الفواتير → التحصيل', status: 'مكتمل', icon: 'check' },
        { module: 'طلب الائتمان + تحليل AI + لجنة', status: 'مكتمل', icon: 'check' },
        { module: 'حدود الائتمان + الضمانات', status: 'مكتمل', icon: 'check' },
        { module: 'KYC / AML / PEP / عقوبات', status: 'مكتمل', icon: 'check' },
        { module: 'Aging Report ومؤشرات DSO', status: 'مكتمل', icon: 'check' },
        { module: 'Risk Register و Heat Map', status: 'مكتمل', icon: 'check' },
      ],
      remaining: [
        { module: 'إدارة العقود (Contract Management)', status: 'يحتاج تطوير', icon: 'warning' },
        { module: 'AI Fraud Detection', status: 'يحتاج تطوير', icon: 'warning' },
        { module: 'AI Document Reader', status: 'يحتاج تطوير', icon: 'warning' },
        { module: 'تكامل مع SAP / Oracle', status: 'يحتاج تطوير', icon: 'warning' },
      ],
    },
  },
  en: {
    helpButton: 'Help Guide',
    dialogTitle: 'CreditAI Enterprise Guide — Order-to-Cash Platform',
    overview: 'Overview',
    modules: 'Modules',
    policies: 'Policies & Procedures',
    quickRef: 'Quick Reference',
    systemOverview: 'System Overview',
    platformName: 'CreditAI Enterprise',
    platformDesc:
      'A comprehensive Order-to-Cash platform matching SAP, Oracle, and Microsoft Dynamics. Covers CRM, Sales, Contracts, Sales Orders, Invoicing, Collections, Receivables, Credit, Risk, Compliance, Legal, Documents (DMS), AI Center, Reports, Workflow, and ERP Integration.',
    keyCapabilities: 'Key Capabilities',
    cap1: 'Full customer lifecycle management (CRM)',
    cap2: 'Sales automation: Quotation → Order → Delivery → Invoice',
    cap3: 'Credit application (100+ fields) with AI analysis and committee approval',
    cap4: 'Smart collections with automated follow-up schedule',
    cap5: 'Receivables management with Aging Report and DSO metrics',
    cap6: 'Fraud detection and default prediction with AI',
    cap7: 'KYC / AML / PEP / Sanctions as prerequisite',
    cap8: 'Legal case management, court tracking, and enforcement',
    cap9: 'Integrated Document Management System (DMS)',
    cap10: 'SAP, Oracle, and Microsoft Dynamics integration',
    modulesTitle: 'Module Guide — 17 Integrated Modules',
    policiesTitle: 'Global Policies & Procedures',
    quickRefTitle: 'Quick Reference',
    modulesList: [
      {
        name: 'Executive Dashboard',
        nameEn: 'Executive Dashboard',
        icon: 'BarChart3',
        desc: 'Interactive dashboard for executives',
        features: [
          'Total customers, sales, and receivables',
          'Overdue debts, daily and monthly collections',
          'DSO, Collection Rate, Bad Debt metrics',
          'Credit approval vs rejection rates',
          'Top 20 customers by sales and receivables',
          'Highest-risk and predicted-default customers (AI)',
          'Cash flow forecasts and team performance',
        ],
      },
      {
        name: 'Customer Management (CRM)',
        nameEn: 'Customer Management (CRM)',
        icon: 'Building2',
        desc: 'Comprehensive customer data, contacts, and document management',
        features: [
          'Customer ID, name, trade name, activity, sector, country, city',
          'Tax ID, commercial registration, national ID',
          'Contacts: Director, CFO, Accountant, Procurement Manager',
          'Documents: Commercial register, tax card, license, incorporation deed',
          'Budgets and bank statements',
          'Customer status and creation date',
        ],
      },
      {
        name: 'Sales Management',
        nameEn: 'Sales Management',
        icon: 'ShoppingCart',
        desc: 'Quotation → Sales Order → Delivery → Invoice',
        features: [
          'Quotations: quote number, products, prices, discounts, tax, validity',
          'Sales Orders: Draft → Pending → Approved → Released → Delivered → Invoiced → Closed',
          'Delivery: warehouse, quantity, date, driver, vehicle',
          'Import data from CSV/Excel',
          'Monthly and annual sales reports',
        ],
      },
      {
        name: 'Contract Management',
        nameEn: 'Contract Management',
        icon: 'FileSignature',
        desc: 'Create, manage, and track contracts',
        features: [
          'Create contracts from templates',
          'Track contract status (active, expired, pending)',
          'Expiration alerts and renewals',
          'Link contracts to customers and invoices',
          'Digital contract archive',
        ],
      },
      {
        name: 'Sales Orders',
        nameEn: 'Sales Orders',
        icon: 'ClipboardList',
        desc: 'Manage sales orders from issuance to delivery',
        features: [
          'Create sales order directly from quotation',
          'Statuses: Draft → Pending → Approved → Released → Delivered → Invoiced → Closed',
          'Track delivery and inventory',
          'Link to previous orders and history',
          'Open and closed order reports',
        ],
      },
      {
        name: 'Invoicing',
        nameEn: 'Invoicing',
        icon: 'Receipt',
        desc: 'Create and send electronic invoices',
        features: [
          'Create invoice directly from sales order',
          'Export PDF with QR Code',
          'Automatic tax calculation',
          'Send via email and WhatsApp',
          'API for import/export',
          'Track invoice status (paid, pending, overdue)',
        ],
      },
      {
        name: 'Credit Management',
        nameEn: 'Credit Management',
        icon: 'CreditCard',
        desc: 'Comprehensive credit application (100+ fields) with AI analysis and committee',
        features: [
          'Application form: company data, ownership, management, bank accounts',
          'Suppliers, customers, revenue, expenses, profits, obligations',
          'Loans, guarantees, contracts, checks, legal judgments',
          'Credit rating (AAA → CCC)',
          'AI analysis: budget, cash flows, profits, debts, risk, history',
          'Score 94/100 → Recommendation: Approve / Limit 2M / 90 days',
          'Committee: Analyst → Credit Manager → CFO → CEO',
        ],
      },
      {
        name: 'Credit Limits',
        nameEn: 'Credit Limits',
        icon: 'Target',
        desc: 'Manage credit limits per customer',
        features: [
          'Current limit, utilized, available',
          'Temporary limit and temporary increase with expiry',
          'Limit change history',
          'Link to pending invoices',
          'Over-limit alerts',
        ],
      },
      {
        name: 'Collections',
        nameEn: 'Collections',
        icon: 'Banknote',
        desc: 'Automated follow-up schedule with smart escalation',
        features: [
          '7 days before: reminder message',
          '3 days before: phone call',
          'Due date: official notification',
          'After 7 days: intensive follow-up',
          'After 15 days: field visit',
          'After 30 days: formal warning',
          'After 60 days: legal action',
          'Installments, payment promises, settlements, write-offs',
        ],
      },
      {
        name: 'Receivables & Aging',
        nameEn: 'Receivables & Aging',
        icon: 'BarChart2',
        desc: 'Aging Report and collection performance metrics',
        features: [
          'Aging Report: 0-30 / 31-60 / 61-90 / 91-120 / 120+ days',
          'DSO: Average Collection Period',
          'Collection Rate: actual collection percentage',
          'Bad Debt: bad debt ratio',
          'Average Delay: average days overdue',
          'Daily, weekly, and monthly reports',
        ],
      },
      {
        name: 'Risk Management',
        nameEn: 'Risk Management',
        icon: 'Shield',
        desc: 'Risk Register with Heat Map and advanced risk analysis',
        features: [
          'Risk Register: risk, probability, impact, level',
          'Heat Map: Critical / High / Medium / Low',
          'Concentration limits: customer 15%, sector 30%, region 25%',
          'Stress testing: revenue drop 20%, interest rate +5%',
          'Expected losses (IFRS 9) with Provision',
          'Rating AAA → CCC for each customer',
        ],
      },
      {
        name: 'Compliance',
        nameEn: 'Compliance',
        icon: 'ShieldCheck',
        desc: 'KYC / AML / PEP / Sanctions as prerequisite',
        features: [
          'KYC: full customer identity verification',
          'AML: Anti-Money Laundering and CFT',
          'PEP: Politically Exposed Persons screening',
          'Sanctions: automated periodic screening',
          'Ultimate Beneficial Owner (UBO)',
          'Electronic signatures',
          'Due Diligence for every customer',
        ],
      },
      {
        name: 'Legal Management',
        nameEn: 'Legal Management',
        icon: 'Gavel',
        desc: 'Case management, notices, courts, and enforcement',
        features: [
          'Open and manage legal cases',
          'Formal and legal notices',
          'Legal settlements',
          'Court session tracking',
          'Enforcement proceedings',
          'Lawyer and legal representative management',
        ],
      },
      {
        name: 'Document Management (DMS)',
        nameEn: 'Document Management (DMS)',
        icon: 'FolderOpen',
        desc: 'Integrated document management for every customer',
        features: [
          'Contracts, invoices, checks, guarantees, correspondence',
          'Secure upload and encrypted storage',
          'Classification by type, customer, and status',
          'Quick search and browsing',
          'Expiration tracking and alerts',
        ],
      },
      {
        name: 'AI Center',
        nameEn: 'AI Center',
        icon: 'Brain',
        desc: 'Smart decision center with 7 integrated AI services',
        features: [
          'AI Credit Scoring: automatic analysis and score 94/100',
          'AI Collection: suggest best time and method for collection',
          'AI Risk: predict default before it happens',
          'AI Fraud Detection: detect suspicious transactions',
          'AI Document Reader: read contracts and extract data automatically',
          'AI Financial Analysis: analyze financial statements and highlight KPIs',
          'AI Forecast: predict cash flows and payment probabilities',
        ],
      },
      {
        name: 'Reports & Analytics',
        nameEn: 'Reports & Analytics',
        icon: 'BarChart3',
        desc: 'Comprehensive reports and interactive dashboards',
        features: [
          'Aging Report and DSO reports',
          'Sales and receivables reports',
          'Risk and compliance reports',
          'Daily and monthly collection reports',
          'Export PDF / Excel / CSV',
          'Interactive executive dashboards',
        ],
      },
      {
        name: 'Workflow',
        nameEn: 'Workflow',
        icon: 'GitBranch',
        desc: 'Automate workflows and approval processes',
        features: [
          'Define custom workflows per module',
          'Automate approval stages (analyst → manager → finance → executive)',
          'Track request status and templates',
          'Automatic notifications and reminders',
          'Approve / reject with comments',
        ],
      },
      {
        name: 'ERP Integration',
        nameEn: 'ERP Integration',
        icon: 'Database',
        desc: 'Integration with SAP, Oracle, and Microsoft Dynamics',
        features: [
          'Customer data synchronization (Business Partners)',
          'Import sales and purchase invoices',
          'Debit and credit account updates',
          'Integration reports and sync logs',
          'Async sync queue',
          'Open API for any ERP system',
        ],
      },
      {
        name: 'Settings & System',
        nameEn: 'Settings & System',
        icon: 'Settings',
        desc: 'General settings, currency management, and system configuration',
        features: [
          'Currency and exchange rate management',
          'General system settings',
          'Notification and preference management',
          'Menu and module management',
          'Backup and data recovery',
          'Audit trail',
        ],
      },
    ],
    policiesContent: {
      sales: 'Sales Policies',
      salesItems: [
        {
          title: 'Quotation',
          content:
            'Quote number + customer + products + prices + discounts + tax + validity. Quote valid for 30 days. Discounts above 10% require CFO approval.',
        },
        {
          title: 'Sales Orders',
          content:
            'Statuses: Draft → Pending → Approved → Released → Delivered → Invoiced → Closed. Each status requires specific approval. Order created directly from quotation.',
        },
        {
          title: 'Delivery',
          content:
            'Warehouse + quantity + date + driver + vehicle. Delivery confirmed with customer signature. Inventory updated automatically.',
        },
        {
          title: 'Returns & Discounts',
          content:
            'Returns accepted with sales management approval. Discounts require prior documentation and CFO approval for large amounts.',
        },
      ],
      collections: 'Collection Procedures',
      collectionsItems: [
        {
          title: 'Automated Follow-up Schedule',
          content:
            '7 days before: reminder. 3 days before: phone call. Due date: notification. After 7 days: follow-up. After 15 days: field visit. After 30 days: formal notice. After 60 days: legal action.',
        },
        {
          title: 'Escalation Procedures',
          content:
            'Automatic escalation by duration: Collection team → Manager → Executive management → Legal department.',
        },
        {
          title: 'Payment Promises & Installments',
          content:
            'Record payment promises with date and amount. Schedule installments automatically. Follow up on due dates.',
        },
        {
          title: 'Settlement Policy',
          content:
            'Settlements below 10%: manager approval. 10-25%: CFO approval. Above 25%: board approval.',
        },
        {
          title: 'Write-off Policy',
          content:
            'Debt written off after exhausting all collection and legal measures. Requires complete documentation and multi-level approval.',
        },
      ],
      credit: 'Credit Policies',
      creditItems: [
        {
          title: 'Credit Application Form',
          content:
            '100+ fields: company data, ownership, management, bank accounts, suppliers, customers, revenue, expenses, profits, obligations, loans, guarantees, contracts, checks, legal judgments.',
        },
        {
          title: 'AI Analysis',
          content:
            'AI analyzes: budget, cash flows, profits, debts, risk, history. Provides score (94/100) and recommendation (approve/reject/review) with credit limit and duration.',
        },
        {
          title: 'Credit Committee',
          content:
            'Workflow: Credit analyst → Credit manager → CFO → CEO. Each stage requires approval with comments.',
        },
        {
          title: 'Exposure Limits',
          content:
            'Maximum per customer: 15% of capital. Maximum per sector: 30% of portfolio. Maximum per region: 25%. Review every 6 months.',
        },
        {
          title: 'Collateral Requirements',
          content:
            'Financial: bank guarantee, letter of guarantee. Real estate: independent appraisal, insurance. Personal: personal guarantee.',
        },
      ],
      risk: 'Risk Policies',
      riskItems: [
        {
          title: 'Risk Register',
          content:
            'Each risk has: description, probability (high/medium/low), impact (high/medium/low), level (critical/high/medium/low).',
        },
        {
          title: 'Heat Map',
          content:
            '3×3 matrix: Probability × Impact. Red = Critical, Orange = High, Yellow = Medium, Green = Low.',
        },
        {
          title: 'Concentration Limits',
          content:
            'Single customer: 15% of capital. Single sector: 30% of portfolio. Single region: 25%. Review every 6 months.',
        },
        {
          title: 'Stress Testing',
          content:
            'Scenarios: revenue drop 20%, interest rate increase 5%, market decline 30%. Analyze impact on credit portfolio.',
        },
        {
          title: 'Expected Losses (IFRS 9)',
          content:
            'Provision: 1-30 days: 1%. 31-60: 5%. 61-90: 20%. 91-180: 50%. 180+: 100%. Probabilistic models for forecasts.',
        },
      ],
      compliance: 'Compliance Policies',
      complianceItems: [
        {
          title: 'KYC',
          content:
            'Full customer identity verification: national ID, commercial registration, tax ID, address, contacts.',
        },
        {
          title: 'AML / CFT',
          content:
            'Anti-money laundering and counter-terrorism financing. Suspicious transaction reports. Large transaction reports.',
        },
        {
          title: 'PEP & Sanctions',
          content:
            'Politically Exposed Persons screening. Periodic screening against international and local sanctions lists.',
        },
        {
          title: 'Ultimate Beneficial Owner',
          content:
            'Identify the real person behind legal entities. Verify the ultimate beneficiary of every transaction.',
        },
        {
          title: 'Due Diligence',
          content:
            'Comprehensive due diligence for every customer before engagement. Periodic review every 12 months. Immediate review on risk change.',
        },
      ],
      invoicing: 'Invoicing Policies',
      invoicingItems: [
        {
          title: 'Invoice Creation',
          content:
            'Invoice created directly from sales order. Includes products, prices, tax, discounts, total.',
        },
        {
          title: 'PDF & QR Code',
          content:
            'Every invoice exported as PDF with QR Code for verification. Electronic verification link.',
        },
        {
          title: 'Sending',
          content:
            'Send via email directly. Send via WhatsApp. API for sending invoices to any system.',
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
        { keys: 'Esc', action: 'Close popup' },
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
    integration: {
      title: 'Integration Map',
      subtitle: 'Unit integration and data flow between systems',
      flow: {
        sales: 'Sales',
        collections: 'Collections',
        credit: 'Credit',
        risk: 'Risk',
        ai: 'AI',
        dashboard: 'Dashboard',
        compliance: 'Compliance',
      },
      connections: [
        { from: 'Sales', to: 'Invoicing', desc: 'Quotation → Order → Delivery → Invoice (PDF + QR + WhatsApp)' },
        { from: 'Invoicing', to: 'Collections', desc: 'Sales invoices → Overdue days → Automated follow-up schedule' },
        { from: 'Sales + Credit', to: 'Risk', desc: 'Sales data + credit requests → AI risk_score → Rating (AAA→CCC)' },
        { from: 'Credit', to: 'Full Cycle', desc: 'Application (100+ fields) → AI analysis → Committee → Vote → Limits + Collateral' },
        { from: 'Compliance', to: 'Every Customer', desc: 'KYC / AML / PEP / Sanctions → Prerequisite → Due Diligence' },
        { from: 'Sales + Credit + Risk', to: 'Dashboard', desc: 'Live stats: DSO, Collection Rate, Bad Debt, Top 20 customers' },
        { from: 'AI Center', to: 'All Modules', desc: '7 services: Credit Scoring, Collection, Risk, Fraud, Document Reader, Analysis, Forecast' },
      ],
      status: [
        { module: 'Sales → Invoicing → Collections', status: 'Completed', icon: 'check' },
        { module: 'Credit Application + AI + Committee', status: 'Completed', icon: 'check' },
        { module: 'Credit Limits + Collateral', status: 'Completed', icon: 'check' },
        { module: 'KYC / AML / PEP / Sanctions', status: 'Completed', icon: 'check' },
        { module: 'Aging Report & DSO Metrics', status: 'Completed', icon: 'check' },
        { module: 'Risk Register & Heat Map', status: 'Completed', icon: 'check' },
      ],
      remaining: [
        { module: 'Contract Management', status: 'Needs Development', icon: 'warning' },
        { module: 'AI Fraud Detection', status: 'Needs Development', icon: 'warning' },
        { module: 'AI Document Reader', status: 'Needs Development', icon: 'warning' },
        { module: 'SAP / Oracle Integration', status: 'Needs Development', icon: 'warning' },
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
  FileSignature,
  ClipboardList,
  Truck,
  Receipt,
  Gavel,
  Search,
  MessageSquare,
  AlertOctagon,
  Eye,
  FileBarChart,
  BarChart2,
};

export function HelpGuide() {
  const { locale } = useLanguage();
  const [open, setOpen] = useState(false);
  const c = content[locale] || content.en;

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon" className="h-8 w-8">
          <HelpCircle className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="flex h-[85vh] max-w-4xl flex-col p-0">
        <DialogHeader className="border-b px-6 py-4">
          <DialogTitle className="text-lg">{c.dialogTitle}</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="overview" className="flex flex-1 flex-col overflow-hidden">
          <div className="border-b px-6">
            <TabsList className="h-auto w-full justify-start gap-1 bg-transparent p-0">
              <TabsTrigger
                value="overview"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <BookOpen className="mr-2 h-4 w-4" />
                {c.overview}
              </TabsTrigger>
              <TabsTrigger
                value="modules"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <Layers className="mr-2 h-4 w-4" />
                {c.modules}
              </TabsTrigger>
              <TabsTrigger
                value="policies"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <BookMarked className="mr-2 h-4 w-4" />
                {c.policies}
              </TabsTrigger>
              <TabsTrigger
                value="quickref"
                className="rounded-none border-b-2 border-transparent px-4 py-3 text-sm data-[state=active]:border-primary data-[state=active]:bg-transparent data-[state=active]:shadow-none"
              >
                <Keyboard className="mr-2 h-4 w-4" />
                {c.quickRef}
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
                      <h3 className="text-xl font-bold">{c.platformName}</h3>
                      <p className="text-sm text-muted-foreground">{c.systemOverview}</p>
                    </div>
                  </div>
                  <p className="text-sm leading-relaxed text-muted-foreground">
                    {c.platformDesc}
                  </p>
                </div>

                <div>
                  <h4 className="mb-3 text-sm font-semibold">{c.keyCapabilities}</h4>
                  <div className="grid gap-2 sm:grid-cols-2">
                    {[c.cap1, c.cap2, c.cap3, c.cap4, c.cap5, c.cap6, c.cap7, c.cap8, c.cap9, c.cap10].map(
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
                {c.modulesList.map((mod, i) => {
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
                    <h4 className="font-semibold">{c.policiesContent.sales}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {c.policiesContent.salesItems.map((item, i) => (
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

                {/* Invoicing Policies */}
                <div>
                  <div className="mb-3 flex items-center gap-2">
                    <Receipt className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{c.policiesContent.invoicing}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {c.policiesContent.invoicingItems.map((item, i) => (
                      <AccordionItem key={i} value={`invoicing-${i}`} className="rounded-md border px-4">
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
                    <h4 className="font-semibold">{c.policiesContent.collections}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {c.policiesContent.collectionsItems.map((item, i) => (
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
                    <h4 className="font-semibold">{c.policiesContent.credit}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {c.policiesContent.creditItems.map((item, i) => (
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
                    <h4 className="font-semibold">{c.policiesContent.risk}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {c.policiesContent.riskItems.map((item, i) => (
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

                <div className="h-px bg-border" />

                {/* Compliance Policies */}
                <div>
                  <div className="mb-3 flex items-center gap-2">
                    <Shield className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{c.policiesContent.compliance}</h4>
                  </div>
                  <Accordion type="multiple" className="space-y-1">
                    {c.policiesContent.complianceItems.map((item, i) => (
                      <AccordionItem key={i} value={`compliance-${i}`} className="rounded-md border px-4">
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
                    <h4 className="font-semibold">{c.shortcuts.title}</h4>
                  </div>
                  <div className="space-y-2">
                    {c.shortcuts.items.map((item, i) => (
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
                    <h4 className="font-semibold">{c.navTips.title}</h4>
                  </div>
                  <ul className="space-y-2">
                    {c.navTips.items.map((tip, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                        <TrendingUp className="mt-1 h-3.5 w-3.5 shrink-0 text-primary" />
                        <span>{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Integration Map */}
                <div className="rounded-lg border bg-card p-5">
                  <div className="mb-4 flex items-center gap-2">
                    <GitBranch className="h-5 w-5 text-primary" />
                    <h4 className="font-semibold">{c.integration.title}</h4>
                  </div>
                  <p className="mb-4 text-sm text-muted-foreground">{c.integration.subtitle}</p>

                  {/* Flow Diagram */}
                  <div className="mb-5 flex flex-wrap items-center justify-center gap-2 rounded-lg bg-muted/50 p-4">
                    {[
                      c.integration.flow.sales,
                      c.integration.flow.collections,
                      c.integration.flow.credit,
                      c.integration.flow.risk,
                    ].map((step, i, arr) => (
                      <div key={i} className="flex items-center gap-2">
                        <div className="rounded-md border bg-background px-3 py-1.5 text-xs font-medium">{step}</div>
                        {i < arr.length - 1 && <ArrowRight className="h-4 w-4 text-primary" />}
                      </div>
                    ))}
                  </div>

                  {/* Connections */}
                  <div className="mb-4">
                    <h5 className="mb-2 text-xs font-semibold uppercase text-muted-foreground">
                      {locale === 'ar' ? 'التكاملات النشطة' : 'Active Integrations'}
                    </h5>
                    <div className="space-y-2">
                      {c.integration.connections.map((conn, i) => (
                        <div key={i} className="flex items-start gap-2 rounded-md border p-3 text-sm">
                          <CheckCircle className="mt-0.5 h-4 w-4 shrink-0 text-green-500" />
                          <div>
                            <span className="font-medium">{conn.from} → {conn.to}</span>
                            <p className="text-xs text-muted-foreground">{conn.desc}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Status */}
                  <div className="mb-4">
                    <h5 className="mb-2 text-xs font-semibold uppercase text-muted-foreground">
                      {locale === 'ar' ? 'حالة الوحدات' : 'Module Status'}
                    </h5>
                    <div className="grid gap-2 sm:grid-cols-2">
                      {c.integration.status.map((s, i) => (
                        <div key={i} className="flex items-center gap-2 rounded-md border border-green-200 bg-green-50 p-2.5 text-sm dark:border-green-900 dark:bg-green-950">
                          <CheckCircle className="h-4 w-4 text-green-600" />
                          <span className="font-medium">{s.module}</span>
                          <Badge variant="outline" className="ms-auto text-xs text-green-600">{s.status}</Badge>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Remaining */}
                  <div>
                    <h5 className="mb-2 text-xs font-semibold uppercase text-muted-foreground">
                      {locale === 'ar' ? 'يحتاج تطوير' : 'Needs Development'}
                    </h5>
                    <div className="grid gap-2 sm:grid-cols-2">
                      {c.integration.remaining.map((r, i) => (
                        <div key={i} className="flex items-center gap-2 rounded-md border border-amber-200 bg-amber-50 p-2.5 text-sm dark:border-amber-900 dark:bg-amber-950">
                          <AlertTriangle className="h-4 w-4 text-amber-600" />
                          <span className="font-medium">{r.module}</span>
                          <Badge variant="outline" className="ms-auto text-xs text-amber-600">{r.status}</Badge>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>
          </ScrollArea>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
