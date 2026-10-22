/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow images from external sources (if needed later)
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },
};

export default nextConfig;
