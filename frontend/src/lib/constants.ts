/**
 * Application Constants
 * Local + Production support
 */


export const APP_NAME =
  process.env.NEXT_PUBLIC_APP_NAME ||
  "CreditAI Enterprise";


export const APP_VERSION =
  process.env.NEXT_PUBLIC_APP_VERSION ||
  "1.0.0";



/**
 * API URL
 *
 * Local:
 * http://localhost:8000/api/v1
 *
 * Production:
 * https://creditai-backend-477s.onrender.com/api/v1
 */

const DEFAULT_LOCAL_API =
  "http://localhost:8000/api/v1";


const DEFAULT_PRODUCTION_API =
  "https://creditai-backend-477s.onrender.com/api/v1";



export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  (
    process.env.NODE_ENV === "production"
      ? DEFAULT_PRODUCTION_API
      : DEFAULT_LOCAL_API
  );



export const API_TIMEOUT =
  Number(
    process.env.NEXT_PUBLIC_API_TIMEOUT
  ) || 60000;



export const DEFAULT_LOCALE =
  process.env.NEXT_PUBLIC_DEFAULT_LOCALE ||
  "ar";



export const SUPPORTED_LOCALES =
  process.env.NEXT_PUBLIC_SUPPORTED_LOCALES
    ? process.env.NEXT_PUBLIC_SUPPORTED_LOCALES.split(",")
    : [
        "ar",
        "en",
      ];



// Authentication

export const TOKEN_KEY =
  "accessToken";


export const REFRESH_TOKEN_KEY =
  "refreshToken";



// Routes

export const ROUTES = {

  LOGIN:
    "/login",

  DASHBOARD:
    "/",

  PROFILE:
    "/profile",

};