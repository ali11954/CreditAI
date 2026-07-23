'use client';

import {
  createContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from 'react';

import { useRouter, usePathname } from 'next/navigation';
import { authService, User, AuthResponse } from '@/lib/auth';


interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<AuthResponse>;
  verifyMfa: (token: string, code: string) => Promise<AuthResponse>;
  logout: () => Promise<void>;
  updateUser: (user: Partial<User>) => void;
}


export const AuthContext = createContext<AuthContextType | null>(null);


export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {

  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const router = useRouter();
  const pathname = usePathname();


  useEffect(() => {

    const initAuth = async () => {

      try {

        const token = authService.getToken();


        if (token) {

          const profile = await authService.getProfile();

          setUser(profile);

        } else {

          setUser(null);

        }


      } catch (error) {

        console.error("Auth check failed:", error);

        authService.clearTokens();

        setUser(null);

      }
      finally {

        setIsLoading(false);

      }

    };


    initAuth();

  }, []);



  useEffect(() => {

    if (
      !isLoading &&
      !user &&
      pathname !== '/login' &&
      pathname !== '/register' &&
      pathname !== '/forgot-password'
    ) {

      router.replace('/login');

    }

  }, [
    user,
    isLoading,
    pathname,
    router
  ]);




  const login = useCallback(
    async (
      email: string,
      password: string
    ) => {


      const response =
        await authService.login(
          email,
          password
        );


      if (response.access_token) {


        authService.setTokens(
          response.access_token,
          response.refresh_token
        );


        try {


          const profile =
            await authService.getProfile();


          setUser(profile);


        } catch {


          authService.clearTokens();

          setUser(null);

        }

      }


      return response;


    },
    []
  );




  const verifyMfa = useCallback(
    async (
      token:string,
      code:string
    ) => {


      const response =
        await authService.verifyMfa(
          token,
          code
        );


      authService.setTokens(
        response.access_token,
        response.refresh_token
      );


      if(response.user){

        setUser(response.user);

      }


      return response;


    },
    []
  );




  const logout = useCallback(
    async () => {


      try {

        await authService.logout();

      }
      finally {


        authService.clearTokens();

        setUser(null);

        router.replace('/login');


      }


    },
    [router]
  );




  const updateUser = useCallback(
    (
      updates: Partial<User>
    ) => {


      setUser(
        previous =>
          previous
          ? {
              ...previous,
              ...updates
            }
          : null
      );


    },
    []
  );



  if(isLoading){

    return (
      <div className="flex min-h-screen items-center justify-center">

        جاري التحقق من الجلسة...

      </div>
    );

  }



  return (

    <AuthContext.Provider
      value={{

        user,

        isAuthenticated: Boolean(user),

        isLoading,

        login,

        verifyMfa,

        logout,

        updateUser,

      }}
    >

      {children}

    </AuthContext.Provider>

  );

}