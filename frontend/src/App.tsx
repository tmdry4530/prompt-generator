import React, { useState, useEffect } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./components/ui/select";
import { Button } from "./components/ui/button";
import { Textarea } from "./components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Toaster } from "./components/ui/toaster";
import { useToast } from "./components/ui/use-toast";
import { Loader2 } from "lucide-react";
import "./App.css";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Copy,
  Check,
  Sparkles,
  Brain,
  Zap,
  Target,
  History,
  BarChart3,
} from "lucide-react";
import apiClient from "./services/api";

// API 기본 URL
const API_BASE = "http://localhost:5001/api";

// 모델 타입 정의
interface ModelInfo {
  max_tokens: number;
  strengths: string[];
  optimization_tips: string[];
  prompt_structure: string;
}

// 최적화 결과 타입 정의
interface OptimizationResult {
  original_task: string;
  model: string;
  optimized_prompt: string;
  optimization_tips: string[];
  model_strengths: string[];
  max_tokens: number;
  generated_at: string;
  prompt_structure: string;
}

interface HistoryItem {
  id: string;
  timestamp: string;
  model: string;
  task: string;
  optimizedPrompt: string;
}

interface ExampleTask {
  text: string;
  category: string;
}

function App() {
  // 상태 관리
  const [selectedModel, setSelectedModel] = useState<string>("gpt-4");
  const [userTask, setUserTask] = useState<string>("");
  const [optimizedResult, setOptimizedResult] =
    useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [copied, setCopied] = useState<boolean>(false);
  const [models, setModels] = useState<Record<string, ModelInfo>>({});
  const [examples, setExamples] = useState<string[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [stats, setStats] = useState<any>(null);
  const { toast } = useToast();

  // 컴포넌트 마운트 시 모델 목록 가져오기
  useEffect(() => {
    loadModels();
    loadHistory();
    loadStats();
  }, []);

  // 모델 변경시 예시 로드
  useEffect(() => {
    if (selectedModel) {
      loadExamples(selectedModel);
    }
  }, [selectedModel]);

  // API 함수들
  const loadModels = async () => {
    try {
      const response = await apiClient.get("/models");
      const data = await response.data;
      setModels(data.model_details || {});
    } catch (err) {
      console.error("모델 정보 로드 실패:", err);
    }
  };

  const loadExamples = async (model: string) => {
    try {
      const response = await apiClient.get(`/examples/${model}`);
      const data = await response.data;
      setExamples(data.examples || []);
    } catch (err) {
      console.error("예시 로드 실패:", err);
    }
  };

  const loadHistory = () => {
    const savedHistory = localStorage.getItem("promptHistory");
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  };

  const saveToHistory = (result: OptimizationResult) => {
    const newItem: HistoryItem = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      model: result.model,
      task: result.original_task,
      optimizedPrompt: result.optimized_prompt,
    };

    const updatedHistory = [newItem, ...history.slice(0, 49)]; // 최대 50개
    setHistory(updatedHistory);
    localStorage.setItem("promptHistory", JSON.stringify(updatedHistory));
  };

  const loadStats = async () => {
    try {
      const response = await apiClient.get("/stats");
      const data = await response.data;
      setStats(data);
    } catch (err) {
      console.error("통계 로드 실패:", err);
    }
  };

  // 프롬프트 최적화 실행
  const optimizePrompt = async () => {
    if (!userTask.trim()) {
      setError("작업 내용을 입력해주세요.");
      return;
    }

    setLoading(true);
    setError("");
    setOptimizedResult(null);

    try {
      const response = await apiClient.post("/optimize", {
        model: selectedModel,
        task: userTask.trim(),
      });

      const data = response.data;

      if (!response.data.success) {
        throw new Error(data.error || "최적화 실패");
      }

      if (data.success && data.data) {
        setOptimizedResult(data.data);
        saveToHistory(data.data);
        loadStats(); // 통계 업데이트
      } else {
        throw new Error("응답 형식 오류");
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "알 수 없는 오류가 발생했습니다."
      );
    } finally {
      setLoading(false);
    }
  };

  // 클립보드 복사
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("복사 실패:", err);
      toast("클립보드에 복사하지 못했습니다.", {
        variant: "destructive",
      });
    }
  };

  // 예시 선택
  const selectExample = (example: string) => {
    setUserTask(example);
  };

  // 기록에서 복원
  const restoreFromHistory = (item: HistoryItem) => {
    setSelectedModel(item.model);
    setUserTask(item.task);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* 헤더 */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-3">
            <Brain className="h-8 w-8 text-indigo-600" />
            <h1 className="text-4xl font-bold text-gray-900">
              Model Optimization Prompt Generator
            </h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            AI 모델별로 최적화된 프롬프트를 생성하여 더 나은 결과를 얻으세요
          </p>
        </div>

        <Tabs defaultValue="generate" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="generate" className="flex items-center gap-2">
              <Sparkles className="h-4 w-4" />
              프롬프트 생성
            </TabsTrigger>
            <TabsTrigger value="history" className="flex items-center gap-2">
              <History className="h-4 w-4" />
              생성 기록
            </TabsTrigger>
            <TabsTrigger value="stats" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              사용 통계
            </TabsTrigger>
          </TabsList>

          <TabsContent value="generate" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              {/* 입력 섹션 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5" />
                    프롬프트 설정
                  </CardTitle>
                  <CardDescription>
                    AI 모델과 작업을 선택하여 최적화된 프롬프트를 생성하세요
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* 모델 선택 */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium">AI 모델 선택</label>
                    <Select
                      value={selectedModel}
                      onValueChange={setSelectedModel}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="모델을 선택하세요" />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.entries(models).map(([modelName, info]) => (
                          <SelectItem key={modelName} value={modelName}>
                            <div className="flex items-center gap-2">
                              <span>{modelName}</span>
                              <Badge variant="secondary" className="text-xs">
                                {info.max_tokens.toLocaleString()} 토큰
                              </Badge>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* 모델 정보 표시 */}
                  {selectedModel && models[selectedModel] && (
                    <div className="p-4 bg-blue-50 rounded-lg space-y-3">
                      <div>
                        <h4 className="font-medium text-blue-900">모델 특성</h4>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {models[selectedModel].strengths.map(
                            (strength, idx) => (
                              <Badge
                                key={idx}
                                variant="outline"
                                className="text-blue-700"
                              >
                                {strength}
                              </Badge>
                            )
                          )}
                        </div>
                      </div>
                      <div>
                        <h4 className="font-medium text-blue-900">최적화 팁</h4>
                        <ul className="text-sm text-blue-800 mt-1 space-y-1">
                          {models[selectedModel].optimization_tips
                            .slice(0, 2)
                            .map((tip, idx) => (
                              <li key={idx} className="flex items-start gap-2">
                                <span className="text-blue-500 mt-1">•</span>
                                <span>{tip}</span>
                              </li>
                            ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* 작업 입력 */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium">작업 내용</label>
                    <Textarea
                      value={userTask}
                      onChange={(e) => setUserTask(e.target.value)}
                      placeholder="AI에게 요청할 작업을 자세히 설명해주세요..."
                      className="min-h-[120px] resize-none"
                    />
                  </div>

                  {/* 예시 작업들 */}
                  {examples.length > 0 && (
                    <div className="space-y-2">
                      <label className="text-sm font-medium">
                        예시 작업 ({selectedModel})
                      </label>
                      <div className="grid gap-2">
                        {examples.slice(0, 3).map((example, idx) => (
                          <button
                            key={idx}
                            onClick={() => selectExample(example)}
                            className="text-left p-3 text-sm bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                          >
                            {example}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 생성 버튼 */}
                  <Button
                    onClick={optimizePrompt}
                    disabled={loading || !userTask.trim()}
                    className="w-full"
                    size="lg"
                  >
                    {loading ? (
                      <div className="flex items-center gap-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                        최적화 중...
                      </div>
                    ) : (
                      <div className="flex items-center gap-2">
                        <Zap className="h-4 w-4" />
                        프롬프트 최적화
                      </div>
                    )}
                  </Button>
                </CardContent>
              </Card>

              {/* 결과 섹션 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5" />
                    최적화 결과
                  </CardTitle>
                  <CardDescription>
                    생성된 최적화 프롬프트를 확인하고 복사하세요
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {error && (
                    <Alert className="mb-4">
                      <AlertDescription className="text-red-600">
                        {error}
                      </AlertDescription>
                    </Alert>
                  )}

                  {optimizedResult ? (
                    <div className="space-y-4">
                      {/* 최적화된 프롬프트 */}
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <label className="text-sm font-medium">
                            최적화된 프롬프트
                          </label>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() =>
                              copyToClipboard(optimizedResult.optimized_prompt)
                            }
                            className="flex items-center gap-2"
                          >
                            {copied ? (
                              <Check className="h-4 w-4" />
                            ) : (
                              <Copy className="h-4 w-4" />
                            )}
                            {copied ? "복사됨" : "복사"}
                          </Button>
                        </div>
                        <div className="p-4 bg-gray-50 rounded-lg max-h-64 overflow-y-auto">
                          <pre className="whitespace-pre-wrap text-sm font-mono">
                            {optimizedResult.optimized_prompt}
                          </pre>
                        </div>
                      </div>

                      {/* 메타 정보 */}
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="font-medium">모델:</span>{" "}
                          {optimizedResult.model}
                        </div>
                        <div>
                          <span className="font-medium">구조:</span>{" "}
                          {optimizedResult.prompt_structure}
                        </div>
                        <div>
                          <span className="font-medium">생성 시간:</span>{" "}
                          {new Date(
                            optimizedResult.generated_at
                          ).toLocaleString("ko-KR")}
                        </div>
                        <div>
                          <span className="font-medium">토큰 한계:</span>{" "}
                          {optimizedResult.max_tokens.toLocaleString()}
                        </div>
                      </div>

                      {/* 최적화 팁 */}
                      <div className="space-y-2">
                        <h4 className="font-medium">적용된 최적화 기법</h4>
                        <ul className="space-y-1">
                          {optimizedResult.optimization_tips.map((tip, idx) => (
                            <li
                              key={idx}
                              className="flex items-start gap-2 text-sm"
                            >
                              <span className="text-green-500 mt-1">✓</span>
                              <span>{tip}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-12 text-gray-500">
                      <Brain className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p>
                        왼쪽에서 모델과 작업을 선택한 후<br />
                        프롬프트 최적화 버튼을 눌러주세요
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="history">
            <Card>
              <CardHeader>
                <CardTitle>생성 기록</CardTitle>
                <CardDescription>
                  최근 생성한 프롬프트들을 확인하고 다시 사용할 수 있습니다
                </CardDescription>
              </CardHeader>
              <CardContent>
                {history.length > 0 ? (
                  <div className="space-y-4">
                    {history.slice(0, 10).map((item) => (
                      <div
                        key={item.id}
                        className="p-4 border rounded-lg hover:bg-gray-50"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1 space-y-2">
                            <div className="flex items-center gap-2">
                              <Badge variant="outline">{item.model}</Badge>
                              <span className="text-sm text-gray-500">
                                {new Date(item.timestamp).toLocaleString(
                                  "ko-KR"
                                )}
                              </span>
                            </div>
                            <p className="font-medium">{item.task}</p>
                            <p className="text-sm text-gray-600 line-clamp-2">
                              {item.optimizedPrompt.substring(0, 150)}...
                            </p>
                          </div>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => restoreFromHistory(item)}
                          >
                            복원
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12 text-gray-500">
                    <History className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>아직 생성 기록이 없습니다</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="stats">
            <Card>
              <CardHeader>
                <CardTitle>사용 통계</CardTitle>
                <CardDescription>
                  프롬프트 생성기 사용 현황을 확인하세요
                </CardDescription>
              </CardHeader>
              <CardContent>
                {stats ? (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">
                          {stats.total_requests}
                        </div>
                        <div className="text-sm text-blue-800">총 요청 수</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600">
                          {Object.keys(stats.model_usage).length}
                        </div>
                        <div className="text-sm text-green-800">
                          사용된 모델
                        </div>
                      </div>
                      <div className="text-center p-4 bg-purple-50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">
                          {stats.recent_requests_count}
                        </div>
                        <div className="text-sm text-purple-800">최근 요청</div>
                      </div>
                    </div>

                    {stats.top_models && stats.top_models.length > 0 && (
                      <div>
                        <h4 className="font-medium mb-3">인기 모델</h4>
                        <div className="space-y-2">
                          {stats.top_models.map(
                            ([model, count]: [string, number]) => (
                              <div
                                key={model}
                                className="flex items-center justify-between p-2 bg-gray-50 rounded"
                              >
                                <span className="font-medium">{model}</span>
                                <Badge variant="secondary">{count}회</Badge>
                              </div>
                            )
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="text-center py-12 text-gray-500">
                    <BarChart3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>통계를 로드하는 중...</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

export default App;
