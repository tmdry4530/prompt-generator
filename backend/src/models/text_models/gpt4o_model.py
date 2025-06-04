"""
GPT-4o 모델 최적화 모듈: GPT-4o 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class GPT4oModel(BaseModel):
    """
    GPT-4o 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """GPT-4o 모델 클래스 초기화"""
        super().__init__(
            model_id="gpt-4o",
            model_name="GPT-4o",
            provider="OpenAI"
        )
        self.capabilities = [
            "text_generation",
            "code_generation",
            "creative_writing",
            "analytical_reasoning",
            "multimodal_understanding",
            "tool_use"
        ]
        self.max_tokens = 128000  # 128K 컨텍스트 길이
        self.supports_multimodal = True
        self.best_practices = [
            "명확한 지시와 맥락 제공",
            "역할 부여를 통한 전문성 유도",
            "단계별 지시로 복잡한 작업 분해",
            "출력 형식 명확히 지정",
            "멀티모달 입력 활용"
        ]
        
        # GPT-4o에 최적화된 역할 템플릿
        self.role_templates = {
            "creative_writing": "당신은 창의적인 작가로서 독창적이고 매력적인 콘텐츠를 생성하는 전문가입니다.",
            "technical_writing": "당신은 기술 문서 작성자로서 복잡한 개념을 명확하고 정확하게 설명하는 전문가입니다.",
            "marketing": "당신은 마케팅 전문가로서 설득력 있고 매력적인 카피를 작성하는 능력을 갖추고 있습니다.",
            "data_analysis": "당신은 데이터 분석가로서 정보를 체계적으로 분석하고 통찰력 있는 결론을 도출하는 전문가입니다.",
            "code_generation": "당신은 소프트웨어 개발자로서 효율적이고 잘 구조화된 코드를 작성하는 전문가입니다.",
            "academic": "당신은 학자로서 철저한 연구와 논리적 분석을 바탕으로 학술적 콘텐츠를 생성합니다.",
            "general": "당신은 지식이 풍부하고 도움이 되는 AI 어시스턴트입니다."
        }
        
        # 출력 형식 템플릿
        self.output_format_templates = {
            "list": "다음 형식으로 응답해주세요:\n- 항목 1\n- 항목 2\n- 항목 3\n...",
            "table": "다음과 같은 표 형식으로 응답해주세요:\n| 열1 | 열2 | 열3 |\n|-----|-----|-----|\n| 값1 | 값2 | 값3 |",
            "json": "다음 JSON 형식으로 응답해주세요:\n```json\n{\n  \"key1\": \"value1\",\n  \"key2\": \"value2\"\n}\n```",
            "markdown": "마크다운 형식으로 응답해주세요. 제목, 부제목, 목록, 강조 등의 마크다운 요소를 적절히 활용하세요.",
            "step_by_step": "다음과 같이 단계별로 응답해주세요:\n1. 첫 번째 단계\n2. 두 번째 단계\n3. 세 번째 단계\n..."
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        GPT-4o 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
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
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 GPT-4o에 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        # 1. 역할 정의 생성
        role = self._generate_role(analysis_result, intent_result)
        
        # 2. 맥락 설정 생성
        context = self._generate_context(analysis_result, intent_result)
        
        # 3. 작업 설명 생성
        task = self._generate_task(analysis_result, intent_result)
        
        # 4. 구체적인 지시사항 생성
        instructions = self._generate_instructions(analysis_result, intent_result)
        
        # 5. 출력 형식 생성
        output_format = self._generate_output_format(analysis_result, intent_result)
        
        # 6. 제약 조건 생성
        constraints = self._generate_constraints(analysis_result, intent_result)
        
        # 7. 최종 프롬프트 조합
        prompt_parts = [role]
        
        if context:
            prompt_parts.append(context)
            
        prompt_parts.append(task)
        
        if instructions:
            prompt_parts.append(instructions)
            
        if output_format:
            prompt_parts.append(output_format)
            
        if constraints:
            prompt_parts.append(constraints)
        
        # 최종 프롬프트 생성
        optimized_prompt = "\n\n".join(filter(None, prompt_parts))
        
        # 공통 규칙 적용
        optimized_prompt = self.apply_common_rules(optimized_prompt)
        
        return optimized_prompt
    
    def _generate_role(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """역할 정의를 생성합니다."""
        # 작업 유형에 따른 역할 선택
        task_types = analysis_result.get("task_type", [])
        
        if not task_types:
            return self.role_templates["general"]
        
        # 첫 번째 작업 유형 기준으로 역할 선택
        task_type = task_types[0][0] if isinstance(task_types[0], tuple) else task_types[0]
        
        # 해당 작업 유형에 맞는 역할 템플릿 선택
        role = self.role_templates.get(task_type, self.role_templates["general"])
        
        # 특정 의도에 따른 역할 조정
        if intent_result.get("is_creative", False):
            role = self.role_templates["creative_writing"]
        elif intent_result.get("is_technical", False):
            role = self.role_templates["technical_writing"]
        
        return role
    
    def _generate_context(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """맥락 설정을 생성합니다."""
        context_parts = []
        
        # 대상 독자 정보가 있으면 추가
        audience = analysis_result.get("constraints", {}).get("audience")
        if audience:
            audience_map = {
                "general": "일반 대중",
                "expert": "해당 분야 전문가",
                "beginner": "입문자나 초보자",
                "children": "어린이",
                "teenager": "청소년",
                "adult": "성인"
            }
            audience_text = audience_map.get(audience, audience)
            context_parts.append(f"대상 독자는 {audience_text}입니다.")
        
        # 스타일 정보가 있으면 추가
        styles = analysis_result.get("style", [])
        if styles and isinstance(styles[0], tuple):
            style = styles[0][0]
            style_map = {
                "formal": "격식적이고 전문적인",
                "casual": "친근하고 일상적인",
                "creative": "창의적이고 독창적인",
                "technical": "기술적이고 정확한",
                "persuasive": "설득력 있는",
                "informative": "정보 제공에 중점을 둔",
                "humorous": "유머러스한",
                "minimalist": "간결하고 핵심적인"
            }
            style_text = style_map.get(style, style)
            context_parts.append(f"스타일은 {style_text} 톤으로 작성해주세요.")
        
        # 맥락 정보 조합
        if context_parts:
            return "맥락: " + " ".join(context_parts)
        
        return ""
    
    def _generate_task(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """작업 설명을 생성합니다."""
        # 기본 작업 설명
        input_text = analysis_result.get("input_text", "")
        
        # 의도에 따른 작업 설명 조정
        primary_intent = intent_result.get("primary_intent", ("generate_content", 0.5))
        
        if isinstance(primary_intent, tuple):
            intent_type = primary_intent[0]
        else:
            intent_type = primary_intent
            
        intent_prefix_map = {
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
        
        task_prefix = intent_prefix_map.get(intent_type, "작업:")
        
        return f"{task_prefix} {input_text}"
    
    def _generate_instructions(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """구체적인 지시사항을 생성합니다."""
        instruction_parts = []
        
        # 복잡성에 따른 지시사항 조정
        complexity = analysis_result.get("complexity", "medium")
        if complexity == "high":
            instruction_parts.append("상세하고 포괄적인 내용을 제공해주세요.")
        elif complexity == "low":
            instruction_parts.append("간결하고 핵심적인 내용만 제공해주세요.")
        
        # 구조 힌트에 따른 지시사항 추가
        structure_hints = analysis_result.get("structure_hints", {})
        
        # 길이 지시사항
        if "word_count" in structure_hints:
            instruction_parts.append(f"약 {structure_hints['word_count']}단어 내외로 작성해주세요.")
        elif "sentence_count" in structure_hints:
            instruction_parts.append(f"약 {structure_hints['sentence_count']}문장 내외로 작성해주세요.")
        elif "length" in structure_hints and structure_hints["length"]:
            length_map = {
                "short": "짧고 간결하게",
                "medium": "적절한 길이로",
                "long": "상세하고 포괄적으로"
            }
            instruction_parts.append(f"{length_map.get(structure_hints['length'], '')} 작성해주세요.")
        
        # 섹션 지시사항
        if "sections" in structure_hints and structure_hints["sections"]:
            sections_text = ", ".join(structure_hints["sections"])
            instruction_parts.append(f"다음 섹션을 포함해주세요: {sections_text}")
        
        # 포함해야 할 요소 추가
        constraints = analysis_result.get("constraints", {})
        if "include" in constraints and constraints["include"]:
            includes_text = ", ".join(constraints["include"])
            instruction_parts.append(f"다음 요소를 반드시 포함해주세요: {includes_text}")
        
        # 제외해야 할 요소 추가
        if "exclude" in constraints and constraints["exclude"]:
            excludes_text = ", ".join(constraints["exclude"])
            instruction_parts.append(f"다음 요소는 제외해주세요: {excludes_text}")
        
        # 지시사항 조합
        if instruction_parts:
            return "지시사항:\n- " + "\n- ".join(instruction_parts)
        
        return ""
    
    def _generate_output_format(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """출력 형식을 생성합니다."""
        # 구조 힌트에서 형식 정보 추출
        structure_hints = analysis_result.get("structure_hints", {})
        format_type = structure_hints.get("format")
        
        # 의도에서 출력 형식 정보 추출
        if not format_type:
            format_type = intent_result.get("output_format")
        
        # 형식 템플릿 선택
        if format_type and format_type in self.output_format_templates:
            return f"출력 형식: {self.output_format_templates[format_type]}"
        
        return ""
    
    def _generate_constraints(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """제약 조건을 생성합니다."""
        constraint_parts = []
        
        # 톤/어조 제약 추가
        constraints = analysis_result.get("constraints", {})
        if "tone" in constraints and constraints["tone"]:
            tone_map = {
                "professional": "전문적이고 격식 있는",
                "friendly": "친근하고 우호적인",
                "formal": "공식적이고 격식 있는",
                "informal": "비격식적이고 편안한",
                "enthusiastic": "열정적이고 활기찬",
                "serious": "진지하고 엄숙한",
                "humorous": "유머러스하고 재미있는"
            }
            constraint_parts.append(f"{tone_map.get(constraints['tone'], constraints['tone'])} 톤을 유지해주세요.")
        
        # 시간 제약 추가
        if "time_constraint" in constraints and constraints["time_constraint"]:
            constraint_parts.append(f"이 작업은 {constraints['time_constraint']} 내에 완료되어야 합니다.")
        
        # 긴급성 수준에 따른 제약 추가
        urgency_level = intent_result.get("urgency_level", "low")
        if urgency_level == "high":
            constraint_parts.append("이 작업은 매우 긴급합니다. 가능한 빨리 핵심적인 정보를 제공해주세요.")
        elif urgency_level == "medium":
            constraint_parts.append("이 작업은 적당히 긴급합니다. 불필요한 세부사항은 생략해주세요.")
        
        # 제약 조건 조합
        if constraint_parts:
            return "제약 조건:\n- " + "\n- ".join(constraint_parts)
        
        return ""
    
    def apply_common_rules(self, prompt: str) -> str:
        """
        GPT-4o에 최적화된 공통 규칙을 프롬프트에 적용합니다.
        
        Args:
            prompt: 원본 프롬프트
            
        Returns:
            규칙이 적용된 프롬프트
        """
        # 1. 불필요한 공백 제거
        prompt = re.sub(r'\n{3,}', '\n\n', prompt)
        
        # 2. 마지막에 불필요한 마침표 제거
        prompt = re.sub(r'\.+$', '', prompt)
        
        # 3. 프롬프트가 너무 길면 핵심 부분만 유지
        if len(prompt) > 4000:
            # 간단한 요약 로직 (실제로는 더 복잡한 요약 알고리즘 사용 가능)
            lines = prompt.split('\n')
            if len(lines) > 50:
                # 처음 10줄, 마지막 10줄, 그리고 중간에 30줄 정도만 유지
                prompt = '\n'.join(lines[:10] + ['...'] + lines[len(lines)//2-15:len(lines)//2+15] + ['...'] + lines[-10:])
        
        return prompt
    
    def get_capability_specific_tips(self, capability: str) -> List[str]:
        """
        특정 기능에 대한 GPT-4o 최적화 팁을 반환합니다.
        
        Args:
            capability: 기능 이름
            
        Returns:
            최적화 팁 목록
        """
        tips = {
            "text_generation": [
                "명확한 출력 형식을 지정하면 더 일관된 결과를 얻을 수 있습니다.",
                "역할 부여를 통해 특정 전문성을 가진 응답을 유도할 수 있습니다.",
                "단계별 지시를 사용하면 복잡한 작업을 더 잘 처리할 수 있습니다."
            ],
            "code_generation": [
                "원하는 프로그래밍 언어를 명시적으로 지정하세요.",
                "코드의 목적과 기능을 상세히 설명하세요.",
                "예상 입출력 예제를 제공하면 더 정확한 코드를 생성할 수 있습니다.",
                "코드 스타일이나 특정 패턴에 대한 요구사항을 명시하세요."
            ],
            "creative_writing": [
                "원하는 글의 분위기, 톤, 스타일을 구체적으로 지정하세요.",
                "캐릭터, 설정, 플롯 등의 요소를 상세히 설명하세요.",
                "특정 장르나 작가의 스타일을 참조하면 더 특화된 결과를 얻을 수 있습니다."
            ],
            "analytical_reasoning": [
                "분석해야 할 데이터나 문제를 명확히 정의하세요.",
                "원하는 분석 방법이나 프레임워크를 지정하세요.",
                "결론이나 통찰을 어떤 형태로 제시할지 명시하세요."
            ],
            "multimodal_understanding": [
                "이미지와 텍스트를 함께 제공할 때는 이미지에 대한 질문이나 지시를 구체적으로 작성하세요.",
                "이미지의 특정 부분에 대해 언급할 때는 위치나 특징을 명확히 설명하세요.",
                "이미지와 텍스트 간의 관계를 명확히 설명하면 더 정확한 이해를 유도할 수 있습니다."
            ],
            "tool_use": [
                "GPT-4o가 사용할 수 있는 도구의 기능과 제한사항을 명확히 설명하세요.",
                "도구 사용의 목적과 원하는 결과를 구체적으로 지정하세요.",
                "여러 도구를 순차적으로 사용해야 하는 경우, 각 단계를 명확히 설명하세요."
            ]
        }
        
        return tips.get(capability, ["GPT-4o는 다양한 작업에 활용할 수 있는 범용 모델입니다."])
