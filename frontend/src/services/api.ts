// 환경 변수 설정 유틸리티
// 개발 및 프로덕션 환경에 따라 적절한 API 엔드포인트를 사용합니다.

// 환경 변수에서 API 기본 URL 가져오기
const getApiBaseUrl = () => {
  // Vite 환경 변수 사용
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  
  // 환경 변수가 없는 경우 배포 환경에서는 현재 호스트의 API를 사용
  if (import.meta.env.PROD) {
    // 현재 호스트 기반 API URL 생성 (동일 도메인 가정)
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    
    // 프로덕션 환경에서는 동일 도메인의 /api 경로 사용
    return `${protocol}//${hostname}/api`;
  }
  
  // 개발 환경에서는 로컬 API 사용
  return 'http://localhost:5000/api';
};

// API 기본 URL 내보내기
export const API_BASE_URL = getApiBaseUrl();

// API 경로 유틸리티 함수
export const getApiUrl = (path: string) => {
  // 경로가 이미 슬래시로 시작하는 경우 중복 슬래시 방지
  const formattedPath = path.startsWith('/') ? path.substring(1) : path;
  return `${API_BASE_URL}/${formattedPath}`;
};
