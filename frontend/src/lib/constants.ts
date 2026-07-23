/**
 * Application Constants
 * يدعم التشغيل المحلي والإنتاج تلقائياً
 */

export const APP_NAME =
  process.env.NEXT_PUBLIC_APP_NAME || "CreditAI Enterprise";

export const APP_VERSION =
  process.env.NEXT_PUBLIC_APP_VERSION || "1.0.0";


// تحديد بيئة التشغيل
const isProduction =
  process.env.NODE_ENV === "production";


// رابط الـ API
export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (
    isProduction
      ? "https://creditai-backend-477s.onrender.com/api/v1"
      : "http://localhost:8000/api/v1"
  );


export const DEFAULT_LOCALE =
  process.env.NEXT_PUBLIC_DEFAULT_LOCALE || "ar";


export const SUPPORTED_LOCALES =
  process.env.NEXT_PUBLIC_SUPPORTED_LOCALES?.split(",") || [
    "ar",
    "en",
  ];


// Auth
export const TOKEN_KEY = "accessToken";
export const REFRESH_TOKEN_KEY = "refreshToken";


// API Settings
export const API_TIMEOUT = 30000;


// Routes
export const ROUTES = {
  LOGIN: "/login",
  DASHBOARD: "/",
  PROFILE: "/profile",
};