/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://shera125-hacku2-phase2.hf.space/api/:path*',
      },
    ]
  },
};

module.exports = nextConfig;

