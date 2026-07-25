import { NextRequest, NextResponse } from 'next/server';

const BACKEND_API = process.env.BACKEND_API_URL
  || (process.env.RENDER
    ? 'https://creditai-backend-477s.onrender.com/api/v1'
    : 'http://127.0.0.1:8001/api/v1');

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

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 90000);

  const init: RequestInit = { method: request.method, headers, signal: controller.signal };
  if (!['GET', 'HEAD'].includes(request.method)) {
    init.body = await request.text();
  }

  try {
    const res = await fetch(targetUrl, init);
    clearTimeout(timeout);
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
