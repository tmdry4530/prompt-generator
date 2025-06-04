"""
GPT-o3 모델 최적화 모듈: GPT-o3 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class GPTo3Model(BaseModel):
    """
    GPT-o3 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """GPT-o3 모델 클래스 초기화"""
        super().__init__(
            model_id="gpt-o3",
            model_name="GPT-o3",
            provider="OpenAI"
        )
        self.capabilities = [
            "reasoning",
            "math_problem_solving",
            "code_generation",
            "technical_writing",
            "multimodal_understanding",
            "tool_use"
        ]
        self.max_tokens = 200000  # 200K 컨텍스트 길이
        self.supports_multimodal = True
        self.best_practices = [
            "다단계 추론 문제에 최적화된 프롬프트 작성",
            "멀티모달 입력 활용",
            "기술적 글쓰기 및 코딩 작업에 적합한 구조화",
            "긴 컨텍스트 효과적 활용",
            "도구 사용 기능 최적화"
        ]
        
        # GPT-o3에 최적화된 역할 템플릿
        self.role_templates = {
            "reasoning": "당신은 복잡한 추론 문제를 단계별로 해결하는 전문가입니다.",
            "math_problem_solving": "당신은 수학 문제를 체계적으로 분석하고 해결하는 전문가입니다.",
            "code_generation": "당신은 효율적이고 잘 구조화된 코드를 작성하는 소프트웨어 개발 전문가입니다.",
            "technical_writing": "당신은 복잡한 기술적 개념을 명확하고 정확하게 설명하는 기술 문서 작성 전문가입니다.",
            "multimodal_analysis": "당신은 텍스트와 이미지 정보를 통합하여 분석하는 멀티모달 분석 전문가입니다.",
            "general": "당신은 추론 능력이 뛰어난 AI 어시스턴트입니다."
        }
        
        # 출력 형식 템플릿
        self.output_format_templates = {
            "step_by_step": "다음과 같이 단계별로 추론 과정을 보여주세요:\n1. 첫 번째 단계: [추론]\n2. 두 번째 단계: [추론]\n...\n최종 결론: [결론]",
            "math_solution": "다음 형식으로 수학 문제 풀이를 제시해주세요:\n문제 이해: [문제 분석]\n접근 방법: [해결 전략]\n풀이 과정:\n[단계별 수식 및 설명]\n최종 답: [결과]",
            "code_with_explanation": "다음 형식으로 코드와 설명을 제공해주세요:\n```[언어]\n[코드]\n```\n\n코드 설명:\n- [주요 부분 설명]\n- [알고리즘 설명]\n- [사용된 기법 설명]",
            "technical_document": "다음 구조로 기술 문서를 작성해주세요:\n## 개요\n[간략한 설명]\n\n## 주요 개념\n[핵심 개념 설명]\n\n## 세부 내용\n[상세 설명]\n\n## 결론\n[요약 및 결론]",
            "multimodal_analysis": "다음 구조로 멀티모달 분석을 제공해주세요:\n## 시각적 요소 분석\n[이미지 내용 분석]\n\n## 텍스트 요소 분석\n[텍스트 내용 분석]\n\n## 통합 분석\n[시각 및 텍스트 정보 통합 분석]\n\n## 결론\n[최종 결론]"
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        GPT-o3 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        return {
            "components": [
                "role_definition",
                "problem_statement",
                "reasoning_approach",
                "step_by_step_instructions",
                "output_format",
                "intermediate_results_request",
                "examples",
                "constraints"
            ],
            "recommended_order": [
                "role_definition",
                "problem_statement",
                "reasoning_approach",
                "step_by_step_instructions",
                "output_format",
                "intermediate_results_request",
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
        분석 결과와 의도 결과를 기반으로 GPT-o3에 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        # 1. 역할 정의 생성
        role = self._generate_role(analysis_result, intent_result)
        
        # 2. 문제 설명 생성
        problem = self._generate_problem(analysis_result, intent_result)
        
        # 3. 추론 접근법 생성
        approach = self._generate_approach(analysis_result, intent_result)
        
        # 4. 단계별 지시사항 생성
        instructions = self._generate_instructions(analysis_result, intent_result)
        
        # 5. 출력 형식 생성
        output_format = self._generate_output_format(analysis_result, intent_result)
        
        # 6. 중간 결과 요청 생성
        intermediate_results = self._generate_intermediate_results(analysis_result, intent_result)
        
        # 7. 제약 조건 생성
        constraints = self._generate_constraints(analysis_result, intent_result)
        
        # 8. 최종 프롬프트 조합
        prompt_parts = [role]
        
        if problem:
            prompt_parts.append(problem)
            
        if approach:
            prompt_parts.append(approach)
            
        if instructions:
            prompt_parts.append(instructions)
            
        if output_format:
            prompt_parts.append(output_format)
            
        if intermediate_results:
            prompt_parts.append(intermediate_results)
            
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
        if intent_result.get("is_math_problem", False):
            role = self.role_templates["math_problem_solving"]
        elif intent_result.get("is_technical", False):
            role = self.role_templates["technical_writing"]
        elif intent_result.get("is_coding", False):
            role = self.role_templates["code_generation"]
        
        return role
    
    def _generate_problem(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """문제 설명을 생성합니다."""
        # 기본 문제 설명
        input_text = analysis_result.get("input_text", "")
        
        # 의도에 따른 문제 설명 조정
        primary_intent = intent_result.get("primary_intent", ("solve_problem", 0.5))
        
        if isinstance(primary_intent, tuple):
            intent_type = primary_intent[0]
        else:
            intent_type = primary_intent
            
        intent_prefix_map = {
            "solve_problem": "다음 문제를 해결해주세요:",
            "analyze": "다음 내용을 분석해주세요:",
            "explain": "다음 개념을 설명해주세요:",
            "code": "다음 코드 작업을 수행해주세요:",
            "math": "다음 수학 문제를 풀어주세요:",
            "reason": "다음 상황에 대해 추론해주세요:"
        }
        
        problem_prefix = intent_prefix_map.get(intent_type, "문제:")
        
        return f"{problem_prefix}\n\n{input_text}"
    
    def _generate_approach(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """추론 접근법을 생성합니다."""
        approach_parts = []
        
        # 작업 유형에 따른 접근법 조정
        task_types = analysis_result.get("task_type", [])
        if task_types:
            task_type = task_types[0][0] if isinstance(task_types[0], tuple) else task_types[0]
            
            if task_type == "reasoning":
                approach_parts.append("이 문제를 해결하기 위해 단계별 추론 접근법을 사용해주세요.")
            elif task_type == "math_problem_solving":
                approach_parts.append("이 수학 문제를 해결하기 위해 체계적인 접근법을 사용하고, 각 단계에서의 수식과 계산을 명확히 보여주세요.")
            elif task_type == "code_generation":
                approach_parts.append("이 코딩 작업을 위해 먼저 문제를 분석하고, 알고리즘을 설계한 후, 효율적인 코드를 작성해주세요.")
        
        # 복잡성에 따른 접근법 조정
        complexity = analysis_result.get("complexity", "medium")
        if complexity == "high":
            approach_parts.append("이 복잡한 문제는 여러 하위 문제로 나누어 접근하는 것이 효과적입니다.")
        
        # 접근법 조합
        if approach_parts:
            return "접근법: " + " ".join(approach_parts)
        
        return "이 문제를 해결하기 위해 단계별로 생각해보세요."
    
    def _generate_instructions(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """단계별 지시사항을 생성합니다."""
        instruction_parts = []
        
        # 작업 유형에 따른 지시사항 조정
        task_types = analysis_result.get("task_type", [])
        if task_types:
            task_type = task_types[0][0] if isinstance(task_types[0], tuple) else task_types[0]
            
            if task_type == "reasoning":
                instruction_parts.append("1. 문제를 명확히 정의하세요.")
                instruction_parts.append("2. 관련된 개념과 원칙을 식별하세요.")
                instruction_parts.append("3. 단계별로 추론 과정을 전개하세요.")
                instruction_parts.append("4. 각 단계에서 중간 결론을 도출하세요.")
                instruction_parts.append("5. 최종 결론에 도달하세요.")
            elif task_type == "math_problem_solving":
                instruction_parts.append("1. 문제에서 주어진 조건과 구해야 할 것을 명확히 하세요.")
                instruction_parts.append("2. 적용할 수학적 개념이나 공식을 선택하세요.")
                instruction_parts.append("3. 단계별로 수식을 전개하고 계산하세요.")
                instruction_parts.append("4. 중간 결과를 검증하세요.")
                instruction_parts.append("5. 최종 답을 도출하고 단위를 명시하세요.")
            elif task_type == "code_generation":
                instruction_parts.append("1. 문제 요구사항을 분석하세요.")
                instruction_parts.append("2. 적절한 알고리즘과 자료구조를 선택하세요.")
                instruction_parts.append("3. 의사코드로 로직을 먼저 설계하세요.")
                instruction_parts.append("4. 실제 코드를 작성하고 주석을 추가하세요.")
                instruction_parts.append("5. 코드의 시간 및 공간 복잡도를 분석하세요.")
        
        # 지시사항 조합
        if instruction_parts:
            return "지시사항:\n" + "\n".join(instruction_parts)
        
        return ""
    
    def _generate_output_format(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """출력 형식을 생성합니다."""
        # 작업 유형에 따른 출력 형식 선택
        task_types = analysis_result.get("task_type", [])
        if not task_types:
            return ""
            
        task_type = task_types[0][0] if isinstance(task_types[0], tuple) else task_types[0]
        
        # 형식 템플릿 선택
        format_map = {
            "reasoning": "step_by_step",
            "math_problem_solving": "math_solution",
            "code_generation": "code_with_explanation",
            "technical_writing": "technical_document",
            "multimodal_analysis": "multimodal_analysis"
        }
        
        format_type = format_map.get(task_type, "step_by_step")
        
        if format_type in self.output_format_templates:
            return f"출력 형식: {self.output_format_templates[format_type]}"
        
        return ""
    
    def _generate_intermediate_results(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """중간 결과 요청을 생성합니다."""
        # 작업 유형에 따른 중간 결과 요청 조정
        task_types = analysis_result.get("task_type", [])
        if not task_types:
            return ""
            
        task_type = task_types[0][0] if isinstance(task_types[0], tuple) else task_types[0]
        
        if task_type == "reasoning" or task_type == "math_problem_solving":
            return "각 추론 단계에서 중간 결과를 명확히 보여주고, 다음 단계로 넘어가기 전에 현재까지의 결론을 요약해주세요."
        elif task_type == "code_generation":
            return "코드의 주요 부분마다 의도와 동작 방식을 설명하고, 함수나 모듈이 완성될 때마다 그 기능을 요약해주세요."
        
        return ""
    
    def _generate_constraints(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """제약 조건을 생성합니다."""
        constraint_parts = []
        
        # 정확성 요구사항 추가
        constraints = analysis_result.get("constraints", {})
        if "accuracy" in constraints and constraints["accuracy"] == "high":
            constraint_parts.append("모든 계산과 추론 과정에서 높은 정확도를 유지해주세요.")
        
        # 복잡성에 따른 제약 추가
        complexity = analysis_result.get("complexity", "medium")
        if complexity == "high":
            constraint_parts.append("복잡한 문제이므로 충분한 세부 사항과 설명을 제공해주세요.")
        elif complexity == "low":
            constraint_parts.append("간결하고 핵심적인 해결 과정만 제시해주세요.")
        
        # 제약 조건 조합
        if constraint_parts:
            return "제약 조건:\n- " + "\n- ".join(constraint_parts)
        
        return ""
    
    def apply_common_rules(self, prompt: str) -> str:
        """
        GPT-o3에 최적화된 공통 규칙을 프롬프트에 적용합니다.
        
        Args:
            prompt: 원본 프롬프트
            
        Returns:
            규칙이 적용된 프롬프트
        """
        # 1. 불필요한 공백 제거
        prompt = re.sub(r'\n{3,}', '\n\n', prompt)
        
        # 2. 단계별 사고 유도 문구 추가
        if "단계별" not in prompt and "step by step" not in prompt.lower():
            prompt += "\n\n단계별로 생각해보세요."
        
        # 3. 프롬프트가 너무 길면 핵심 부분만 유지
        if len(prompt) > 8000:  # GPT-o3는 더 긴 컨텍스트를 처리할 수 있음
            # 간단한 요약 로직 (실제로는 더 복잡한 요약 알고리즘 사용 가능)
            lines = prompt.split('\n')
            if len(lines) > 100:
                # 처음 20줄, 마지막 20줄, 그리고 중간에 60줄 정도만 유지
                prompt = '\n'.join(lines[:20] + ['...'] + lines[len(lines)//2-30:len(lines)//2+30] + ['...'] + lines[-20:])
        
        return prompt
    
    def get_capability_specific_tips(self, capability: str) -> List[str]:
        """
        특정 기능에 대한 GPT-o3 최적화 팁을 반환합니다.
        
        Args:
            capability: 기능 이름
            
        Returns:
            최적화 팁 목록
        """
        tips = {
            "reasoning": [
                "문제를 여러 하위 문제로 분해하여 단계별로 접근하세요.",
                "각 추론 단계에서 중간 결과를 명시적으로 요청하세요.",
                "추론 과정에서 사용하는 가정이나 원칙을 명확히 언급하세요.",
                "복잡한 추론 체인에서는 '단계별로 생각해보세요'라는 지시어를 포함하세요."
            ],
            "math_problem_solving": [
                "수학 문제의 조건과 구해야 할 것을 명확히 구분하여 제시하세요.",
                "적용해야 할 수학적 개념이나 공식을 언급하세요.",
                "계산 과정을 단계별로 보여달라고 요청하세요.",
                "최종 답변 뿐만 아니라 중간 계산 결과도 확인하세요."
            ],
            "code_generation": [
                "원하는 프로그래밍 언어와 버전을 명시하세요.",
                "코드의 목적과 기능 요구사항을 상세히 설명하세요.",
                "예상 입출력 예제를 제공하세요.",
                "코드 설명과 주석을 요청하세요.",
                "시간 및 공간 복잡도 분석을 요청하세요."
            ],
            "technical_writing": [
                "대상 독자의 전문성 수준을 명시하세요.",
                "포함해야 할 주요 섹션이나 주제를 나열하세요.",
                "기술 문서의 목적(설명, 지침, 참조 등)을 명확히 하세요.",
                "원하는 형식이나 스타일 가이드를 언급하세요."
            ],
            "multimodal_understanding": [
                "이미지와 텍스트를 함께 제공할 때는 이미지에 대한 질문이나 분석 요점을 구체적으로 작성하세요.",
                "이미지의 특정 부분에 대해 언급할 때는 위치나 특징을 명확히 설명하세요.",
                "이미지와 텍스트 정보를 어떻게 통합하여 분석해야 하는지 지시하세요.",
                "시각적 요소와 텍스트적 요소를 별도로 분석한 후 통합 분석을 요청하세요."
            ],
            "tool_use": [
                "사용할 도구의 기능과 제한사항을 명확히 설명하세요.",
                "도구 사용의 목적과 원하는 결과를 구체적으로 지정하세요.",
                "여러 도구를 순차적으로 사용해야 하는 경우, 각 단계를 명확히 설명하세요.",
                "도구 사용 결과를 어떻게 분석하고 활용해야 하는지 지시하세요."
            ]
        }
        
        return tips.get(capability, ["GPT-o3는 복잡한 추론 문제 해결에 특화된 모델입니다."])
