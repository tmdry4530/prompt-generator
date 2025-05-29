# AI Prompt Optimization Tool - 빠른 시작 가이드

## 🚀 서버 통합 실행 스크립트

이 프로젝트는 frontend(React + Vite)와 backend(Python Flask)를 쉽게 실행할 수 있는 통합 스크립트를 제공합니다.

## 📋 필수 준비사항

### Windows 환경 요구사항

- **운영체제**: Windows 10/11 (64-bit)
- **PowerShell**: 5.1 이상 (권장: PowerShell 7+)
- **Node.js**: 18.x 이상 (LTS 버전)
- **Python**: 3.11 이상
- **Git**: 최신 버전

### 설치 확인

PowerShell에서 다음 명령어로 설치 상태를 확인하세요:

```powershell
# 버전 확인
node --version
python --version
git --version
pwsh --version  # PowerShell 7의 경우
```

## 🛠️ 환경 설정

### 1단계: 자동 환경 설정

```powershell
# 프로젝트 디렉터리로 이동
cd /path/to/prompt-generator

# 자동 환경 설정 실행
.\setup-environment.ps1 -All
```

### 수동 설정 (필요한 경우)

```powershell
# Frontend만 설정
.\setup-environment.ps1 -Frontend

# Backend만 설정
.\setup-environment.ps1 -Backend

# 상세 로그와 함께 설정
.\setup-environment.ps1 -All -Verbose
```

## 🚀 서버 실행

### 기본 실행 (개발 모드)

```powershell
# Frontend + Backend 모두 실행
.\start-servers.ps1

# 실행 후 접속 URL:
# Frontend: http://localhost:5173
# Backend:  http://localhost:5000
```

### 고급 실행 옵션

#### 개발 환경

```powershell
# 개발 모드 (기본값)
.\start-servers.ps1 -Mode dev

# Frontend만 실행
.\start-servers.ps1 -Backend false

# Backend만 실행
.\start-servers.ps1 -Frontend false

# 사용자 정의 포트로 실행
.\start-servers.ps1 -FrontendPort 3000 -BackendPort 8000

# 상세 로그와 함께 실행
.\start-servers.ps1 -Verbose
```

#### 프로덕션 환경

```powershell
# 프로덕션 모드
.\start-servers.ps1 -Mode prod

# Frontend 빌드만 수행
.\start-servers.ps1 -Mode build -Backend false
```

#### Watch 모드 (실시간 reload)

```powershell
# Frontend Watch 모드 활성화
.\start-servers.ps1 -Watch
```

## 📊 서버 상태 확인

### 현재 서버 상태 확인

```powershell
# 기본 상태 확인
.\check-servers.ps1

# 상세 시스템 정보 포함
.\check-servers.ps1 -Verbose

# 사용자 정의 포트 확인
.\check-servers.ps1 -FrontendPort 3000 -BackendPort 8000
```

### 서버 상태 해석

- ✅ **RUNNING**: 서버가 정상 작동 중
- ❌ **NOT RUNNING**: 서버가 실행되지 않음

## 🔧 문제 해결

### 일반적인 문제들

#### 1. 포트 충돌 오류

```powershell
# 다른 포트로 실행
.\start-servers.ps1 -FrontendPort 3000 -BackendPort 8000

# 현재 사용 중인 포트 확인
netstat -ano | findstr ":5173"
netstat -ano | findstr ":5000"
```

#### 2. Node.js 설치 문제

```powershell
# winget으로 Node.js 설치
winget install -e --id OpenJS.NodeJS

# npm 글로벌 패키지 권한 문제 해결
npm config set prefix "%APPDATA%\npm"
```

#### 3. Python 가상환경 문제

```powershell
# Backend 디렉터리에서 수동 설정
cd backend

# 가상환경 재생성
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. PowerShell 실행 정책 문제

```powershell
# 현재 사용자에 대해 실행 정책 변경
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 또는 스크립트 실행 시 바이패스
powershell -ExecutionPolicy Bypass -File .\start-servers.ps1
```

### 로그 및 디버깅

#### 상세 로그 활성화

```powershell
# 모든 스크립트에서 상세 로그 보기
.\start-servers.ps1 -Verbose
.\setup-environment.ps1 -Verbose
.\check-servers.ps1 -Verbose
```

#### 수동 서버 실행 (디버깅용)

```powershell
# Frontend 수동 실행
cd frontend
npm run dev

# Backend 수동 실행 (새 터미널)
cd backend
.\.venv\Scripts\Activate.ps1
python -m src.main
```

## 📂 프로젝트 구조 이해

```
prompt-generator/
├── frontend/                 # React + Vite + TypeScript
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # Python Flask API
│   ├── src/
│   ├── requirements.txt
│   └── .venv/               # Python 가상환경
├── start-servers.ps1         # 통합 서버 실행 스크립트
├── setup-environment.ps1     # 환경 설정 스크립트
└── check-servers.ps1         # 서버 상태 확인 스크립트
```

## 🎯 개발 워크플로우

### 일반적인 개발 과정

```powershell
# 1. 프로젝트 클론
git clone <repository-url>
cd prompt-generator

# 2. 환경 설정
.\setup-environment.ps1 -All

# 3. 개발 서버 시작
.\start-servers.ps1

# 4. 개발 작업...

# 5. 서버 상태 확인 (필요시)
.\check-servers.ps1

# 6. 서버 종료 (Ctrl+C)
```

### 배포 준비

```powershell
# 프로덕션 빌드 테스트
.\start-servers.ps1 -Mode prod

# Frontend만 빌드
.\start-servers.ps1 -Mode build -Backend false
```

## 💡 팁과 권장사항

### 성능 최적화

1. **SSD 사용 권장**: 빠른 빌드와 서버 시작을 위해
2. **충분한 RAM**: 최소 8GB, 권장 16GB 이상
3. **Antivirus 예외 설정**: node_modules와 .venv 디렉터리를 예외로 설정

### 개발 환경 권장사항

1. **Cursor/VSCode 확장**:

   - Python
   - TypeScript
   - ES7+ React/Redux/React-Native snippets
   - Prettier - Code formatter

2. **터미널 설정**:
   - Windows Terminal 사용 권장
   - PowerShell 7+ 사용

### 보안 고려사항

1. **환경 변수**: API 키는 환경 변수로 관리
2. **Git 무시**: `.env` 파일과 민감한 정보는 `.gitignore`에 추가
3. **의존성 업데이트**: 정기적으로 패키지 보안 업데이트 수행

## 🆘 도움말 보기

각 스크립트의 상세 도움말:

```powershell
.\start-servers.ps1 -Help
.\setup-environment.ps1 -Help
.\check-servers.ps1 -Help
```

## 📞 지원 및 문의

문제가 발생하면 다음 순서로 확인하세요:

1. 이 가이드의 문제 해결 섹션 참조
2. 각 스크립트의 `-Verbose` 옵션으로 상세 로그 확인
3. GitHub Issues에 문제 보고

---

**🎉 이제 AI Prompt Optimization Tool 개발을 시작할 준비가 완료되었습니다!**
