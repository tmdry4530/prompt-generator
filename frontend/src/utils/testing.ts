// 테스트 유틸리티: 통합 테스트 및 품질 검증을 위한 유틸리티
import apiService from '../services/api';
import { logError } from './errorHandling';

// 테스트 상태 타입 정의
export interface TestResult {
  name: string;
  success: boolean;
  message: string;
  duration: number;
}

// 테스트 실행 함수
export const runTest = async (
  name: string,
  testFn: () => Promise<void>
): Promise<TestResult> => {
  const startTime = performance.now();
  let success = false;
  let message = '';
  
  try {
    await testFn();
    success = true;
    message = '테스트 성공';
  } catch (error) {
    success = false;
    message = error instanceof Error ? error.message : '알 수 없는 오류';
    logError(error, `테스트: ${name}`);
  }
  
  const endTime = performance.now();
  const duration = endTime - startTime;
  
  return {
    name,
    success,
    message,
    duration
  };
};

// API 연결 테스트
export const testApiConnection = async (): Promise<TestResult> => {
  return runTest('API 연결 테스트', async () => {
    const isHealthy = await apiService.checkHealth();
    if (!isHealthy) {
      throw new Error('API 서버에 연결할 수 없습니다.');
    }
  });
};

// 모델 목록 가져오기 테스트
export const testGetModels = async (): Promise<TestResult> => {
  return runTest('모델 목록 가져오기 테스트', async () => {
    const models = await apiService.getModels();
    if (!models || models.length === 0) {
      throw new Error('모델 목록을 가져오는 데 실패했습니다.');
    }
  });
};

// 프롬프트 최적화 테스트
export const testOptimizePrompt = async (
  inputText: string,
  modelId: string
): Promise<TestResult> => {
  return runTest('프롬프트 최적화 테스트', async () => {
    const result = await apiService.optimizePrompt(inputText, modelId);
    if (!result.success) {
      throw new Error(result.error || '프롬프트 최적화에 실패했습니다.');
    }
    
    // 결과 검증
    if (!result.optimized_prompt || result.optimized_prompt.trim().length === 0) {
      throw new Error('최적화된 프롬프트가 비어 있습니다.');
    }
  });
};

// 모델 팁 가져오기 테스트
export const testGetModelTips = async (modelId: string): Promise<TestResult> => {
  return runTest('모델 팁 가져오기 테스트', async () => {
    const tips = await apiService.getModelTips(modelId);
    if (!tips || tips.length === 0) {
      throw new Error('모델 팁을 가져오는 데 실패했습니다.');
    }
  });
};

// 모델 구조 가져오기 테스트
export const testGetModelStructure = async (modelId: string): Promise<TestResult> => {
  return runTest('모델 구조 가져오기 테스트', async () => {
    const structure = await apiService.getModelStructure(modelId);
    if (!structure || Object.keys(structure).length === 0) {
      throw new Error('모델 구조를 가져오는 데 실패했습니다.');
    }
  });
};

// 모델 정보 가져오기 테스트
export const testGetModelInfo = async (modelId: string): Promise<TestResult> => {
  return runTest('모델 정보 가져오기 테스트', async () => {
    const info = await apiService.getModelInfo(modelId);
    if (!info || Object.keys(info).length === 0) {
      throw new Error('모델 정보를 가져오는 데 실패했습니다.');
    }
  });
};

// 모델 비교 테스트
export const testCompareModels = async (modelIds: string[]): Promise<TestResult> => {
  return runTest('모델 비교 테스트', async () => {
    const comparison = await apiService.compareModels(modelIds);
    if (!comparison || Object.keys(comparison).length === 0) {
      throw new Error('모델 비교에 실패했습니다.');
    }
  });
};

// 저장 기능 테스트
export const testSavePrompt = async (): Promise<TestResult> => {
  return runTest('프롬프트 저장 테스트', async () => {
    const testPrompt = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      modelId: 'test-model',
      modelName: 'Test Model',
      originalInput: 'Test input',
      optimizedPrompt: 'Test optimized prompt'
    };
    
    const success = apiService.savePrompt(testPrompt);
    if (!success) {
      throw new Error('프롬프트 저장에 실패했습니다.');
    }
    
    const savedPrompts = apiService.getSavedPrompts();
    const found = savedPrompts.some(p => p.id === testPrompt.id);
    if (!found) {
      throw new Error('저장된 프롬프트를 찾을 수 없습니다.');
    }
    
    // 테스트 후 정리
    apiService.deleteSavedPrompt(testPrompt.id);
  });
};

// 전체 테스트 실행
export const runAllTests = async (
  inputText: string = '산 위에서 일출을 바라보는 사람의 실루엣',
  modelId: string = 'gpt-4o'
): Promise<TestResult[]> => {
  const results: TestResult[] = [];
  
  // API 연결 테스트
  results.push(await testApiConnection());
  
  // 모델 목록 가져오기 테스트
  const modelsResult = await testGetModels();
  results.push(modelsResult);
  
  // 모델 목록 테스트가 성공한 경우에만 다음 테스트 진행
  if (modelsResult.success) {
    // 프롬프트 최적화 테스트
    results.push(await testOptimizePrompt(inputText, modelId));
    
    // 모델 팁 가져오기 테스트
    results.push(await testGetModelTips(modelId));
    
    // 모델 구조 가져오기 테스트
    results.push(await testGetModelStructure(modelId));
    
    // 모델 정보 가져오기 테스트
    results.push(await testGetModelInfo(modelId));
    
    // 모델 비교 테스트 (최소 2개 모델 필요)
    const models = await apiService.getModels();
    if (models.length >= 2) {
      const modelIds = models.slice(0, 2).map(m => m.model_id);
      results.push(await testCompareModels(modelIds));
    }
  }
  
  // 저장 기능 테스트
  results.push(await testSavePrompt());
  
  return results;
};

// 테스트 결과 요약
export const summarizeTestResults = (results: TestResult[]): {
  total: number;
  passed: number;
  failed: number;
  passRate: number;
  failedTests: string[];
} => {
  const total = results.length;
  const passed = results.filter(r => r.success).length;
  const failed = total - passed;
  const passRate = (passed / total) * 100;
  const failedTests = results
    .filter(r => !r.success)
    .map(r => `${r.name}: ${r.message}`);
  
  return {
    total,
    passed,
    failed,
    passRate,
    failedTests
  };
};
