import { NextRequest, NextResponse } from 'next/server';

function getBackendApi(): string {
  const url = (
    process.env.BACKEND_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    'http://localhost:8000'
  ).replace(/\/+$/, '');
  return url.endsWith('/api/v1') ? url : `${url}/api/v1`;
}

async function proxyRequest(request: NextRequest, path: string[]) {
  const BACKEND_API = getBackendApi();
  const targetPath = path.join('/');
  const url = new URL(request.url);
  const targetUrl = `${BACKEND_API}/${targetPath}${url.search}`;

  const headers = new Headers();
  request.headers.forEach((value, key) => {
    const lower = key.toLowerCase();
    if (lower === 'host' || lower === 'origin' || lower === 'referer' || lower === 'x-forwarded-for' || lower === 'x-real-ip') {
      return;
    }
    headers.set(key, value);
  });
  headers.set('Accept', 'application/json');

  const init: RequestInit = {
    method: request.method,
    headers,
    redirect: 'follow',
  };

  if (!['GET', 'HEAD'].includes(request.method)) {
    const body = await request.arrayBuffer();
    init.body = body;
  }

  try {
    const response = await fetch(targetUrl, init);

    const responseHeaders = new Headers();
    response.headers.forEach((value, key) => {
      if (!['content-encoding', 'transfer-encoding'].includes(key.toLowerCase())) {
        responseHeaders.set(key, value);
      }
    });

    const responseBody = await response.arrayBuffer();
    return new NextResponse(responseBody, {
      status: response.status,
      statusText: response.statusText,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error(`Proxy error for /api/v1/${targetPath}:`, error);
    return NextResponse.json(
      { detail: 'Backend service unavailable' },
      { status: 502 }
    );
  }
}

export async function GET(request: NextRequest, { params }: { params: { path: string[] } }) {
  return proxyRequest(request, params.path);
}

export async function POST(request: NextRequest, { params }: { params: { path: string[] } }) {
  return proxyRequest(request, params.path);
}

export async function PUT(request: NextRequest, { params }: { params: { path: string[] } }) {
  return proxyRequest(request, params.path);
}

export async function PATCH(request: NextRequest, { params }: { params: { path: string[] } }) {
  return proxyRequest(request, params.path);
}

export async function DELETE(request: NextRequest, { params }: { params: { path: string[] } }) {
  return proxyRequest(request, params.path);
}
