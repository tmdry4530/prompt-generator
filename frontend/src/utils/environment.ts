/**
 * 환경 변수 설정 유틸리티
 * 개발 및 프로덕션 환경에 따라 적절한 환경 변수를 로드합니다.
 */

// 필수 환경 변수 목록
const REQUIRED_ENV_VARS = [
  'VITE_API_BASE_URL'
];

// 환경 변수 유효성 검사
export function validateEnvironment(): { isValid: boolean; missingVars: string[] } {
  const missingVars: string[] = [];
  
  // 필수 환경 변수 확인
  for (const varName of REQUIRED_ENV_VARS) {
    if (!import.meta.env[varName]) {
      missingVars.push(varName);
    }
  }
  
  // 누락된 환경 변수가 있으면 경고 출력
  if (missingVars.length > 0) {
    console.warn(`경고: 다음 환경 변수가 설정되지 않았습니다: ${missingVars.join(', ')}`);
    return { isValid: false, missingVars };
  }
  
  return { isValid: true, missingVars };
}

// 환경 설정 초기화
export function initEnvironment(): { 
  isValid: boolean; 
  envInfo: { 
    mode: string; 
    isProd: boolean; 
    isDev: boolean; 
    apiBaseUrl: string; 
    appTitle: string; 
  } 
} {
  const { isValid } = validateEnvironment();
  
  // 환경 정보 반환
  return {
    isValid,
    envInfo: {
      mode: import.meta.env.MODE || 'development',
      isProd: import.meta.env.PROD,
      isDev: import.meta.env.DEV,
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
      appTitle: import.meta.env.VITE_APP_TITLE || 'AI 프롬프트 최적화 도구'
    }
  };
}
