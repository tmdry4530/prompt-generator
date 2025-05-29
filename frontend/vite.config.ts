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
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
        secure: false,
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
