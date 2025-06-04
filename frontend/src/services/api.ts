// 환경 변수 설정 유틸리티
// 개발 및 프로덕션 환경에 따라 적절한 API 엔드포인트를 사용합니다.

import axios from "axios";

// 환경 변수에서 API 기본 URL 가져오기
const getApiBaseUrl = () => {
  // Next.js 환경 변수 사용
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }

  // 환경 변수가 없는 경우 배포 환경에서는 현재 호스트의 API를 사용
  if (process.env.NODE_ENV === "production") {
    // 브라우저 환경에서만 실행
    if (typeof window !== "undefined") {
      // 현재 호스트 기반 API URL 생성 (동일 도메인 가정)
      const protocol = window.location.protocol;
      const hostname = window.location.hostname;

      // 프로덕션 환경에서는 동일 도메인의 /api 경로 사용
      return `${protocol}//${hostname}/api`;
    }
  }

  // 개발 환경에서는 로컬 API 사용 (포트 5001로 변경)
  return "http://localhost:5001/api";
};

// API 기본 URL 내보내기
export const API_BASE_URL = getApiBaseUrl();

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: false, // CORS를 위해 false로 설정
  timeout: 10000, // 10초 타임아웃
});

// 요청 인터셉터 추가 (디버깅용)
apiClient.interceptors.request.use(
  (config) => {
    console.log(`🚀 API 요청: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error("❌ API 요청 오류:", error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터 추가 (디버깅용)
apiClient.interceptors.response.use(
  (response) => {
    console.log(`✅ API 응답: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error("❌ API 응답 오류:", error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// API 경로 유틸리티 함수
export const getApiUrl = (path: string) => {
  // 경로가 이미 슬래시로 시작하는 경우 중복 슬래시 방지
  const formattedPath = path.startsWith("/") ? path.substring(1) : path;
  return `${API_BASE_URL}/${formattedPath}`;
};

// 기본 API 클라이언트 내보내기
export default apiClient;
