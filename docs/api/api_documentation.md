# AI 프롬프트 최적화 도구 API 문서

## 개요

AI 프롬프트 최적화 도구 API는 다양한 AI 모델에 최적화된 프롬프트를 생성하기 위한 RESTful API를 제공합니다. 이 문서는 API의 엔드포인트, 요청 및 응답 형식, 오류 처리 등에 대한 정보를 제공합니다.

## 기본 URL

```
https://[your-domain]/api
```

## 인증

현재 버전에서는 별도의 인증이 필요하지 않습니다.

## 엔드포인트

### 1. 서버 상태 확인

```
GET /health
```

**응답 예시:**
```json
{
  "status": "ok",
  "timestamp": "2025-05-27T01:42:00.000Z",
  "version": "1.0.0"
}
```

### 2. 사용 가능한 모델 목록 조회

```
GET /models
```

**응답 예시:**
```json
{
  "success": true,
  "models": [
    {
      "model_id": "gpt-4o",
      "model_name": "GPT-4o",
      "provider": "OpenAI",
      "category": "text",
      "capabilities": ["text-generation", "code-generation", "reasoning"],
      "supports_multimodal": true
    },
    {
      "model_id": "dalle-3",
      "model_name": "DALL-E 3",
      "provider": "OpenAI",
      "category": "image",
      "capabilities": ["image-generation"],
      "supports_multimodal": false
    }
  ]
}
```

### 3. 프롬프트 최적화

```
POST /optimize
```

**요청 본문:**
```json
{
  "input_text": "인공지능의 미래에 대한 에세이를 작성해주세요",
  "model_id": "gpt-4o",
  "additional_params": {
    "tone": "academic",
    "length": "long"
  }
}
```

**응답 예시:**
```json
{
  "success": true,
  "original_input": "인공지능의 미래에 대한 에세이를 작성해주세요",
  "optimized_prompt": "다음 주제에 대한 학술적 에세이를 작성해주세요: '인공지능의 미래: 기술적 발전, 사회적 영향, 그리고 윤리적 고려사항'. 에세이는 최소 1500단어로 작성하며, 다음 구조를 따라주세요:\n\n1. 서론: AI의 현재 상태와 주요 발전 방향 소개\n2. 본론:\n   - 기술적 발전 전망 (신경망 구조, 계산 능력, 학습 방법론)\n   - 사회경제적 영향 (일자리 변화, 생산성, 불평등)\n   - 윤리적 고려사항 (편향성, 투명성, 책임성)\n3. 결론: 지속 가능하고 인간 중심적인 AI 발전을 위한 제언\n\n각 섹션에서 최신 연구 결과와 전문가 의견을 인용하고, 다양한 관점을 균형 있게 다루어주세요. 학술적 어조를 유지하되, 복잡한 개념은 명확하게 설명해주세요.",
  "model_id": "gpt-4o",
  "model_info": {
    "model_name": "GPT-4o",
    "provider": "OpenAI",
    "capabilities": ["text-generation", "code-generation", "reasoning"]
  },
  "prompt_structure": {
    "components": [
      "주제 및 과제 명시",
      "형식 및 길이 지정",
      "구조적 가이드라인",
      "스타일 및 톤 지침",
      "내용 요소 상세화"
    ]
  },
  "generation_params": {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 2500
  },
  "analysis_result": {
    "keywords": ["인공지능", "미래", "에세이", "학술적", "기술 발전", "사회적 영향", "윤리"]
  },
  "intent_result": {
    "primary_intent": "학술적 에세이 작성 요청",
    "secondary_intent": "AI 미래 전망 탐색"
  }
}
```

### 4. 모델별 최적화 팁 조회

```
GET /model/{model_id}/tips
```

**매개변수:**
- `model_id`: 모델 ID
- `capability` (선택 사항): 특정 기능에 대한 팁만 조회

