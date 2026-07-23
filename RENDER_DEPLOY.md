# CreditAI Enterprise - دليل النشر على Render

## لماذا Render؟
- **مجاني بالكامل** — خطة مجانية للخادم وقاعدة البيانات
- **قاعدة بيانات PostgreSQL مجانية** — 90 يوم احتفاظ بالبيانات
- **نشر تلقائي** — ربط GitHub للنشر التلقائي
- **بدون بطاقة ائتمان** — لا حاجة لإدخال بيانات الدفع

---

## خطوات النشر

### الخطوة 1: رفع المشروع على GitHub
```bash
cd D:\ghith\CreditAI
git init
git add .
git commit -m "Initial CreditAI Enterprise Platform"
git remote add origin https://github.com/YOUR_USERNAME/CreditAI.git
git push -u origin main
```

### الخطوة 2: إنشاء حساب على Render
1. اذهب إلى https://render.com
2. سجل الدخول بحساب GitHub
3. اضغط "New +" → "Blueprint"
4. اختر مستودع GitHub الخاص بك
5. اضغط "Apply Blueprint"

### الخطوة 3: انتظار البناء
- سيقوم Render ببناء 3 خدمات تلقائياً:
  - **creditai-db** — قاعدة بيانات PostgreSQL
  - **creditai-backend** — خادم FastAPI
  - **creditai-frontend** — واجهة Next.js
- قد يستغرق البناء 5-10 دقائق

### الخطوة 4: تهيئة قاعدة البيانات
بعد بناء Backend، اذهب إلى Backend Service → Shell وأدخل:
```bash
python -m app.init_db
```
أو انتظر التهيئة التلقائية (تتم عند أول تشغيل).

### الخطوة 5: اختبار التطبيق
- Backend: https://creditai-backend.onrender.com/docs
- Frontend: https://creditai-frontend.onrender.com
- تسجيل الدخول: `admin@creditai.com` / `Admin@123`

---

## بيانات الدخول الافتراضية
| الحقل | القيمة |
|--------|--------|
| البريد الإلكتروني | admin@creditai.com |
| كلمة المرور | Admin@123 |

---

## إعدادات بيئية مهمة

| المتغير | الوصف | القيمة |
|---------|-------|--------|
| DATABASE_URL | رابط قاعدة البيانات | (تلقائي من Render) |
| SECRET_KEY | مفتاح الأمان | (تلقائي) |
| CORS_ORIGINS | مصادر CORS | `["https://creditai-frontend.onrender.com"]` |
| DEBUG | وضع التطوير | `false` |
| ENVIRONMENT | البيئة | `production` |

---

## ملاحظات مهمة

### قاعدة البيانات المجانية
- Render يوفر 90 يوم احتفاظ بالبيانات على الخطة المجانية
- إذا لم تستخدم قاعدة البيانات لأكثر من 90 يوم، قد تُحذف البيانات
- يُنصح بالاشتراك في الخطة المدفوعة ($7/شهر) للحفاظ على البيانات

### وقت البناء الأول
- Backend: 3-5 دقائق
- Frontend: 5-8 دقائق
- قاعدة البيانات: 1-2 دقائق

### التحديثات التلقائية
- عند دفع تغييرات جديدة إلى GitHub، سيتم نشرها تلقائياً
- يمكن تعطيل النشر التلقائي من إعدادات الخدمة

---

## استكمال النشر يدوياً (بديل عن Blueprint)

### إنشاء قاعدة البيانات
1. Render → New + → PostgreSQL
2. اسم: `creditai-db`
3. خطة: Free
4. انسخ رابط الاتصال

### إنشاء Backend
1. Render → New + → Web Service
2. ربط GitHub
3. Dockerfile: `./Dockerfile`
4. إضافة متغيرات البيئة أعلاه

### إنشاء Frontend
1. Render → New + → Web Service
2. ربط GitHub
3. Dockerfile: `./frontend/Dockerfile`
4. NEXT_PUBLIC_API_URL: رابط Backend

---

## الصيانة

### مراقبة السجلات
- اذهب إلى الخدمة → Logs لمتابعة السجلات

### التحديث
```bash
git add .
git commit -m "Update"
git push
```
سيتم النشر تلقائياً.

### النسخ الاحتياطي
```bash
# من Render Shell
pg_dump $DATABASE_URL > backup.sql
```

---

## دعم有问题؟
- تحقق من السجلات: Backend → Logs
- تحقق من الصحة: https://creditai-backend.onrender.com/health
- تحقق من قاعدة البيانات: Backend → Shell → `python -c "from app.database import *; print('DB OK')"`
