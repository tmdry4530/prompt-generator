/// <reference types="vitest" />
import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig, UserConfig } from "vite";
import type { InlineConfig } from "vitest";

// 타입 정의 추가
interface ViteConfigWithTest extends UserConfig {
  test?: InlineConfig;
}

// Vite 기본 설정
const viteConfig: UserConfig = {
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: "0.0.0.0", // 모든 인터페이스에서 접근 가능하도록 설정
    port: 5173, // 프론트엔드 기본 포트
    strictPort: true, // 포트가 사용 중이면 실패
    open: false, // 자동으로 브라우저 열지 않음
    cors: true, // CORS 활성화
    proxy: {
      "/api": {
        target: "http://localhost:5001", // 백엔드 포트를 5001로 변경
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path, // /api 경로 유지
        configure: (proxy, options) => {
          proxy.on("error", (err, req, res) => {
            console.error("프록시 오류:", err);
          });
          proxy.on("proxyReq", (proxyReq, req, res) => {
            console.log("프록시 요청:", req.method, req.url);
          });
        },
      },
      // WebSocket 프록시 (향후 실시간 기능용)
      "/ws": {
        target: "ws://localhost:5001",
        ws: true,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "dist",
    assetsDir: "assets",
    sourcemap: true,
    minify: "terser",
    terserOptions: {
      compress: {
        drop_console: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          react: ["react", "react-dom"],
          ui: [
            "@radix-ui/react-tabs",
            "@radix-ui/react-dialog",
            "@radix-ui/react-dropdown-menu",
          ],
        },
      },
    },
  },
};

// Vitest 설정
const vitestConfig: InlineConfig = {
  globals: true,
  environment: "happy-dom",
  setupFiles: ["./test/setup.ts"],
  css: false, // CSS 파일 처리 비활성화
  deps: {
    inline: ["axios"],
  },
  coverage: {
    provider: "v8",
    reporter: ["text", "html", "lcov"],
    exclude: [
      "node_modules/",
      "test/",
      "dist/",
      "**/*.d.ts",
      "**/*.config.*",
      "**/coverage/**",
    ],
    thresholds: {
      global: {
        branches: 70,
        functions: 70,
        lines: 70,
        statements: 70,
      },
    },
  },
};

// 전체 설정 내보내기
export default defineConfig({
  ...viteConfig,
  test: vitestConfig,
} as ViteConfigWithTest);
