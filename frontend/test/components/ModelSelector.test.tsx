/**
 * ModelSelector 컴포넌트 테스트
 */

import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ModelSelector from "@/components/ModelSelector";

// Mock 데이터
const mockModels = [
  {
    model_id: "gpt-4o",
    model_name: "GPT-4o",
    provider: "OpenAI",
    capabilities: ["text_generation", "conversation", "code_generation"],
    supports_multimodal: true,
  },
  {
    model_id: "imagen-3",
    model_name: "Imagen 3",
    provider: "Google",
    capabilities: ["image_generation", "photorealistic_rendering"],
    supports_multimodal: false,
  },
  {
    model_id: "suno",
    model_name: "Suno",
    provider: "Suno",
    capabilities: ["music_generation", "lyrics_generation"],
    supports_multimodal: false,
  },
];

// Props 인터페이스 (실제 컴포넌트에서 정의된 것과 일치해야 함)
interface ModelSelectorProps {
  onModelSelect: (modelId: string) => void;
}

describe("ModelSelector 컴포넌트", () => {
  const defaultProps: ModelSelectorProps = {
    onModelSelect: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("기본 렌더링", () => {
    it("타이틀이 표시된다", () => {
      render(<ModelSelector {...defaultProps} />);
      expect(screen.getByText("AI 모델 선택")).toBeInTheDocument();
    });

    it("카테고리 탭이 표시된다", () => {
      render(<ModelSelector {...defaultProps} />);
      expect(screen.getByRole("tab", { name: "텍스트" })).toBeInTheDocument();
      expect(screen.getByRole("tab", { name: "이미지" })).toBeInTheDocument();
      expect(screen.getByRole("tab", { name: "비디오" })).toBeInTheDocument();
      expect(screen.getByRole("tab", { name: "음악" })).toBeInTheDocument();
    });
  });

  describe("상호작용", () => {
    it("카테고리 변경 시 해당 카테고리의 콘텐츠가 표시된다", async () => {
      render(<ModelSelector {...defaultProps} />);

      // 이미지 탭 클릭
      await userEvent.click(screen.getByRole("tab", { name: "이미지" }));

      // 이미지 탭의 내용이 표시되는지 확인
      expect(screen.getByRole("combobox")).toBeInTheDocument();
    });
  });

  describe("로딩 상태", () => {
    it("초기 로딩 중일 때 로딩 메시지가 표시된다", () => {
      render(<ModelSelector {...defaultProps} />);
      expect(
        screen.getByText("모델 목록을 불러오는 중...")
      ).toBeInTheDocument();
    });
  });

  describe("접근성", () => {
    it("선택된 탭이 올바르게 표시된다", () => {
      render(<ModelSelector {...defaultProps} />);
      const selectedTab = screen.getByRole("tab", { selected: true });
      expect(selectedTab).toHaveTextContent("텍스트");
    });
  });
});
