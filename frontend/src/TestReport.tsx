// 테스트 결과 보고서: 전체 기능 테스트 결과 및 품질 검증 보고서
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Separator } from './components/ui/separator';
import { Badge } from './components/ui/badge';
import { CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { runAllTests, summarizeTestResults, TestResult } from './utils/testing';

const TestReport: React.FC = () => {
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [testDate, setTestDate] = useState<string>('');

  useEffect(() => {
    const runTests = async () => {
      setIsLoading(true);
      try {
        // 테스트 실행
        const results = await runAllTests();
        setTestResults(results);
        
        // 결과 요약
        const resultSummary = summarizeTestResults(results);
        setSummary(resultSummary);
        
        // 테스트 날짜 설정
        setTestDate(new Date().toLocaleString());
      } catch (error) {
        console.error('테스트 실행 오류:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    runTests();
  }, []);

  const getStatusIcon = (success: boolean) => {
    return success ? (
      <CheckCircle className="h-5 w-5 text-green-500" />
    ) : (
      <XCircle className="h-5 w-5 text-red-500" />
    );
  };

  const getOverallStatus = () => {
    if (!summary) return null;
    
    if (summary.passRate === 100) {
      return (
        <div className="flex items-center space-x-2 text-green-600">
          <CheckCircle className="h-6 w-6" />
          <span className="font-medium">모든 테스트 통과</span>
        </div>
      );
    } else if (summary.passRate >= 80) {
      return (
        <div className="flex items-center space-x-2 text-yellow-600">
          <AlertTriangle className="h-6 w-6" />
          <span className="font-medium">대부분 테스트 통과 (일부 실패)</span>
        </div>
      );
    } else {
      return (
        <div className="flex items-center space-x-2 text-red-600">
          <XCircle className="h-6 w-6" />
          <span className="font-medium">다수 테스트 실패</span>
        </div>
      );
    }
  };

  const downloadReport = () => {
    if (!summary) return;
    
    const reportContent = `
# AI 프롬프트 최적화 웹 도구 테스트 보고서

## 테스트 요약
- 테스트 날짜: ${testDate}
- 전체 테스트: ${summary.total}
- 성공: ${summary.passed}
- 실패: ${summary.failed}
- 성공률: ${summary.passRate.toFixed(1)}%

## 실패한 테스트
${summary.failedTests.length > 0 ? summary.failedTests.map((test: string) => `- ${test}`).join('\n') : '- 없음'}

## 상세 테스트 결과
${testResults.map(result => `
### ${result.name}
- 결과: ${result.success ? '성공' : '실패'}
- 메시지: ${result.message}
- 실행 시간: ${result.duration.toFixed(2)}ms
`).join('\n')}
    `;
    
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `test-report-${new Date().toISOString().split('T')[0]}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p className="text-lg">테스트 실행 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4">
      <header className="mb-8">
        <h1 className="text-3xl font-bold mb-2">테스트 결과 보고서</h1>
        <p className="text-gray-600">
          AI 프롬프트 최적화 웹 도구의 전체 기능 테스트 결과 및 품질 검증 보고서
        </p>
        <div className="mt-4">
          <Badge variant={summary?.passRate === 100 ? 'default' : summary?.passRate >= 80 ? 'outline' : 'destructive'}>
            테스트 날짜: {testDate}
          </Badge>
        </div>
      </header>

      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle>테스트 요약</CardTitle>
              <CardDescription>
                전체 테스트 결과 요약
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between items-center mb-6">
                <div className="text-2xl font-bold">{summary.passRate.toFixed(1)}%</div>
                {getOverallStatus()}
              </div>
              
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-gray-100 p-4 rounded-md text-center">
                  <div className="text-xl font-bold">{summary.total}</div>
                  <div className="text-sm text-gray-600">전체 테스트</div>
                </div>
                <div className="bg-green-100 p-4 rounded-md text-center">
                  <div className="text-xl font-bold text-green-700">{summary.passed}</div>
                  <div className="text-sm text-green-700">성공</div>
                </div>
                <div className="bg-red-100 p-4 rounded-md text-center">
                  <div className="text-xl font-bold text-red-700">{summary.failed}</div>
                  <div className="text-sm text-red-700">실패</div>
                </div>
              </div>
              
              <div className="mt-6">
                <Button onClick={downloadReport} variant="outline" className="w-full">
                  보고서 다운로드
                </Button>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader>
              <CardTitle>실패한 테스트</CardTitle>
              <CardDescription>
                실패한 테스트 목록 및 원인
              </CardDescription>
            </CardHeader>
            <CardContent>
              {summary.failed > 0 ? (
                <ul className="space-y-2">
                  {summary.failedTests.map((test: string, index: number) => (
                    <li key={index} className="p-3 bg-red-50 rounded-md text-red-800 text-sm">
                      {test}
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="p-4 bg-green-50 rounded-md text-green-800 text-center">
                  <CheckCircle className="h-8 w-8 mx-auto mb-2" />
                  <p>모든 테스트가 성공적으로 통과했습니다!</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle>상세 테스트 결과</CardTitle>
          <CardDescription>
            각 테스트의 상세 결과 및 실행 시간
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {testResults.map((result, index) => (
              <div key={index} className={`p-4 rounded-md ${result.success ? 'bg-green-50' : 'bg-red-50'}`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(result.success)}
                    <h3 className="font-medium">{result.name}</h3>
                  </div>
                  <Badge variant={result.success ? 'default' : 'destructive'}>
                    {result.success ? '성공' : '실패'}
                  </Badge>
                </div>
                <Separator className="my-2" />
                <div className="mt-2 text-sm">
                  <p><strong>메시지:</strong> {result.message}</p>
                  <p><strong>실행 시간:</strong> {result.duration.toFixed(2)}ms</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default TestReport;
