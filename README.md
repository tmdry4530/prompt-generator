# Model Optimization Prompt Generator

**AI 모델별로 최적화된 프롬프트를 생성하는 웹 애플리케이션**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![React](https://img.shields.io/badge/react-18.0+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)

## 🎯 프로젝트 개요

Model Optimization Prompt Generator는 GPT-4, Claude-3, Llama-2, Gemini Pro 등 다양한 AI 모델의 특성에 맞게 프롬프트를 최적화하여 더 나은 AI 응답을 얻을 수 있도록 도와주는 웹 애플리케이션입니다.

### ✨ 주요 기능

- **🤖 다중 모델 지원**: GPT-4, Claude-3, Llama-2, Gemini Pro
- **🎨 모델별 최적화**: 각 모델의 특성에 맞춘 프롬프트 구조 적용
- **📝 템플릿 라이브러리**: 코드 생성, 분석, 글쓰기, 요약 등 다양한 템플릿
- **📊 사용 통계**: 모델별 사용 현황 및 인기 템플릿 분석
- **💾 히스토리 관리**: 생성된 프롬프트 자동 저장 및 재사용
- **📋 원클릭 복사**: 최적화된 프롬프트 쉬운 복사

## 🚀 빠른 시작

### 필수 요구사항

- **Python 3.8+**
- **Node.js 16+**
- **PowerShell 7.x** (Windows)

### 1️⃣ 저장소 클론

```powershell
git clone https://github.com/your-repo/prompt-generator.git
cd prompt-generator
```

### 2️⃣ 서버 시작

```powershell
# 실행 권한 부여 (최초 1회)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 서버 시작 (대화형 메뉴)
.\start-servers.ps1

# 또는 직접 실행
.\start-servers.ps1               # Frontend + Backend 동시 시작 (개발 모드)
.\start-servers.ps1 -Backend false # Frontend만 시작
.\start-servers.ps1 -Frontend false # Backend만 시작

# Linux/macOS 환경
./start-servers.sh                 # 프론트엔드와 백엔드 동시 시작
```

### 3️⃣ 브라우저 접속

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 📱 사용법

### 기본 프롬프트 최적화

1. **모델 선택**: 드롭다운에서 원하는 AI 모델 선택
2. **작업 입력**: 텍스트 영역에 요청할 작업 설명
3. **최적화 실행**: "프롬프트 최적화" 버튼 클릭
4. **결과 복사**: 생성된 최적화 프롬프트를 클립보드에 복사

### 예시 작업 활용

각 모델별로 준비된 예시 작업들을 클릭하여 빠르게 테스트해볼 수 있습니다:

- **GPT-4**: CSV 파일 처리, 양자컴퓨팅 설명, 마케팅 전략 등
- **Claude-3**: 연구논문 분석, 보안 검토, 기술 문서 작성 등
- **Llama-2**: REST API 구현, 코드 변환, 알고리즘 추천 등
- **Gemini Pro**: 멀티모달 분석, 복합 문서 생성 등

## 🏗️ 아키텍처

```
prompt-generator/
├── backend/                 # Flask API 서버
│   ├── src/
│   │   ├── app.py          # 메인 Flask 애플리케이션
│   │   ├── model_optimizer.py    # 프롬프트 최적화 엔진
│   │   └── template_library.py  # 템플릿 라이브러리
│   └── requirements.txt     # Python 의존성
├── frontend/               # React 웹 애플리케이션
│   ├── src/
│   │   ├── App.tsx         # 메인 React 컴포넌트
│   │   └── components/     # UI 컴포넌트들
│   └── package.json        # Node.js 의존성
├── start-servers.ps1       # Windows용 서버 시작 스크립트
└── start-servers.sh        # Linux/macOS용 서버 시작 스크립트
```

## 🔌 API 엔드포인트

### 모델 정보

```http
GET /api/models
```

지원되는 AI 모델 목록과 상세 정보를 반환합니다.

### 프롬프트 최적화

```http
POST /api/optimize
Content-Type: application/json

{
  "model": "gpt-4",
  "task": "사용자 작업 설명"
}
```

### 예시 작업

```http
GET /api/examples/{model}
```

특정 모델의 예시 작업들을 반환합니다.

### 사용 통계

```http
GET /api/stats
```

서비스 사용 통계를 반환합니다.

## 📋 체크리스트 완료 현황

### ✅ Priority 1: Core Functionality (Deploy Today)

- [x] **Step 1**: Basic Working Generator
  - [x] ModelOptimizationPromptGenerator 클래스 구현
  - [x] 4개 모델 지원 (GPT-4, Claude-3, Llama-2, Gemini Pro)
  - [x] 모델별 최적화 규칙 적용
- [x] **Step 2**: Simple Web Interface
  - [x] React + TypeScript 프론트엔드
  - [x] 모델 선택 드롭다운
  - [x] 작업 입력 텍스트 영역
  - [x] 최적화 버튼 및 결과 표시

### ✅ Priority 2: Essential Features (Deploy This Week)

- [x] **Step 3**: Add Prompt Templates

  - [x] PromptTemplateLibrary 클래스 구현
  - [x] 5개 카테고리 템플릿 (코드생성, 분석, 글쓰기, 번역, 요약)
  - [x] 모델별 템플릿 최적화

- [x] **Step 4**: Basic API Endpoint
  - [x] Flask 기반 REST API
  - [x] CORS 설정 및 에러 핸들링
  - [x] 모델 정보, 최적화, 예시, 통계 API

### ✅ Priority 3: User Experience (Deploy Next Week)

- [x] **Step 5**: Add Common Use Case Examples

  - [x] 모델별 예시 작업 데이터베이스
  - [x] 클릭으로 예시 선택 기능
  - [x] 동적 예시 로딩

- [x] **Step 6**: Add Copy-to-Clipboard and History
  - [x] 클립보드 복사 기능
  - [x] 로컬 스토리지 기반 히스토리
  - [x] 히스토리에서 복원 기능
  - [x] 사용 통계 대시보드

## 🔧 개발 가이드

### Backend 개발

```powershell
cd backend

# 가상환경 생성
py -m venv .venv

# 가상환경 활성화
.\.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt

# 개발 서버 시작
python src/app.py
```

### Frontend 개발

```powershell
cd frontend

# 의존성 설치
npm install

# 개발 서버 시작
npm run dev

# 프로덕션 빌드
npm run build
```

## 🧪 테스트

### Backend 테스트

```powershell
cd backend
pytest
```

### Frontend 테스트

```powershell
cd frontend
npm test
```

### 통합 테스트

```powershell
# 전체 테스트 실행
.\run-all-tests.ps1
```

## 📈 성능 최적화

- **캐싱**: 모델 정보 및 템플릿 메모리 캐싱
- **지연 로딩**: 필요시에만 데이터 로드
- **경량화**: 최소한의 의존성으로 빠른 시작
- **반응형**: 모바일 친화적 UI

## 🛠️ 배포

### Heroku 배포

```powershell
# Heroku CLI 설치
winget install Heroku.CLI

# 앱 생성 및 배포
heroku create your-app-name
git push heroku main
```

### Vercel 배포

```powershell
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel --prod
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 제작자

- **개발자**: Chamdom
- **이메일**: wjdtmdry9904@gmail.com
- **프로젝트 링크**: https://github.com/tmdry4530/prompt-generator

---

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!
