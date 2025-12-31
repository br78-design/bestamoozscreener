/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      // هر چیزی که از فرانت با /api شروع شد، به سرویس backend داخل شبکه docker پاس بده
      {
        source: "/api/:path*",
        destination: "http://backend:8000/api/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
