/**
 * @type {import('next').NextConfig}
 *
 * Next.js 구성 파일
 * - output: 정적 파일로 내보냅니다 (Vercel 배포 지원)
 * - distDir: 빌드 결과물 디렉토리를 dist로 설정합니다
 * - eslint와 typescript 검사는 빌드 속도를 위해 무시합니다
 */
const nextConfig = {
  reactStrictMode: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  output: "export",
  distDir: "dist",
};

export default nextConfig;
