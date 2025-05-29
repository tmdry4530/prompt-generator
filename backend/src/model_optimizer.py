"""
Model Optimization Prompt Generator
모델별로 최적화된 프롬프트를 생성하는 핵심 클래스
"""

from typing import Dict, List, Optional
import json
from datetime import datetime


class ModelOptimizationPromptGenerator:
    """AI 모델별로 최적화된 프롬프트를 생성하는 클래스"""
    
    def __init__(self):
        self.model_configs = {
            'gpt-4': {
                'max_tokens': 8192,
                'strengths': ['추론', '창의성', '코드 생성'],
                'optimization_tips': [
                    '명확하고 구조화된 지시사항 사용',
                    '복잡한 작업을 단계별로 분해',
                    '이해를 돕기 위한 예시 제공',
                    'Chain-of-Thought 프롬프팅 활용'
                ],
                'prompt_structure': 'step_by_step'
            },
            'claude-3': {
                'max_tokens': 100000,
                'strengths': ['분석', '글쓰기', '안전성'],
                'optimization_tips': [
                    '긴 컨텍스트 윈도우 활용',
                    '구조화를 위한 XML 태그 사용',
                    '출력 형식에 대한 명시적 지시',
                    '세부적인 분석 요청'
                ],
                'prompt_structure': 'xml_structured'
            },
            'llama-2': {
                'max_tokens': 4096,
                'strengths': ['효율성', '오픈소스'],
                'optimization_tips': [
                    '간결한 프롬프트 유지',
                    'Few-shot 예시 사용',
                    '모호한 지시사항 피하기',
                    '직접적이고 명확한 언어 사용'
                ],
                'prompt_structure': 'concise'
            },
            'gemini-pro': {
                'max_tokens': 30720,
                'strengths': ['멀티모달', '검색', '실시간 정보'],
                'optimization_tips': [
                    '멀티모달 입력 활용',
                    '단계별 추론 요청',
                    '구체적인 예시와 형식 제공',
                    '코드와 텍스트 혼합 작업에 특화'
                ],
                'prompt_structure': 'multimodal'
            }
        }
    
    def generate_optimized_prompt(self, user_task: str, model_name: str, 
                                template_type: Optional[str] = None) -> Dict[str, str]:
        """
        사용자 작업과 모델명을 받아 최적화된 프롬프트를 생성
        
        Args:
            user_task: 사용자가 요청한 작업
            model_name: 대상 AI 모델명
            template_type: 템플릿 타입 (optional)
        
        Returns:
            최적화된 프롬프트와 메타데이터를 포함한 딕셔너리
        """
        if model_name not in self.model_configs:
            return {
                'error': f"모델 '{model_name}'은 아직 지원되지 않습니다.",
                'supported_models': list(self.model_configs.keys())
            }
        
        config = self.model_configs[model_name]
        optimized_instructions = self._apply_optimizations(user_task, config)
        
        result = {
            'original_task': user_task,
            'model': model_name,
            'optimized_prompt': self._format_prompt(optimized_instructions, config),
            'optimization_tips': config['optimization_tips'],
            'model_strengths': config['strengths'],
            'max_tokens': config['max_tokens'],
            'generated_at': datetime.now().isoformat(),
            'prompt_structure': config['prompt_structure']
        }
        
        return result
    
    def _apply_optimizations(self, task: str, config: Dict) -> str:
        """모델별 최적화 규칙을 적용하여 지시사항을 개선"""
        structure = config.get('prompt_structure', 'basic')
        
        if structure == 'step_by_step':
            return self._create_step_by_step_prompt(task)
        elif structure == 'xml_structured':
            return self._create_xml_structured_prompt(task)
        elif structure == 'concise':
            return self._create_concise_prompt(task)
        elif structure == 'multimodal':
            return self._create_multimodal_prompt(task)
        else:
            return task
    
    def _create_step_by_step_prompt(self, task: str) -> str:
        """GPT-4에 최적화된 단계별 프롬프트 생성"""
        return f"""다음 작업을 단계별로 수행해주세요:

**작업**: {task}

**수행 단계**:
1. **분석**: 요청사항을 정확히 이해하고 분석
2. **계획**: 작업 수행을 위한 구체적인 계획 수립
3. **실행**: 계획에 따라 작업 수행
4. **검증**: 결과의 정확성과 완성도 확인

**출력 요구사항**:
- 각 단계별로 명확한 설명 제공
- 최종 결과는 실제로 사용 가능한 형태로 제공
- 필요한 경우 예시나 코드 포함"""

    def _create_xml_structured_prompt(self, task: str) -> str:
        """Claude-3에 최적화된 XML 구조 프롬프트 생성"""
        return f"""<task_request>
<description>{task}</description>
<requirements>
- 체계적이고 철저한 분석 수행
- 명확하고 구조화된 출력 제공
- 단계별 사고 과정 포함
</requirements>
<output_format>
구체적이고 실행 가능한 결과를 제공하되, 
분석 과정과 결론을 명확히 구분하여 제시
</output_format>
</task_request>

위 요청사항에 따라 체계적으로 분석하고 응답해주세요."""

    def _create_concise_prompt(self, task: str) -> str:
        """Llama-2에 최적화된 간결한 프롬프트 생성"""
        return f"""작업: {task}

요구사항:
- 명확하고 간결한 응답
- 관련 예시 포함
- 실용적이고 즉시 사용 가능한 결과

출력 형식: 구조화된 응답으로 핵심 내용 위주"""

    def _create_multimodal_prompt(self, task: str) -> str:
        """Gemini Pro에 최적화된 멀티모달 프롬프트 생성"""
        return f"""**요청 작업**: {task}

**분석 접근법**:
1. 멀티모달 관점에서 작업 분석
2. 단계별 추론 과정 제시
3. 코드, 텍스트, 구조화된 데이터 등 적절한 형식 활용

**출력 구성**:
- 개요 및 핵심 포인트
- 세부 구현 또는 설명
- 실제 사용 예시
- 추가 고려사항

실용성과 명확성을 중시하여 응답해주세요."""
    
    def _format_prompt(self, instructions: str, config: Dict) -> str:
        """최종 프롬프트 형식 정리"""
        header = f"### {config.get('prompt_structure', 'optimized').upper()} 최적화 프롬프트\n\n"
        footer = f"\n\n---\n**모델 특성**: {', '.join(config['strengths'])}\n**토큰 한계**: {config['max_tokens']:,}개"
        
        return header + instructions + footer
    
    def get_supported_models(self) -> List[str]:
        """지원되는 모델 목록 반환"""
        return list(self.model_configs.keys())
    
    def get_model_info(self, model_name: str) -> Dict:
        """특정 모델의 정보 반환"""
        return self.model_configs.get(model_name, {}) 