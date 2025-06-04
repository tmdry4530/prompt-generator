"use client";

import React, { useState, useEffect } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { useToast } from "./ui/use-toast";
import { Loader2 } from "lucide-react";
import { Badge } from "./ui/badge";
import { Alert, AlertDescription } from "./ui/alert";
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
import axios from "axios";

// API 기본 URL
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5001/api";

// API 클라이언트 설정
const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

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

export default function PromptGenerator() {
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
      setModels(response.data.model_details || {});
    } catch (err) {
      console.error("모델 정보 로드 실패:", err);
    }
  };

  const loadExamples = async (model: string) => {
    try {
      const response = await apiClient.get(`/examples/${model}`);
      setExamples(response.data.examples || []);
    } catch (err) {
      console.error("예시 로드 실패:", err);
    }
  };

  const loadHistory = () => {
    if (typeof window !== "undefined") {
      const savedHistory = localStorage.getItem("promptHistory");
      if (savedHistory) {
        setHistory(JSON.parse(savedHistory));
      }
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

    if (typeof window !== "undefined") {
      localStorage.setItem("promptHistory", JSON.stringify(updatedHistory));
    }
  };

  const loadStats = async () => {
    try {
      const response = await apiClient.get("/stats");
      setStats(response.data);
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

      if (response.data.success && response.data.data) {
        setOptimizedResult(response.data.data);
        saveToHistory(response.data.data);
        loadStats(); // 통계 업데이트
      } else {
        throw new Error("응답 형식 오류");
      }
    } catch (err: any) {
      setError(err.message ? err.message : "알 수 없는 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // 클립보드 복사
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      toast({
        title: "복사 완료!",
        description: "프롬프트가 클립보드에 복사되었습니다.",
      });
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast({
        title: "복사 실패",
        description: "클립보드에 복사하지 못했습니다.",
        variant: "destructive",
      });
    }
  };

  // 예시 선택
  const selectExample = (example: string) => {
    setUserTask(example);
  };

  // 히스토리에서 복원
  const restoreFromHistory = (item: HistoryItem) => {
    setUserTask(item.task);
    setSelectedModel(item.model);
  };

  return (
    <div className="grid gap-6">
      <Tabs defaultValue="generator" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="generator">
            <Sparkles className="h-4 w-4 mr-2" />
            생성기
          </TabsTrigger>
          <TabsTrigger value="history">
            <History className="h-4 w-4 mr-2" />
            히스토리
          </TabsTrigger>
          <TabsTrigger value="statistics">
            <BarChart3 className="h-4 w-4 mr-2" />
            통계
          </TabsTrigger>
        </TabsList>

        {/* 생성기 탭 */}
        <TabsContent value="generator">
          <Card>
            <CardHeader>
              <CardTitle>프롬프트 최적화</CardTitle>
              <CardDescription>
                작업 내용을 입력하고 모델을 선택하면 최적화된 프롬프트를
                생성합니다.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* 모델 선택 */}
              <div className="space-y-2">
                <label className="text-sm font-medium">모델 선택</label>
                <Select value={selectedModel} onValueChange={setSelectedModel}>
                  <SelectTrigger>
                    <SelectValue placeholder="모델을 선택하세요" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.keys(models).map((model) => (
                      <SelectItem key={model} value={model}>
                        {model}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* 작업 내용 입력 */}
              <div className="space-y-2">
                <label className="text-sm font-medium">작업 내용</label>
                <Textarea
                  placeholder="원하는 작업을 자세히 설명해주세요..."
                  value={userTask}
                  onChange={(e) => setUserTask(e.target.value)}
                  rows={6}
                />
              </div>

              {/* 예시 목록 */}
              {examples.length > 0 && (
                <div className="space-y-2">
                  <label className="text-sm font-medium">예시 작업</label>
                  <div className="flex flex-wrap gap-2">
                    {examples.map((example, index) => (
                      <Badge
                        key={index}
                        variant="outline"
                        className="cursor-pointer hover:bg-accent"
                        onClick={() => selectExample(example)}
                      >
                        {example.length > 30
                          ? `${example.substring(0, 30)}...`
                          : example}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}

              {/* 모델 정보 */}
              {models[selectedModel] && (
                <div className="rounded-lg bg-muted p-3 text-sm">
                  <div className="flex items-center space-x-2 mb-2">
                    <Brain className="h-4 w-4" />
                    <span className="font-medium">모델 정보</span>
                  </div>
                  <div className="grid gap-2">
                    <div className="flex items-start">
                      <Zap className="h-4 w-4 mr-2 mt-1 flex-shrink-0" />
                      <div>
                        <span className="font-medium">강점: </span>
                        <span>
                          {models[selectedModel].strengths.join(", ")}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <Target className="h-4 w-4 mr-2 mt-1 flex-shrink-0" />
                      <div>
                        <span className="font-medium">최대 토큰: </span>
                        <span>{models[selectedModel].max_tokens}</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* 오류 메시지 */}
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
            </CardContent>
            <CardFooter>
              <Button
                onClick={optimizePrompt}
                disabled={loading || !userTask.trim()}
                className="w-full"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    처리 중...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    프롬프트 최적화하기
                  </>
                )}
              </Button>
            </CardFooter>
          </Card>

          {/* 최적화 결과 */}
          {optimizedResult && (
            <Card className="mt-6">
              <CardHeader>
                <CardTitle>최적화된 프롬프트</CardTitle>
                <CardDescription>
                  {optimizedResult.model}에 최적화된 프롬프트입니다.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative">
                  <Textarea
                    value={optimizedResult.optimized_prompt}
                    readOnly
                    rows={8}
                    className="pr-10"
                  />
                  <Button
                    size="sm"
                    variant="ghost"
                    className="absolute top-2 right-2"
                    onClick={() =>
                      copyToClipboard(optimizedResult.optimized_prompt)
                    }
                  >
                    {copied ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>

                <div className="space-y-3">
                  <h4 className="text-sm font-medium">최적화 팁</h4>
                  <ul className="space-y-1 text-sm">
                    {optimizedResult.optimization_tips.map((tip, index) => (
                      <li key={index} className="flex items-start">
                        <Sparkles className="h-4 w-4 mr-2 mt-1 flex-shrink-0" />
                        <span>{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h4 className="text-sm font-medium mb-2">
                    프롬프트 구조 가이드
                  </h4>
                  <div className="text-sm whitespace-pre-line rounded-lg bg-muted p-3">
                    {optimizedResult.prompt_structure}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* 히스토리 탭 */}
        <TabsContent value="history">
          <Card>
            <CardHeader>
              <CardTitle>프롬프트 히스토리</CardTitle>
              <CardDescription>
                이전에 생성한 최적화 프롬프트 기록입니다.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {history.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  아직 생성 기록이 없습니다.
                </div>
              ) : (
                <div className="space-y-4">
                  {history.map((item) => (
                    <Card
                      key={item.id}
                      className="cursor-pointer hover:bg-accent/5"
                      onClick={() => restoreFromHistory(item)}
                    >
                      <CardHeader className="py-3">
                        <div className="flex justify-between items-center">
                          <CardTitle className="text-base">
                            {item.model}
                          </CardTitle>
                          <CardDescription className="text-xs">
                            {new Date(item.timestamp).toLocaleString("ko-KR", {
                              year: "numeric",
                              month: "short",
                              day: "numeric",
                              hour: "2-digit",
                              minute: "2-digit",
                            })}
                          </CardDescription>
                        </div>
                      </CardHeader>
                      <CardContent className="py-2">
                        <div className="text-sm mb-2 font-medium line-clamp-2">
                          {item.task}
                        </div>
                        <div className="text-sm text-muted-foreground line-clamp-3">
                          {item.optimizedPrompt}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* 통계 탭 */}
        <TabsContent value="statistics">
          <Card>
            <CardHeader>
              <CardTitle>사용 통계</CardTitle>
              <CardDescription>
                프롬프트 최적화 서비스 사용 통계입니다.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!stats ? (
                <div className="text-center py-8 text-muted-foreground">
                  통계 정보를 불러오는 중...
                </div>
              ) : (
                <div className="grid gap-4 md:grid-cols-2">
                  <Card>
                    <CardHeader className="py-3">
                      <CardTitle className="text-base">
                        총 최적화 횟수
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="py-2">
                      <div className="text-3xl font-bold">
                        {stats.total_optimizations || 0}
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader className="py-3">
                      <CardTitle className="text-base">인기 모델</CardTitle>
                    </CardHeader>
                    <CardContent className="py-2">
                      <div className="text-xl font-bold">
                        {stats.popular_model || "-"}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {stats.popular_model_count || 0}회 사용
                      </div>
                    </CardContent>
                  </Card>
                  {/* 추가 통계 */}
                  {stats.recent_activity && (
                    <Card className="md:col-span-2">
                      <CardHeader className="py-3">
                        <CardTitle className="text-base">최근 활동</CardTitle>
                      </CardHeader>
                      <CardContent className="py-2">
                        <div className="text-sm">{stats.recent_activity}</div>
                      </CardContent>
                    </Card>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
