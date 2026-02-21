import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactCompiler: true,
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  async rewrites() {
    return [
      {
        source: '/api-engine/:path*',
        destination: 'http://localhost:8000/:path*', // Mudará para o IP da VPS no futuro
      },
    ];
  },
};

export default nextConfig;
