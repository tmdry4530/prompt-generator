// 오류 처리 및 예외 관리 유틸리티
import { AxiosError } from 'axios';

// 오류 타입 정의
export interface ErrorResponse {
  success: boolean;
  error: string;
}

// 오류 메시지 생성 함수
export const getErrorMessage = (error: unknown): string => {
  if (error instanceof AxiosError) {
    // Axios 오류 처리
    if (error.response) {
      // 서버에서 응답이 왔지만 오류 상태 코드인 경우
      const data = error.response.data as ErrorResponse;
      if (data && data.error) {
        return data.error;
      }
      return `서버 오류 (${error.response.status}): ${error.response.statusText}`;
    } else if (error.request) {
      // 요청은 보냈지만 응답이 없는 경우
      return '서버에 연결할 수 없습니다. 네트워크 연결을 확인하세요.';
    } else {
      // 요청 설정 중 오류가 발생한 경우
      return `요청 오류: ${error.message}`;
    }
  } else if (error instanceof Error) {
    // 일반 Error 객체인 경우
    return error.message;
  } else if (typeof error === 'string') {
    // 문자열인 경우
    return error;
  } else {
    // 기타 알 수 없는 오류
    return '알 수 없는 오류가 발생했습니다.';
  }
};

// 입력 유효성 검사 함수
export const validateInput = (input: string): boolean => {
  return input.trim().length > 0;
};

// 모델 ID 유효성 검사 함수
export const validateModelId = (modelId: string): boolean => {
  return modelId.trim().length > 0;
};

// 추가 매개변수 유효성 검사 함수
export const validateAdditionalParams = (params: any): boolean => {
  if (!params) return true;
  if (typeof params !== 'object') return false;
  
  // 특정 매개변수 유효성 검사 로직 추가 가능
  return true;
};

// 오류 로깅 함수
export const logError = (error: unknown, context?: string): void => {
  const timestamp = new Date().toISOString();
  const errorMessage = getErrorMessage(error);
  const contextInfo = context ? ` [${context}]` : '';
  
  console.error(`[${timestamp}]${contextInfo} 오류: ${errorMessage}`);
  
  // 실제 프로덕션 환경에서는 원격 로깅 서비스로 전송 가능
};

// 네트워크 상태 확인 함수
export const checkNetworkStatus = (): boolean => {
  return navigator.onLine;
};

// 재시도 로직 함수
export const retry = async <T>(
  fn: () => Promise<T>,
  retries: number = 3,
  delay: number = 1000
): Promise<T> => {
  try {
    return await fn();
  } catch (error) {
    if (retries <= 0) {
      throw error;
    }
    
    await new Promise(resolve => setTimeout(resolve, delay));
    return retry(fn, retries - 1, delay * 2);
  }
};

// 타임아웃 함수
export const withTimeout = <T>(
  promise: Promise<T>,
  timeoutMs: number = 10000
): Promise<T> => {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) => {
      setTimeout(() => {
        reject(new Error(`요청 시간이 초과되었습니다 (${timeoutMs}ms).`));
      }, timeoutMs);
    })
  ]);
};
