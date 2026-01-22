import type { NextConfig } from "next";

const nextConfig: NextConfig = {

  transpilePackages: ["@saas/ui"],
  experimental: {
    optimizePackageImports: ["lucide-react", "@saas/ui"],
  },
};

export default nextConfig;
