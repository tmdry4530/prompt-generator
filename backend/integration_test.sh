#!/bin/bash

# 통합 테스트 스크립트
# 개발 및 프로덕션 환경에서 전체 스택 통합 테스트를 수행합니다.

echo "===== AI 프롬프트 최적화 도구 통합 테스트 ====="
echo "테스트 시작 시간: $(date)"
echo "----------------------------------------"

# 작업 디렉토리 설정
BASE_DIR="/home/ubuntu/ai-prompt-optimizer-restructured"
FRONTEND_DIR="$BASE_DIR/frontend"
BACKEND_DIR="$BASE_DIR/backend"
TEST_RESULTS_DIR="$BASE_DIR/tests/results"

# 테스트 결과 디렉토리 생성
mkdir -p $TEST_RESULTS_DIR

# 환경 설정
echo "환경 설정 확인 중..."
if [ -f "$FRONTEND_DIR/.env.development" ]; then
  echo "✓ 프론트엔드 개발 환경 설정 파일 존재"
else
  echo "✗ 프론트엔드 개발 환경 설정 파일 누락"
  exit 1
fi

if [ -f "$FRONTEND_DIR/.env.production" ]; then
  echo "✓ 프론트엔드 프로덕션 환경 설정 파일 존재"
else
  echo "✗ 프론트엔드 프로덕션 환경 설정 파일 누락"
  exit 1
fi

if [ -f "$BACKEND_DIR/config/.env.development" ]; then
  echo "✓ 백엔드 개발 환경 설정 파일 존재"
else
  echo "✗ 백엔드 개발 환경 설정 파일 누락"
  exit 1
fi

if [ -f "$BACKEND_DIR/config/.env.production" ]; then
  echo "✓ 백엔드 프로덕션 환경 설정 파일 존재"
else
  echo "✗ 백엔드 프로덕션 환경 설정 파일 누락"
  exit 1
fi

echo "----------------------------------------"
echo "백엔드 서버 시작 중..."

# 백엔드 서버 시작 (개발 환경)
cd $BACKEND_DIR
export FLASK_ENV=development
python3 -m src.main > $TEST_RESULTS_DIR/backend_dev.log 2>&1 &
BACKEND_PID=$!

# 백엔드 서버가 시작될 때까지 대기
echo "백엔드 서버 시작 대기 중..."
sleep 5

# 백엔드 서버 상태 확인
echo "백엔드 API 상태 확인 중..."
HEALTH_CHECK=$(curl -s http://localhost:5000/api/health)
if [[ $HEALTH_CHECK == *"\"status\":\"ok\""* ]]; then
  echo "✓ 백엔드 서버 정상 작동 중"
  echo "응답: $HEALTH_CHECK"
else
  echo "✗ 백엔드 서버 상태 확인 실패"
  echo "응답: $HEALTH_CHECK"
  kill $BACKEND_PID
  exit 1
fi

echo "----------------------------------------"
echo "API 엔드포인트 테스트 중..."

# 모델 목록 API 테스트
echo "모델 목록 API 테스트 중..."
MODELS_RESPONSE=$(curl -s http://localhost:5000/api/models)
if [[ $MODELS_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ 모델 목록 API 정상 작동"
  echo "모델 수: $(echo $MODELS_RESPONSE | grep -o "model_id" | wc -l)"
else
  echo "✗ 모델 목록 API 테스트 실패"
  echo "응답: $MODELS_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# 프롬프트 최적화 API 테스트
echo "프롬프트 최적화 API 테스트 중..."
OPTIMIZE_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"input_text":"인공지능의 미래에 대한 에세이를 작성해주세요", "model_id":"gpt-4o"}' http://localhost:5000/api/optimize)
if [[ $OPTIMIZE_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ 프롬프트 최적화 API 정상 작동"
else
  echo "✗ 프롬프트 최적화 API 테스트 실패"
  echo "응답: $OPTIMIZE_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# 모델 팁 API 테스트
echo "모델 팁 API 테스트 중..."
TIPS_RESPONSE=$(curl -s http://localhost:5000/api/model/gpt-4o/tips)
if [[ $TIPS_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ 모델 팁 API 정상 작동"
else
  echo "✗ 모델 팁 API 테스트 실패"
  echo "응답: $TIPS_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

echo "----------------------------------------"
echo "프론트엔드 빌드 테스트 중..."

# 프론트엔드 빌드 테스트 (개발 환경)
cd $FRONTEND_DIR
echo "개발 환경 빌드 테스트 중..."
npm run build > $TEST_RESULTS_DIR/frontend_dev_build.log 2>&1
if [ $? -eq 0 ]; then
  echo "✓ 개발 환경 빌드 성공"
else
  echo "✗ 개발 환경 빌드 실패"
  cat $TEST_RESULTS_DIR/frontend_dev_build.log
  kill $BACKEND_PID
  exit 1
fi

# 프론트엔드 빌드 테스트 (프로덕션 환경)
echo "프로덕션 환경 빌드 테스트 중..."
NODE_ENV=production npm run build > $TEST_RESULTS_DIR/frontend_prod_build.log 2>&1
if [ $? -eq 0 ]; then
  echo "✓ 프로덕션 환경 빌드 성공"
else
  echo "✗ 프로덕션 환경 빌드 실패"
  cat $TEST_RESULTS_DIR/frontend_prod_build.log
  kill $BACKEND_PID
  exit 1
fi

echo "----------------------------------------"
echo "프로덕션 환경 테스트 중..."

# 백엔드 서버 재시작 (프로덕션 환경)
kill $BACKEND_PID
cd $BACKEND_DIR
export FLASK_ENV=production
python3 -m src.main > $TEST_RESULTS_DIR/backend_prod.log 2>&1 &
BACKEND_PID=$!

# 백엔드 서버가 시작될 때까지 대기
echo "프로덕션 백엔드 서버 시작 대기 중..."
sleep 5

# 백엔드 서버 상태 확인 (프로덕션)
echo "프로덕션 백엔드 API 상태 확인 중..."
HEALTH_CHECK=$(curl -s http://localhost:5000/api/health)
if [[ $HEALTH_CHECK == *"\"status\":\"ok\""* && $HEALTH_CHECK == *"\"environment\":\"production\""* ]]; then
  echo "✓ 프로덕션 백엔드 서버 정상 작동 중"
  echo "응답: $HEALTH_CHECK"
else
  echo "✗ 프로덕션 백엔드 서버 상태 확인 실패"
  echo "응답: $HEALTH_CHECK"
  kill $BACKEND_PID
  exit 1
fi

# 정적 파일 서빙 테스트
echo "정적 파일 서빙 테스트 중..."
INDEX_RESPONSE=$(curl -s http://localhost:5000/)
if [[ $INDEX_RESPONSE == *"<!DOCTYPE html>"* ]]; then
  echo "✓ 정적 파일 서빙 정상 작동"
else
  echo "✗ 정적 파일 서빙 테스트 실패"
  kill $BACKEND_PID
  exit 1
fi

# 백엔드 서버 종료
kill $BACKEND_PID

echo "----------------------------------------"
echo "통합 테스트 결과: 성공"
echo "테스트 완료 시간: $(date)"
echo "모든 테스트가 성공적으로 완료되었습니다."
echo "===== 테스트 종료 ====="
