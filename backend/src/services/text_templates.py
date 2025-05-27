"""
텍스트 모델용 프롬프트 템플릿: 텍스트 기반 AI 모델을 위한 프롬프트 템플릿을 제공합니다.
"""

from typing import Dict, Any, List

class TextTemplates:
    """텍스트 기반 AI 모델을 위한 프롬프트 템플릿 클래스"""
    
    @staticmethod
    def get_role_template(role_type: str) -> str:
        """
        역할 유형에 따른 템플릿을 반환합니다.
        
        Args:
            role_type: 역할 유형 (creative_writing, technical_writing 등)
            
        Returns:
            역할 템플릿 문자열
        """
        templates = {
            "creative_writing": "당신은 창의적인 작가로서 독창적이고 매력적인 콘텐츠를 생성하는 전문가입니다.",
            "technical_writing": "당신은 기술 문서 작성자로서 복잡한 개념을 명확하고 정확하게 설명하는 전문가입니다.",
            "marketing": "당신은 마케팅 전문가로서 설득력 있고 매력적인 카피를 작성하는 능력을 갖추고 있습니다.",
            "data_analysis": "당신은 데이터 분석가로서 정보를 체계적으로 분석하고 통찰력 있는 결론을 도출하는 전문가입니다.",
            "code_generation": "당신은 소프트웨어 개발자로서 효율적이고 잘 구조화된 코드를 작성하는 전문가입니다.",
            "academic": "당신은 학자로서 철저한 연구와 논리적 분석을 바탕으로 학술적 콘텐츠를 생성합니다.",
            "general": "당신은 지식이 풍부하고 도움이 되는 AI 어시스턴트입니다."
        }
        
        return templates.get(role_type, templates["general"])
    
    @staticmethod
    def get_task_template(task_type: str) -> str:
        """
        작업 유형에 따른 템플릿을 반환합니다.
        
        Args:
            task_type: 작업 유형 (generate_content, analyze 등)
            
        Returns:
            작업 템플릿 문자열
        """
        templates = {
            "generate_content": "다음 내용을 생성해주세요:",
            "analyze": "다음 내용을 분석해주세요:",
            "summarize": "다음 내용을 요약해주세요:",
            "explain": "다음 내용을 설명해주세요:",
            "translate": "다음 내용을 번역해주세요:",
            "compare": "다음 내용을 비교해주세요:",
            "improve": "다음 내용을 개선해주세요:",
            "brainstorm": "다음 주제에 대한 아이디어를 제시해주세요:",
            "question": "다음 질문에 답변해주세요:"
        }
        
        return templates.get(task_type, "작업:")
    
    @staticmethod
    def get_output_format_template(format_type: str) -> str:
        """
        출력 형식에 따른 템플릿을 반환합니다.
        
        Args:
            format_type: 출력 형식 유형 (list, table 등)
            
        Returns:
            출력 형식 템플릿 문자열
        """
        templates = {
            "list": "다음 형식으로 응답해주세요:\n- 항목 1\n- 항목 2\n- 항목 3\n...",
            "table": "다음과 같은 표 형식으로 응답해주세요:\n| 열1 | 열2 | 열3 |\n|-----|-----|-----|\n| 값1 | 값2 | 값3 |",
            "json": "다음 JSON 형식으로 응답해주세요:\n```json\n{\n  \"key1\": \"value1\",\n  \"key2\": \"value2\"\n}\n```",
            "markdown": "마크다운 형식으로 응답해주세요. 제목, 부제목, 목록, 강조 등의 마크다운 요소를 적절히 활용하세요.",
            "step_by_step": "다음과 같이 단계별로 응답해주세요:\n1. 첫 번째 단계\n2. 두 번째 단계\n3. 세 번째 단계\n..."
        }
        
        return templates.get(format_type, "")
    
    @staticmethod
    def get_complexity_template(complexity_level: str) -> str:
        """
        복잡성 수준에 따른 템플릿을 반환합니다.
        
        Args:
            complexity_level: 복잡성 수준 (high, medium, low)
            
        Returns:
            복잡성 템플릿 문자열
        """
        templates = {
            "high": "상세하고 포괄적인 내용을 제공해주세요.",
            "medium": "적절한 상세 수준으로 균형 잡힌 내용을 제공해주세요.",
            "low": "간결하고 핵심적인 내용만 제공해주세요."
        }
        
        return templates.get(complexity_level, templates["medium"])
    
    @staticmethod
    def get_tone_template(tone_type: str) -> str:
        """
        톤/어조에 따른 템플릿을 반환합니다.
        
        Args:
            tone_type: 톤/어조 유형 (professional, friendly 등)
            
        Returns:
            톤/어조 템플릿 문자열
        """
        templates = {
            "professional": "전문적이고 격식 있는 톤을 유지해주세요.",
            "friendly": "친근하고 우호적인 톤을 유지해주세요.",
            "formal": "공식적이고 격식 있는 톤을 유지해주세요.",
            "informal": "비격식적이고 편안한 톤을 유지해주세요.",
            "enthusiastic": "열정적이고 활기찬 톤을 유지해주세요.",
            "serious": "진지하고 엄숙한 톤을 유지해주세요.",
            "humorous": "유머러스하고 재미있는 톤을 유지해주세요."
        }
        
        return templates.get(tone_type, "")
    
    @staticmethod
    def get_audience_template(audience_type: str) -> str:
        """
        대상 독자에 따른 템플릿을 반환합니다.
        
        Args:
            audience_type: 대상 독자 유형 (general, expert 등)
            
        Returns:
            대상 독자 템플릿 문자열
        """
        templates = {
            "general": "일반 대중을 대상으로 작성해주세요.",
            "expert": "해당 분야 전문가를 대상으로 작성해주세요.",
            "beginner": "입문자나 초보자를 대상으로 작성해주세요.",
            "children": "어린이를 대상으로 작성해주세요.",
            "teenager": "청소년을 대상으로 작성해주세요.",
            "adult": "성인을 대상으로 작성해주세요."
        }
        
        return templates.get(audience_type, "")
    
    @staticmethod
    def get_style_template(style_type: str) -> str:
        """
        스타일에 따른 템플릿을 반환합니다.
        
        Args:
            style_type: 스타일 유형 (formal, casual 등)
            
        Returns:
            스타일 템플릿 문자열
        """
        templates = {
            "formal": "격식적이고 전문적인 스타일로 작성해주세요.",
            "casual": "친근하고 일상적인 스타일로 작성해주세요.",
            "creative": "창의적이고 독창적인 스타일로 작성해주세요.",
            "technical": "기술적이고 정확한 스타일로 작성해주세요.",
            "persuasive": "설득력 있는 스타일로 작성해주세요.",
            "informative": "정보 제공에 중점을 둔 스타일로 작성해주세요.",
            "humorous": "유머러스한 스타일로 작성해주세요.",
            "minimalist": "간결하고 핵심적인 스타일로 작성해주세요."
        }
        
        return templates.get(style_type, "")
    
    @staticmethod
    def get_urgency_template(urgency_level: str) -> str:
        """
        긴급성 수준에 따른 템플릿을 반환합니다.
        
        Args:
            urgency_level: 긴급성 수준 (high, medium, low)
            
        Returns:
            긴급성 템플릿 문자열
        """
        templates = {
            "high": "이 작업은 매우 긴급합니다. 가능한 빨리 핵심적인 정보를 제공해주세요.",
            "medium": "이 작업은 적당히 긴급합니다. 불필요한 세부사항은 생략해주세요.",
            "low": ""
        }
        
        return templates.get(urgency_level, "")
