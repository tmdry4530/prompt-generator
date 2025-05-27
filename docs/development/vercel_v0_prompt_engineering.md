# Vercel v0 모델 프롬프트 엔지니어링 가이드라인

## 개요
Vercel v0는 자연어로 아이디어를 설명하면 코드와 UI를 모두 생성하는 페어 프로그래머 도구입니다. v0-1.0-md 모델은 현대적인 웹 애플리케이션 구축에 최적화되어 있으며, 텍스트와 이미지 입력을 지원하고 빠른 스트리밍 응답을 제공합니다. OpenAI Chat Completions API 형식과 호환되어 다양한 도구와 SDK에서 활용할 수 있습니다.

## 주요 특성
- **프레임워크 인식 완성**: Next.js 및 Vercel과 같은 현대적 스택에 최적화
- **자동 수정**: 생성 중 일반적인 코딩 문제를 식별하고 수정
- **빠른 편집**: 인라인 편집을 실시간으로 스트리밍
- **OpenAI 호환**: OpenAI API 형식을 지원하는 모든 도구나 SDK와 함께 사용 가능
- **멀티모달**: 텍스트와 이미지 입력(base64 인코딩) 모두 지원

## 프롬프트 엔지니어링 가이드라인

### 1. 프로젝트 유형 명시
v0는 다양한 프로젝트 유형을 생성할 수 있으므로, 명확한 프로젝트 유형을 지정하는 것이 중요합니다:

- **명확한 프로젝트 유형 지정**: "Create a landing page for a tech startup" 또는 "Build a full-stack app with authentication"
- **구체적인 기능 요청**: "Add a contact form with email validation" 또는 "Include a dark mode toggle"
- **기술 스택 명시**: "Using Next.js and Tailwind CSS" 또는 "With a Supabase backend"

### 2. 상세한 디자인 요구사항 제공
UI 생성 품질을 높이기 위한 프롬프트 전략:

- **디자인 스타일 명시**: "Modern minimalist design" 또는 "Corporate professional look"
- **색상 체계 지정**: "Using a blue and white color scheme" 또는 "With earth tones"
- **레이아웃 구조화**: "Three-column layout with a hero section" 또는 "Mobile-first design with a bottom navigation"
- **참조 이미지 활용**: 이미지 입력을 통해 디자인 참조 제공

### 3. 코드 생성 최적화
고품질 코드 생성을 위한 프롬프트 전략:

- **코드 구조 지정**: "Organize code using the feature-based folder structure" 또는 "Follow clean architecture principles"
- **특정 패턴 요청**: "Use React hooks for state management" 또는 "Implement with TypeScript interfaces"
- **성능 고려사항 포함**: "Optimize for performance with code splitting" 또는 "Implement lazy loading for images"
- **접근성 요구사항 추가**: "Ensure WCAG compliance" 또는 "Add proper aria labels"

### 4. 통합 및 확장성 지정
서드파티 서비스 통합을 위한 프롬프트 전략:

- **통합 서비스 명시**: "Integrate with Supabase for authentication" 또는 "Connect to Stripe for payments"
- **API 요구사항 상세화**: "Include REST API endpoints for user management" 또는 "Set up GraphQL queries"
- **환경 변수 처리**: "Handle environment variables securely" 또는 "Set up configuration for multiple environments"

### 5. 반복적 개선 전략
생성된 결과를 개선하기 위한 프롬프트 전략:

- **구체적인 수정 요청**: "Update the navigation to be sticky" 또는 "Change the button color to match the brand"
- **코드 리팩토링 지시**: "Refactor the authentication logic for better security" 또는 "Optimize database queries"
- **기능 확장 요청**: "Add pagination to the product list" 또는 "Implement a search feature"

### 6. 멀티모달 입력 활용
이미지와 텍스트를 함께 사용하는 프롬프트 전략:

- **디자인 참조 제공**: 스크린샷이나 디자인 이미지를 base64로 인코딩하여 제공
- **UI 요소 지정**: "Create a component similar to the one in this image" + 이미지 첨부
- **스타일 가이드 참조**: "Follow the design system shown in this image" + 이미지 첨부

## API 사용 예시

### 기본 텍스트 프롬프트
```json
{
  "model": "v0-1.0-md",
  "messages": [
    { "role": "user", "content": "Create a Next.js landing page for a SaaS product with a hero section, features grid, pricing table, and contact form. Use a modern design with blue and white colors." }
  ]
}
```

### 멀티모달 프롬프트 (이미지 + 텍스트)
```json
{
  "model": "v0-1.0-md",
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "Create a landing page similar to this design but for a fitness app" },
        { "type": "image_url", "image_url": { "url": "data:image/jpeg;base64,..." } }
      ]
    }
  ]
}
```

### 스트리밍 응답 요청
```json
{
  "model": "v0-1.0-md",
  "stream": true,
  "messages": [
    { "role": "user", "content": "Build a React component for a product card with image, title, price, and add to cart button" }
  ]
}
```

## 사용 사례 및 권장 시나리오
- 랜딩 페이지 및 마케팅 웹사이트 생성
- 풀스택 애플리케이션 프로토타이핑
- 블로그 및 콘텐츠 관리 시스템 구축
- 챗봇 및 대화형 인터페이스 개발
- 데이터 분석 및 시각화 도구 생성
- 고객 지원 시스템 구현

## 제한사항 및 주의사항
- 현재 베타 버전으로 Premium 또는 Team 플랜 필요
- 일일 최대 메시지 수: 200개
- 최대 컨텍스트 윈도우 크기: 128,000 토큰
- 최대 출력 컨텍스트 크기: 32,000 토큰
- 생성된 코드는 검토 및 테스트 필요

## 참고 자료
- Vercel v0 공식 문서
- v0 API 문서
- Vercel AI SDK 문서
