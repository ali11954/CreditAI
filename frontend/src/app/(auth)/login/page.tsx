'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Eye, EyeOff, Lock, Mail, KeyRound } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { useAuth } from '@/hooks/use-auth';
import Link from 'next/link';

const loginSchema = z.object({
  email: z.string().email('البريد الإلكتروني غير صحيح'),
  password: z.string().min(6, 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'),
  rememberMe: z.boolean().default(false),
});

const mfaSchema = z.object({
  code: z.string().length(6, 'رمز التحقق يجب أن يكون 6 أرقام'),
});

type LoginForm = z.infer<typeof loginSchema>;
type MfaForm = z.infer<typeof mfaSchema>;

export default function LoginPage() {
  const router = useRouter();
  const { login, verifyMfa } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [isMfaRequired, setIsMfaRequired] = useState(false);
  const [pendingMfaToken, setPendingMfaToken] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const loginForm = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false,
    },
  });

  const mfaForm = useForm<MfaForm>({
    resolver: zodResolver(mfaSchema),
    defaultValues: {
      code: '',
    },
  });

  const onLoginSubmit = async (data: LoginForm) => {
    setIsLoading(true);
    setError('');
    try {
      const result = await login(data.email, data.password);
      if (result.mfaRequired) {
        setIsMfaRequired(true);
        setPendingMfaToken(result.pendingToken || '');
      } else {
        router.push('/');
      }
    } catch (err: any) {
      setError(err.message || 'فشل تسجيل الدخول');
    } finally {
      setIsLoading(false);
    }
  };

  const onMfaSubmit = async (data: MfaForm) => {
    setIsLoading(true);
    setError('');
    try {
      await verifyMfa(pendingMfaToken, data.code);
      router.push('/');
    } catch (err: any) {
      setError(err.message || 'رمز التحقق غير صحيح');
    } finally {
      setIsLoading(false);
    }
  };

  if (isMfaRequired) {
    return (
      <Card className="w-full">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
            <KeyRound className="h-6 w-6 text-primary" />
          </div>
          <CardTitle className="font-arabic text-2xl">التحقق بخطوتين</CardTitle>
          <CardDescription className="font-arabic">
            أدخل الرمز المُرسل إلى هاتفك
          </CardDescription>
        </CardHeader>
        <form onSubmit={mfaForm.handleSubmit(onMfaSubmit)}>
          <CardContent className="space-y-4">
            {error && (
              <div className="rounded-md bg-destructive/10 p-3 text-center text-sm text-destructive">
                {error}
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="code" className="font-arabic">رمز التحقق</Label>
              <Input
                id="code"
                type="text"
                inputMode="numeric"
                placeholder="000000"
                className="text-center text-2xl tracking-[0.5em]"
                maxLength={6}
                {...mfaForm.register('code')}
              />
              {mfaForm.formState.errors.code && (
                <p className="text-sm text-destructive">
                  {mfaForm.formState.errors.code.message}
                </p>
              )}
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <Button type="submit" className="w-full font-arabic" disabled={isLoading}>
              {isLoading ? 'جاري التحقق...' : 'تحقق'}
            </Button>
            <Button
              type="button"
              variant="ghost"
              className="font-arabic"
              onClick={() => {
                setIsMfaRequired(false);
                setPendingMfaToken('');
                setError('');
              }}
            >
              العودة لتسجيل الدخول
            </Button>
          </CardFooter>
        </form>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader className="text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">
          <Lock className="h-6 w-6 text-primary" />
        </div>
        <CardTitle className="font-arabic text-2xl">تسجيل الدخول</CardTitle>
        <CardDescription className="font-arabic">
          أدخل بيانات حسابك للمتابعة
        </CardDescription>
      </CardHeader>
      <form onSubmit={loginForm.handleSubmit(onLoginSubmit)}>
        <CardContent className="space-y-4">
          {error && (
            <div className="rounded-md bg-destructive/10 p-3 text-center text-sm text-destructive">
              {error}
            </div>
          )}
          <div className="space-y-2">
            <Label htmlFor="email" className="font-arabic">البريد الإلكتروني</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                id="email"
                type="email"
                placeholder="name@company.com"
                className="pl-10 font-arabic"
                dir="ltr"
                {...loginForm.register('email')}
              />
            </div>
            {loginForm.formState.errors.email && (
              <p className="text-sm text-destructive">
                {loginForm.formState.errors.email.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="password" className="font-arabic">كلمة المرور</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                className="pl-10 pr-10 font-arabic"
                {...loginForm.register('password')}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            {loginForm.formState.errors.password && (
              <p className="text-sm text-destructive">
                {loginForm.formState.errors.password.message}
              </p>
            )}
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 space-x-reverse">
              <Checkbox id="rememberMe" {...loginForm.register('rememberMe')} />
              <Label htmlFor="rememberMe" className="font-arabic text-sm">
                تذكرني
              </Label>
            </div>
            <Link
              href="/forgot-password"
              className="text-sm text-primary hover:underline font-arabic"
            >
              نسيت كلمة المرور؟
            </Link>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full font-arabic" disabled={isLoading}>
            {isLoading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
          </Button>
          <p className="text-center text-sm text-muted-foreground font-arabic">
            ليس لديك حساب؟{' '}
            <Link href="/register" className="text-primary hover:underline">
              طلب حساب جديد
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
