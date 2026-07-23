/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,

  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  images: {
    domains: [],
  },

  async rewrites() {
    return [];
  },
};

module.exports = nextConfig;