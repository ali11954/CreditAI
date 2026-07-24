import { NextRequest, NextResponse } from 'next/server';

const BACKEND_API = 'https://creditai-backend-477s.onrender.com/api/v1';

async function proxy(request: NextRequest, path: string[]) {
  const targetPath = path.join('/');
  const url = new URL(request.url);
  const targetUrl = `${BACKEND_API}/${targetPath}${url.search}`;

  const headers: Record<string, string> = {};
  const ct = request.headers.get('content-type');
  if (ct) headers['Content-Type'] = ct;
  headers['Accept'] = 'application/json';
  const auth = request.headers.get('authorization');
  if (auth) headers['Authorization'] = auth;

  const init: RequestInit = { method: request.method, headers };
  if (!['GET', 'HEAD'].includes(request.method)) {
    init.body = await request.text();
  }

  try {
    const res = await fetch(targetUrl, init);
    const body = await res.text();
    return new NextResponse(body, {
      status: res.status,
      headers: { 'Content-Type': res.headers.get('content-type') || 'application/json' },
    });
  } catch {
    return NextResponse.json({ detail: 'Backend unavailable' }, { status: 502 });
  }
}

export const GET = (req: NextRequest, { params }: { params: { path: string[] } }) => proxy(req, params.path);
export const POST = (req: NextRequest, { params }: { params: { path: string[] } }) => proxy(req, params.path);
export const PUT = (req: NextRequest, { params }: { params: { path: string[] } }) => proxy(req, params.path);
export const PATCH = (req: NextRequest, { params }: { params: { path: string[] } }) => proxy(req, params.path);
export const DELETE = (req: NextRequest, { params }: { params: { path: string[] } }) => proxy(req, params.path);
