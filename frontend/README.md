# 프롬프트 생성기

모델 최적화 프롬프트 생성기는 다양한 AI 모델에 최적화된 프롬프트를 생성하는 웹 애플리케이션입니다.

## 기능

- 다양한 AI 모델에 맞춤화된 프롬프트 최적화
- 모델별 최적화 팁과 가이드 제공
- 프롬프트 생성 히스토리 관리
- 사용 통계 및 분석

## 기술 스택

- **프론트엔드**: Next.js 15, React 18, TypeScript
- **UI 라이브러리**: Tailwind CSS, shadcn/ui
- **상태 관리**: React Hooks
- **API 통신**: Axios

## 개발 환경 설정

```bash
# 의존성 설치
pnpm install

# 개발 서버 실행
pnpm dev

# 프로덕션 빌드
pnpm build

# 빌드 결과물 실행
pnpm start
```

## 배포

이 프로젝트는 정적 사이트로 빌드됩니다 (`output: 'export'`). 빌드 결과물은 `dist` 디렉토리에 생성됩니다.

### Vercel 배포 설정

- **프레임워크 프리셋**: Next.js
- **루트 디렉토리**: frontend
- **빌드 명령어**: pnpm run build
- **출력 디렉토리**: dist

## 프로젝트 구조

```
frontend/
├── app/                 # Next.js App Router
│   ├── _not-found/      # 404 페이지
│   ├── layout.tsx       # 루트 레이아웃
│   └── page.tsx         # 홈페이지
├── components/          # UI 컴포넌트
│   ├── ui/              # 기본 UI 컴포넌트
│   └── prompt-generator.tsx # 메인 컴포넌트
├── lib/                 # 유틸리티 함수
├── public/              # 정적 파일
└── styles/              # 글로벌 스타일
```
