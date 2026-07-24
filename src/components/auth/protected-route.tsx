'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';

export default function ProtectedRoute({
  children,
}: {
  children: React.ReactNode;
}) {

  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !user) {
      router.replace('/login');
    }
  }, [user, isLoading, router]);


  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        جاري التحقق...
      </div>
    );
  }


  if (!user) {
    return null;
  }


  return children;
}