**응답 예시:**
```json
{
  "success": true,
  "model_id": "gpt-4o",
  "capability": null,
  "tips": [
    "명확한 지시문을 사용하세요 (예: '작성해주세요', '분석해주세요')",
    "복잡한 작업은 단계별로 나누어 요청하세요",
    "원하는 출력 형식을 구체적으로 지정하세요",
    "예시를 제공하면 더 정확한 결과를 얻을 수 있습니다"
  ]
}
```

### 5. 모델 프롬프트 구조 조회

```
GET /model/{model_id}/structure
```

**응답 예시:**
```json
{
  "success": true,
  "model_id": "gpt-4o",
  "structure": {
    "recommended_components": [
      "명확한 지시문",
      "맥락 정보",
      "형식 지정",
      "예시 (선택 사항)",
      "제약 조건 (선택 사항)"
    ],
    "templates": {
      "basic": "다음 [작업]을 수행해주세요: [상세 지시사항]. 출력 형식은 [형식]으로 해주세요.",
      "advanced": "# 작업: [작업 제목]\n## 배경: [맥락 정보]\n## 지시사항: [상세 지시사항]\n## 형식: [출력 형식]\n## 제약 조건: [제약 조건]"
    }
  }
}
```

### 6. 모델 정보 조회

```
GET /model/{model_id}/info
```

**응답 예시:**
```json
{
  "success": true,
  "model_id": "gpt-4o",
  "info": {
    "model_name": "GPT-4o",
    "provider": "OpenAI",
    "release_date": "2025-03-15",
    "description": "GPT-4o는 OpenAI의 최신 멀티모달 모델로, 텍스트 생성, 코드 작성, 추론 등 다양한 작업에 최적화되어 있습니다.",
    "capabilities": ["text-generation", "code-generation", "reasoning"],
    "supports_multimodal": true,
    "context_window": 128000,
    "training_data_cutoff": "2023-12-31"
  }
}
```

### 7. 모델 비교

```
POST /compare
```

**요청 본문:**
```json
{
  "model_ids": ["gpt-4o", "gpt-o3", "claude-sonnet-4"]
}
```

**응답 예시:**
```json
{
  "success": true,
  "comparison": {
    "models": [
      {
        "model_id": "gpt-4o",
        "model_name": "GPT-4o",
        "provider": "OpenAI",
        "strengths": ["광범위한 지식", "높은 추론 능력", "멀티모달 지원"],
        "weaknesses": ["비용", "일부 전문 분야 제한적 지식"]
      },
      {
        "model_id": "gpt-o3",
        "model_name": "GPT-o3",
        "provider": "OpenAI",
        "strengths": ["빠른 응답 속도", "효율적인 리소스 사용"],
        "weaknesses": ["GPT-4o보다 제한된 능력", "복잡한 추론에서 성능 저하"]
      },
      {
        "model_id": "claude-sonnet-4",
        "model_name": "Claude Sonnet 4",
        "provider": "Anthropic",
        "strengths": ["긴 컨텍스트 처리", "안전성", "지시 충실도"],
        "weaknesses": ["일부 기술적 작업에서 제한적 성능"]
      }
    ],
    "comparison_metrics": {
      "reasoning": {
        "gpt-4o": 9.2,
        "gpt-o3": 8.5,
        "claude-sonnet-4": 9.0
      },
      "creativity": {
        "gpt-4o": 8.8,
        "gpt-o3": 8.3,
        "claude-sonnet-4": 8.7
      },
      "instruction_following": {
        "gpt-4o": 9.0,
        "gpt-o3": 8.7,
        "claude-sonnet-4": 9.3
      }
    }
  }
}
```

## 오류 응답

모든 API 엔드포인트는 오류 발생 시 다음과 같은 형식으로 응답합니다:

```json
{
  "success": false,
  "error": "오류 메시지"
}
```

### 일반적인 오류 코드

- `400 Bad Request`: 잘못된 요청 형식 또는 필수 매개변수 누락
- `404 Not Found`: 요청한 리소스를 찾을 수 없음
- `405 Method Not Allowed`: 허용되지 않은 HTTP 메서드
- `500 Internal Server Error`: 서버 내부 오류

## 변경 이력

- **v1.0.0** (2025-05-27): 초기 API 릴리스
