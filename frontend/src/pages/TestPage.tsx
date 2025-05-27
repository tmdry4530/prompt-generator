import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Loader2 } from 'lucide-react';
import { runAllTests, summarizeTestResults, TestResult } from '../utils/testing';
import { useToast } from '../components/ui/use-toast';
import React, { useState } from 'react';

const TestPage: React.FC = () => {
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const { toast } = useToast();

  const handleRunTests = async () => {
    setIsRunning(true);
    setTestResults([]);
    setSummary(null);

    try {
      const results = await runAllTests();
      setTestResults(results);
      const resultSummary = summarizeTestResults(results);
      setSummary(resultSummary);

      if (resultSummary.failed === 0) {
        toast('모든 테스트가 성공적으로 완료되었습니다.');
      } else {
        toast(`${resultSummary.failed}개의 테스트가 실패했습니다.`, {
          variant: 'destructive',
        });
      }
    } catch (error) {
      toast('테스트 실행 중 오류가 발생했습니다.', {
        variant: 'destructive',
      });
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <header className="mb-8 text-center">
        <h1 className="text-3xl font-bold mb-2">통합 테스트 및 품질 검증</h1>
        <p className="text-gray-600">
          AI 프롬프트 최적화 웹 도구의 모든 기능을 테스트하고 품질을 검증합니다
        </p>
      </header>

      <div className="grid grid-cols-1 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>테스트 실행</CardTitle>
            <CardDescription>
              모든 기능에 대한 통합 테스트를 실행합니다
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={handleRunTests} 
              disabled={isRunning}
              className="w-full"
            >
              {isRunning ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  테스트 실행 중...
                </>
              ) : (
                '모든 테스트 실행'
              )}
            </Button>
          </CardContent>
        </Card>

        {summary && (
          <Card>
            <CardHeader>
              <CardTitle>테스트 요약</CardTitle>
              <CardDescription>
                테스트 결과 요약 정보
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-4 gap-4 mb-4">
                <div className="bg-gray-100 p-4 rounded-md text-center">
                  <div className="text-2xl font-bold">{summary.total}</div>
                  <div className="text-sm text-gray-600">전체 테스트</div>
                </div>
                <div className="bg-green-100 p-4 rounded-md text-center">
                  <div className="text-2xl font-bold text-green-700">{summary.passed}</div>
                  <div className="text-sm text-green-700">성공</div>
                </div>
                <div className="bg-red-100 p-4 rounded-md text-center">
                  <div className="text-2xl font-bold text-red-700">{summary.failed}</div>
                  <div className="text-sm text-red-700">실패</div>
                </div>
                <div className="bg-blue-100 p-4 rounded-md text-center">
                  <div className="text-2xl font-bold text-blue-700">{summary.passRate.toFixed(1)}%</div>
                  <div className="text-sm text-blue-700">성공률</div>
                </div>
              </div>

              {summary.failed > 0 && (
                <div className="mt-4">
                  <h3 className="text-lg font-semibold mb-2">실패한 테스트</h3>
                  <ul className="list-disc pl-5 space-y-1 text-red-700">
                    {summary.failedTests.map((test: string, index: number) => (
                      <li key={index}>{test}</li>
                    ))}
                  </ul>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {testResults.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>상세 테스트 결과</CardTitle>
              <CardDescription>
                각 테스트의 상세 결과
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {testResults.map((result, index) => (
                  <div key={index} className="border rounded-md overflow-hidden">
                    <div className={`p-4 ${result.success ? 'bg-green-50' : 'bg-red-50'}`}>
                      <div className="flex justify-between items-center">
                        <h3 className={`font-medium ${result.success ? 'text-green-700' : 'text-red-700'}`}>
                          {result.name}
                        </h3>
                        <span className={`px-2 py-1 text-xs rounded-full ${result.success ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
                          {result.success ? '성공' : '실패'}
                        </span>
                      </div>
                      <p className="text-sm mt-2">{result.message}</p>
                      <div className="text-xs text-gray-500 mt-1">
                        실행 시간: {result.duration.toFixed(2)}ms
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default TestPage;
