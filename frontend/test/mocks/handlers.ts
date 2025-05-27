/**
 * MSW API 핸들러 정의
 * axios가 사용하는 API 엔드포인트를 모킹합니다.
 */

import { http, HttpResponse } from "msw";

// 모의 모델 데이터
const mockModels = [
  {
    model_id: "gpt-4o",
    model_name: "GPT-4o",
    provider: "OpenAI",
    category: "text",
    capabilities: ["text_generation", "conversation", "code_generation"],
    supports_multimodal: true,
  },
  {
    model_id: "imagen-3",
    model_name: "Imagen 3",
    provider: "Google",
    category: "image",
    capabilities: ["image_generation", "photorealistic_rendering"],
    supports_multimodal: false,
  },
  {
    model_id: "suno",
    model_name: "Suno",
    provider: "Suno",
    category: "music",
    capabilities: ["music_generation", "lyrics_generation"],
    supports_multimodal: false,
  },
];

// 모의 모델 팁 데이터
const mockModelTips = {
  "gpt-4o": [
    "자세한 지시사항을 제공하세요.",
    "단계별로 요청을 분리하세요.",
    "맥락을 충분히 제공하세요.",
  ],
  "imagen-3": [
    "사진의 주제를 명확히 설명하세요.",
    "원하는 구도를 자세히 설명하세요.",
    "원하는 스타일을 참조 이미지로 제공하세요.",
  ],
  suno: [
    "음악 장르를 명확히 지정하세요.",
    "템포와, 분위기를 설명하세요.",
    "인용할 아티스트 스타일을 언급하세요.",
  ],
};

export const handlers = [
  // GET /api/models 모킹
  http.get("http://localhost:5000/api/models", () => {
    return HttpResponse.json({
      success: true,
      models: mockModels,
    });
  }),

  // GET /api/model/:modelId/tips 모킹
  http.get("http://localhost:5000/api/model/:modelId/tips", ({ params }) => {
    const { modelId } = params;

    return HttpResponse.json({
      success: true,
      tips: mockModelTips[modelId as keyof typeof mockModelTips] || [],
    });
  }),

  // POST /api/optimize 모킹
  http.post("http://localhost:5000/api/optimize", async ({ request }) => {
    const body = (await request.json()) as {
      input_text: string;
      model_id: string;
    };

    return HttpResponse.json({
      success: true,
      original_input: body.input_text,
      optimized_prompt: `최적화된 프롬프트: ${body.input_text}`,
      model_id: body.model_id,
      model_info:
        mockModels.find((model) => model.model_id === body.model_id) || null,
      prompt_structure: {
        components: ["subject", "style", "details"],
        recommended_order: ["subject", "style", "details"],
      },
      generation_params: {
        quality: "high",
        format: "png",
      },
      analysis_result: {
        keywords: ["테스트", "프롬프트"],
        intent: "일반적인 질문",
      },
      intent_result: {
        primary_intent: "정보 요청",
        confidence: 0.95,
      },
    });
  }),

  // 오류 케이스 모킹
  http.post("http://localhost:5000/api/optimize-error", () => {
    return HttpResponse.json(
      {
        success: false,
        error: "모킹된 오류 메시지",
      },
      { status: 500 }
    );
  }),
];
