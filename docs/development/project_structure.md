# 프로젝트 구조 설명 문서

## 디렉토리 구조 개요

```
ai-prompt-optimizer-restructured/
├── frontend/                # 프론트엔드 코드
│   ├── src/                 # 소스 코드
│   │   ├── components/      # 재사용 가능한 UI 컴포넌트
│   │   ├── utils/           # 유틸리티 함수
│   │   ├── styles/          # 스타일 관련 파일
│   │   ├── hooks/           # 커스텀 React 훅
│   │   └── types/           # TypeScript 타입 정의
│   ├── .env.development     # 개발 환경 설정
│   └── .env.production      # 프로덕션 환경 설정
│
├── backend/                 # 백엔드 코드
│   ├── src/                 # 소스 코드
│   │   ├── services/        # 비즈니스 로직 서비스
│   │   ├── models/          # 데이터 모델
│   │   ├── routes/          # API 라우트 정의
│   │   ├── utils/           # 유틸리티 함수
│   │   └── middlewares/     # 미들웨어
│   ├── tests/               # 테스트 코드
│   └── config/              # 설정 파일
│       ├── .env.development # 개발 환경 설정
│       └── .env.production  # 프로덕션 환경 설정
│
└── docs/                    # 문서
    ├── api/                 # API 문서
    ├── user-guide/          # 사용자 가이드
    └── development/         # 개발 문서
```

## 주요 파일 설명

### 프론트엔드

- `frontend/src/App.tsx`: 메인 애플리케이션 컴포넌트
- `frontend/src/components/ModelSelector.tsx`: AI 모델 선택 컴포넌트
- `frontend/src/utils/api.ts`: API 통신 유틸리티

### 백엔드

- `backend/src/main.py`: 메인 애플리케이션 진입점
- `backend/src/services/prompt_optimizer/optimizer.py`: 프롬프트 최적화 엔진

## 환경 설정

### 프론트엔드 환경 변수

- `VITE_API_BASE_URL`: API 서버 기본 URL
- `NODE_ENV`: 환경 모드 (development/production)
- `VITE_APP_TITLE`: 애플리케이션 제목

### 백엔드 환경 변수

- `PORT`: 서버 포트
- `FLASK_ENV`: Flask 환경 모드
- `DEBUG`: 디버그 모드 활성화 여부
- `CORS_ORIGINS`: CORS 허용 출처
- `LOG_LEVEL`: 로깅 레벨
- `LOG_FILE`: 로그 파일 경로

## 네트워크 오류 해결 방법

이전 버전에서는 프론트엔드 코드에 API 엔드포인트가 `http://localhost:5000/api`로 하드코딩되어 있어 배포 환경에서 API 연결 오류가 발생했습니다. 이 문제를 해결하기 위해:

1. 환경변수 기반 API 엔드포인트 관리 도입
2. 개발/프로덕션 환경별 자동 분기 처리
3. 모든 API 호출을 `getApiUrl()` 유틸리티 함수로 통일

이제 프로덕션 환경에서는 현재 호스트 기반으로 API 경로가 자동 설정되어 네트워크 오류가 발생하지 않습니다.
