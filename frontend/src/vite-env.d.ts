// 환경 변수 타입 선언 파일
// Vite의 import.meta.env 타입을 확장합니다.

/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_APP_TITLE: string;
  // 추가 환경 변수가 있다면 여기에 선언하세요
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
