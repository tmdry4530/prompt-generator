"""
텍스트 생성 모델을 위한 프롬프트 템플릿 모듈
"""

from typing import Dict, List, Any

class TextPromptTemplate:
    """텍스트 생성 모델을 위한 프롬프트 템플릿 클래스"""
    
    @staticmethod
    def get_basic_template() -> Dict[str, Any]:
        """기본 텍스트 프롬프트 템플릿 반환"""
        return {
            "components": [
                "role_definition",
                "context_setting",
                "task_description",
                "specific_instructions",
                "output_format",
                "examples",
                "constraints"
            ],
            "recommended_order": [
                "role_definition",
                "context_setting",
                "task_description",
                "specific_instructions",
                "output_format",
                "examples",
                "constraints"
            ],
            "optional_components": [
                "examples",
                "constraints"
            ]
        }
    
    @staticmethod
    def get_system_role_templates() -> Dict[str, str]:
        """시스템 역할 템플릿 반환"""
        return {
            "creative_writing": "당신은 창의적인 작가로서 독창적이고 매력적인 콘텐츠를 생성하는 전문가입니다.",
            "technical_writing": "당신은 기술 문서 작성자로서 복잡한 개념을 명확하고 정확하게 설명하는 전문가입니다.",
            "marketing": "당신은 마케팅 전문가로서 설득력 있고 매력적인 카피를 작성하는 능력을 갖추고 있습니다.",
            "data_analysis": "당신은 데이터 분석가로서 정보를 체계적으로 분석하고 통찰력 있는 결론을 도출하는 전문가입니다.",
            "code_generation": "당신은 소프트웨어 개발자로서 효율적이고 잘 구조화된 코드를 작성하는 전문가입니다.",
            "academic": "당신은 학자로서 철저한 연구와 논리적 분석을 바탕으로 학술적 콘텐츠를 생성합니다.",
            "general": "당신은 지식이 풍부하고 도움이 되는 AI 어시스턴트입니다."
        }
    
    @staticmethod
    def get_output_format_templates() -> Dict[str, str]:
        """출력 형식 템플릿 반환"""
        return {
            "list": "다음 형식으로 응답해주세요:\n- 항목 1\n- 항목 2\n- 항목 3\n...",
            "table": "다음과 같은 표 형식으로 응답해주세요:\n| 열1 | 열2 | 열3 |\n|-----|-----|-----|\n| 값1 | 값2 | 값3 |",
            "json": "다음 JSON 형식으로 응답해주세요:\n```json\n{\n  \"key1\": \"value1\",\n  \"key2\": \"value2\"\n}\n```",
            "markdown": "마크다운 형식으로 응답해주세요. 제목, 부제목, 목록, 강조 등의 마크다운 요소를 적절히 활용하세요.",
            "step_by_step": "다음과 같이 단계별로 응답해주세요:\n1. 첫 번째 단계\n2. 두 번째 단계\n3. 세 번째 단계\n..."
        }
    
    @staticmethod
    def get_chain_of_thought_template() -> str:
        """사고 과정 (Chain of Thought) 템플릿 반환"""
        return (
            "이 작업을 수행하기 위해 단계별로 생각해 보겠습니다.\n\n"
            "1. 먼저 문제/요청을 정확히 이해하겠습니다.\n"
            "2. 필요한 정보와 접근 방식을 결정하겠습니다.\n"
            "3. 단계별로 해결책을 구성하겠습니다.\n"
            "4. 결과를 검증하고 마무리하겠습니다."
        )
    
    @staticmethod
    def get_context_setting_templates() -> Dict[str, str]:
        """맥락 설정 템플릿 반환"""
        return {
            "audience": {
                "general": "일반 대중을 대상으로 합니다.",
                "expert": "해당 분야 전문가를 대상으로 합니다.",
                "beginner": "입문자나 초보자를 대상으로 합니다.",
                "children": "어린이를 대상으로 합니다.",
                "teenager": "청소년을 대상으로 합니다.",
                "adult": "성인을 대상으로 합니다."
            },
            "style": {
                "formal": "격식적이고 전문적인 톤으로 작성합니다.",
                "casual": "친근하고 일상적인 톤으로 작성합니다.",
                "creative": "창의적이고 독창적인 톤으로 작성합니다.",
                "technical": "기술적이고 정확한 톤으로 작성합니다.",
                "persuasive": "설득력 있는 톤으로 작성합니다.",
                "informative": "정보 제공에 중점을 둔 톤으로 작성합니다.",
                "humorous": "유머러스한 톤으로 작성합니다.",
                "minimalist": "간결하고 핵심적인 톤으로 작성합니다."
            }
        }
    
    @staticmethod
    def get_zero_shot_template(task: str) -> str:
        """제로샷 프롬프팅 템플릿 반환"""
        return f"다음 작업을 수행해주세요: {task}"
    
    @staticmethod
    def get_few_shot_template(task: str, examples: List[Dict[str, str]]) -> str:
        """퓨샷 프롬프팅 템플릿 반환"""
        template = f"다음 작업을 수행해주세요: {task}\n\n다음은 몇 가지 예시입니다:\n\n"
        
        for i, example in enumerate(examples, 1):
            template += f"예시 {i}:\n"
            template += f"입력: {example.get('input', '')}\n"
            template += f"출력: {example.get('output', '')}\n\n"
        
        template += "위 예시들과 같은 방식으로 작업을 수행해주세요."
        return template 