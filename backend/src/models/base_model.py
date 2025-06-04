"""
기본 모델 클래스: 모든 AI 모델 최적화 모듈의 기본 클래스입니다.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseModel(ABC):
    """
    모든 AI 모델 최적화 모듈의 기본 클래스
    """
    
    def __init__(self, model_id: str, model_name: str, provider: str):
        """
        기본 모델 클래스 초기화
        
        Args:
            model_id: 모델 식별자
            model_name: 모델 이름
            provider: 모델 제공 업체
        """
        self.model_id = model_id
        self.model_name = model_name
        self.provider = provider
        self.capabilities = []
        self.max_tokens = 0
        self.supports_multimodal = False
        self.best_practices = []
        
    @abstractmethod
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        pass
    
    @abstractmethod
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        모델 정보를 반환합니다.
        
        Returns:
            모델 정보를 담은 딕셔너리
        """
        return {
            "model_id": self.model_id,
            "model_name": self.model_name,
            "provider": self.provider,
            "capabilities": self.capabilities,
            "max_tokens": self.max_tokens,
            "supports_multimodal": self.supports_multimodal,
            "best_practices": self.best_practices
        }
    
    def get_capability_specific_tips(self, capability: str) -> List[str]:
        """
        특정 기능에 대한 최적화 팁을 반환합니다.
        
        Args:
            capability: 기능 이름
            
        Returns:
            최적화 팁 목록
        """
        # 기본 구현은 빈 목록 반환
        return []
    
    def apply_common_rules(self, prompt: str) -> str:
        """
        모든 모델에 공통적으로 적용되는 규칙을 프롬프트에 적용합니다.
        
        Args:
            prompt: 원본 프롬프트
            
        Returns:
            규칙이 적용된 프롬프트
        """
        # 기본 구현은 원본 프롬프트 반환
        return prompt
