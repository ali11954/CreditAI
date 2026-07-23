export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      <div className="hidden w-1/2 bg-gradient-to-br from-primary to-primary/80 lg:flex lg:items-center lg:justify-center">
        <div className="max-w-md px-8 text-center text-white">
          <h1 className="mb-4 text-4xl font-bold">CreditAI Enterprise</h1>
          <p className="text-lg text-white/80">
            منصة إدارة الائتمان المدعومة بالذكاء الاصطناعي
          </p>
          <p className="mt-2 text-lg text-white/80">
            AI-Powered Credit Management Platform
          </p>
        </div>
      </div>
      <div className="flex w-full items-center justify-center bg-background px-4 lg:w-1/2">
        <div className="w-full max-w-md">{children}</div>
      </div>
    </div>
  );
}
