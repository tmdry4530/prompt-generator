/**
 * 테스트 환경 설정 파일
 * Vitest와 React Testing Library 초기화를 담당합니다.
 */

import "@testing-library/jest-dom";
import "vitest-canvas-mock";

// CSS 파일 모킹
vi.mock("*.css", () => ({}));

// MSW (Mock Service Worker) 설정
import { beforeAll, afterEach, afterAll, vi } from "vitest";
import { server } from "./mocks/server";

// API 모킹 서버 설정
beforeAll(() => {
  // 테스트 시작 전 서버 시작
  server.listen({ onUnhandledRequest: "error" });
});

afterEach(() => {
  // 각 테스트 후 핸들러 리셋
  server.resetHandlers();
});

afterAll(() => {
  // 모든 테스트 완료 후 서버 종료
  server.close();
});

// 전역 테스트 설정
Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {},
    removeListener: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
});

// ResizeObserver 모킹 (차트 컴포넌트 등에서 사용)
global.ResizeObserver = class ResizeObserver {
  constructor(callback: ResizeObserverCallback) {
    this.callback = callback;
  }
  callback: ResizeObserverCallback;
  observe() {}
  unobserve() {}
  disconnect() {}
};

// IntersectionObserver 모킹
global.IntersectionObserver = class IntersectionObserver {
  constructor(callback: IntersectionObserverCallback) {
    this.callback = callback;
  }
  callback: IntersectionObserverCallback;
  observe() {}
  unobserve() {}
  disconnect() {}
};

// localStorage 모킹
const localStorageMock = {
  getItem: (_: string) => null,
  setItem: (_: string, __: string) => {},
  removeItem: (_: string) => {},
  clear: () => {},
};
Object.defineProperty(window, "localStorage", {
  value: localStorageMock,
});

// sessionStorage 모킹
Object.defineProperty(window, "sessionStorage", {
  value: localStorageMock,
});

// fetch 모킹을 위한 전역 설정
globalThis.fetch = fetch;
