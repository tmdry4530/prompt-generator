import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from './components/ui/select';
import { Button } from './components/ui/button';
import { Textarea } from './components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Toaster } from './components/ui/toaster';
import { useToast } from './components/ui/use-toast';
import { Loader2 } from 'lucide-react';
import './App.css';

// API 기본 URL
const API_BASE_URL = 'http://localhost:5000/api';

// 모델 타입 정의
interface Model {
  model_id: string;
  model_name: string;
  provider: string;
  capabilities: string[];
  supports_multimodal: boolean;
}

// 최적화 결과 타입 정의
interface OptimizationResult {
  success: boolean;
  original_input: string;
  optimized_prompt: string;
  model_id: string;
  model_info: any;
  prompt_structure: any;
  generation_params: any;
  analysis_result: any;
  intent_result: any;
  error?: string;
}

function App() {
  // 상태 관리
  const [models, setModels] = useState<Model[]>([]);
  const [selectedModelId, setSelectedModelId] = useState<string>('');
  const [inputText, setInputText] = useState<string>('');
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [modelTips, setModelTips] = useState<string[]>([]);
  const { toast } = useToast();

  // 컴포넌트 마운트 시 모델 목록 가져오기
  useEffect(() => {
    fetchModels();
  }, []);

  // 모델 선택 시 해당 모델의 팁 가져오기
  useEffect(() => {
    if (selectedModelId) {
      fetchModelTips(selectedModelId);
    }
  }, [selectedModelId]);

  // 모델 목록 가져오기
  const fetchModels = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/models`);
      if (response.data.success) {
        setModels(response.data.models);
        // 첫 번째 모델을 기본 선택
        if (response.data.models.length > 0) {
          setSelectedModelId(response.data.models[0].model_id);
        }
      } else {
        toast('모델 목록을 가져오는 데 실패했습니다.', {
          variant: 'destructive',
        });
      }
    } catch (error) {
      console.error('모델 목록 가져오기 오류:', error);
      toast('서버 연결에 실패했습니다.', {
        variant: 'destructive',
      });
    }
  };

  // 모델 팁 가져오기
  const fetchModelTips = async (modelId: string) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/model/${modelId}/tips`);
      if (response.data.success) {
        setModelTips(response.data.tips);
      }
    } catch (error) {
      console.error('모델 팁 가져오기 오류:', error);
    }
  };

  // 프롬프트 최적화 요청
  const optimizePrompt = async () => {
    if (!inputText.trim()) {
      toast('최적화할 텍스트를 입력해주세요.', {
        variant: 'destructive',
      });
      return;
    }

    if (!selectedModelId) {
      toast('AI 모델을 선택해주세요.', {
        variant: 'destructive',
      });
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/optimize`, {
        input_text: inputText,
        model_id: selectedModelId,
      });

      setOptimizationResult(response.data);
      
      if (response.data.success) {
        toast('프롬프트가 성공적으로 최적화되었습니다.');
      } else {
        toast(response.data.error || '알 수 없는 오류가 발생했습니다.', {
          variant: 'destructive',
        });
      }
    } catch (error) {
      console.error('프롬프트 최적화 오류:', error);
      toast('서버 연결에 실패했습니다.', {
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  // 결과 복사하기
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(
      () => {
        toast('클립보드에 복사되었습니다.');
      },
      (err) => {
        console.error('클립보드 복사 실패:', err);
        toast('클립보드에 복사하지 못했습니다.', {
          variant: 'destructive',
        });
      }
    );
  };

  // 결과 저장하기 (로컬 스토리지)
  const saveResult = () => {
    if (!optimizationResult) return;
    
    try {
      const savedResults = JSON.parse(localStorage.getItem('savedPrompts') || '[]');
      const newResult = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        modelId: optimizationResult.model_id,
        modelName: models.find(m => m.model_id === optimizationResult.model_id)?.model_name || '',
        originalInput: optimizationResult.original_input,
        optimizedPrompt: optimizationResult.optimized_prompt,
      };
      
      savedResults.push(newResult);
      localStorage.setItem('savedPrompts', JSON.stringify(savedResults));
      
      toast('프롬프트가 저장되었습니다.');
    } catch (error) {
      console.error('저장 오류:', error);
      toast('프롬프트를 저장하지 못했습니다.', {
        variant: 'destructive',
      });
    }
  };

  // 모델 제공업체별 그룹화
  const groupedModels = models.reduce((acc, model) => {
    if (!acc[model.provider]) {
      acc[model.provider] = [];
    }
    acc[model.provider].push(model);
    return acc;
  }, {} as Record<string, Model[]>);

  return (
    <div className="container mx-auto py-8 px-4">
      <Toaster />
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-2">AI 프롬프트 최적화 도구</h1>
        <p className="text-gray-600">
          다양한 AI 모델에 최적화된 고품질 프롬프트를 생성하세요
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>AI 모델 선택</CardTitle>
              <CardDescription>
                프롬프트를 최적화할 AI 모델을 선택하세요
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Select value={selectedModelId} onValueChange={setSelectedModelId}>
                <SelectTrigger>
                  <SelectValue placeholder="AI 모델 선택" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(groupedModels).map(([provider, providerModels]) => (
                    <React.Fragment key={provider}>
                      <div className="px-2 py-1.5 text-sm font-semibold">{provider}</div>
                      {providerModels.map((model) => (
                        <SelectItem key={model.model_id} value={model.model_id}>
                          {model.model_name}
                        </SelectItem>
                      ))}
                    </React.Fragment>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
            <CardFooter className="flex-col items-start">
              <h4 className="text-sm font-semibold mb-2">모델 최적화 팁:</h4>
              <ul className="text-sm text-gray-600 list-disc pl-5 space-y-1">
                {modelTips.map((tip, index) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </CardFooter>
          </Card>
        </div>

        <div className="md:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>프롬프트 최적화</CardTitle>
              <CardDescription>
                기본 요청을 입력하면 선택한 AI 모델에 최적화된 프롬프트로 변환됩니다
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label htmlFor="input-text" className="block text-sm font-medium mb-1">
                    기본 요청 입력
                  </label>
                  <Textarea
                    id="input-text"
                    placeholder="여기에 기본 요청을 입력하세요. 예: '산 위에서 일출을 바라보는 사람의 실루엣'"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    rows={5}
                  />
                </div>

                <Button 
                  onClick={optimizePrompt} 
                  className="w-full" 
                  disabled={loading || !inputText.trim() || !selectedModelId}
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      최적화 중...
                    </>
                  ) : (
                    '프롬프트 최적화'
                  )}
                </Button>

                {optimizationResult && optimizationResult.success && (
                  <div className="mt-6">
                    <Tabs defaultValue="result">
                      <TabsList className="grid w-full grid-cols-3">
                        <TabsTrigger value="result">최적화 결과</TabsTrigger>
                        <TabsTrigger value="analysis">분석 정보</TabsTrigger>
                        <TabsTrigger value="params">생성 매개변수</TabsTrigger>
                      </TabsList>
                      
                      <TabsContent value="result" className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium mb-1">
                            최적화된 프롬프트
                          </label>
                          <div className="relative">
                            <Textarea
                              value={optimizationResult.optimized_prompt}
                              readOnly
                              rows={8}
                              className="pr-12"
                            />
                            <Button
                              variant="ghost"
                              size="sm"
                              className="absolute top-2 right-2"
                              onClick={() => copyToClipboard(optimizationResult.optimized_prompt)}
                            >
                              복사
                            </Button>
                          </div>
                        </div>
                        <div className="flex justify-end">
                          <Button variant="outline" onClick={saveResult}>
                            결과 저장
                          </Button>
                        </div>
                      </TabsContent>
                      
                      <TabsContent value="analysis">
                        <div className="space-y-4">
                          <div>
                            <h3 className="text-sm font-medium mb-1">키워드 분석</h3>
                            <div className="bg-gray-50 p-3 rounded-md text-sm">
                              {optimizationResult.analysis_result.keywords?.map((keyword: string, i: number) => (
                                <span key={i} className="inline-block bg-blue-100 text-blue-800 rounded-full px-2 py-1 text-xs mr-2 mb-2">
                                  {keyword}
                                </span>
                              )) || '키워드 분석 정보가 없습니다.'}
                            </div>
                          </div>
                          
                          <div>
                            <h3 className="text-sm font-medium mb-1">의도 분석</h3>
                            <div className="bg-gray-50 p-3 rounded-md text-sm">
                              {optimizationResult.intent_result.primary_intent || '의도 분석 정보가 없습니다.'}
                            </div>
                          </div>
                          
                          <div>
                            <h3 className="text-sm font-medium mb-1">프롬프트 구조</h3>
                            <div className="bg-gray-50 p-3 rounded-md text-sm">
                              {optimizationResult.prompt_structure.components?.map((component: string, i: number) => (
                                <div key={i} className="mb-1">
                                  • {component}
                                </div>
                              )) || '프롬프트 구조 정보가 없습니다.'}
                            </div>
                          </div>
                        </div>
                      </TabsContent>
                      
                      <TabsContent value="params">
                        <div className="space-y-4">
                          <div>
                            <h3 className="text-sm font-medium mb-1">생성 매개변수</h3>
                            <div className="bg-gray-50 p-3 rounded-md text-sm">
                              {Object.keys(optimizationResult.generation_params || {}).length > 0 ? (
                                <pre className="whitespace-pre-wrap">
                                  {JSON.stringify(optimizationResult.generation_params, null, 2)}
                                </pre>
                              ) : (
                                '생성 매개변수 정보가 없습니다.'
                              )}
                            </div>
                          </div>
                          
                          <div>
                            <h3 className="text-sm font-medium mb-1">모델 정보</h3>
                            <div className="bg-gray-50 p-3 rounded-md text-sm">
                              <div><strong>모델:</strong> {optimizationResult.model_info.model_name}</div>
                              <div><strong>제공업체:</strong> {optimizationResult.model_info.provider}</div>
                              <div><strong>기능:</strong> {optimizationResult.model_info.capabilities.join(', ')}</div>
                            </div>
                          </div>
                        </div>
                      </TabsContent>
                    </Tabs>
                  </div>
                )}
                
                {optimizationResult && !optimizationResult.success && (
                  <div className="mt-6 p-4 bg-red-50 text-red-800 rounded-md">
                    <h3 className="font-medium">오류 발생</h3>
                    <p>{optimizationResult.error || '알 수 없는 오류가 발생했습니다.'}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default App;
