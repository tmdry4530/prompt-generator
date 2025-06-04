"""
모델 최적화 프롬프트 생성기 - 중앙 조정 모듈

이 모듈은 다양한 AI 모델들에 대한 프롬프트 최적화를 통합적으로 관리합니다.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# 모델 클래스들 가져오기
from .base_model import BaseModel
from . import text_models, image_models, video_models, music_models

logger = logging.getLogger(__name__)

class ModelOptimizer:
    """다양한 AI 모델들에 대한 프롬프트 최적화를 중앙에서 관리하는 클래스"""
    
    def __init__(self):
        """ModelOptimizer 초기화"""
        self.models: Dict[str, BaseModel] = {}
        self._load_all_models()
        logger.info(f"ModelOptimizer initialized with {len(self.models)} models")
    
    def _load_all_models(self):
        """모든 지원되는 모델 인스턴스를 로드"""
        # 텍스트 모델들
        self.models["gpt4o"] = text_models.GPT4oModel()
        self.models["gemini-pro"] = text_models.Gemini25ProModel()
        self.models["grok-3"] = text_models.Grok3Model()
        self.models["v0"] = text_models.VercelV0Model()
        self.models["gpt-o3"] = text_models.GPTo3Model()
        
        # 이미지 모델들
        self.models["dalle3"] = image_models.DALLE3Model()
        self.models["imagen3"] = image_models.Imagen3Model()
        self.models["midjourney"] = image_models.MidjourneyV6Model()
        
        # 비디오 모델들
        self.models["veo3"] = video_models.GoogleVeo3Model()
        self.models["pika"] = video_models.PikaModel()
        self.models["sora"] = video_models.SoraModel()
        
        # 음악 모델들
        self.models["suno"] = music_models.SunoModel()
    
    def get_available_models(self, model_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        사용 가능한 모델 목록을 반환
        
        Args:
            model_type: 모델 타입으로 필터링 ('text', 'image', 'video', 'music')
            
        Returns:
            모델 정보 목록
        """
        result = []
        
        for model_id, model in self.models.items():
            model_info = model.get_model_info()
            
            # 모델 타입이 지정된 경우 필터링
            if model_type:
                if model_type == "text" and "text_generation" not in model_info["capabilities"]:
                    continue
                elif model_type == "image" and "image_generation" not in model_info["capabilities"]:
                    continue
                elif model_type == "video" and "video_generation" not in model_info["capabilities"]:
                    continue
                elif model_type == "music" and "music_generation" not in model_info["capabilities"]:
                    continue
            
            result.append(model_info)
        
        return result
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        특정 모델의 정보를 반환
        
        Args:
            model_id: 모델 ID
            
        Returns:
            모델 정보 딕셔너리
        """
        if model_id not in self.models:
            raise ValueError(f"Model ID '{model_id}' not found")
        
        return self.models[model_id].get_model_info()
    
    def optimize_prompt(self, model_id: str, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        특정 모델에 맞게 프롬프트를 최적화
        
        Args:
            model_id: 대상 모델 ID
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트와 메타데이터를 포함한 딕셔너리
        """
        if model_id not in self.models:
            raise ValueError(f"Model ID '{model_id}' not found")
        
        model = self.models[model_id]
        model_info = model.get_model_info()
        
        # 프롬프트 최적화 수행
        optimized_prompt = model.optimize_prompt(analysis_result, intent_result)
        
        # 최적화 결과 생성
        result = {
            "model_id": model_id,
            "model_name": model_info["model_name"],
            "provider": model_info["provider"],
            "optimized_prompt": optimized_prompt,
            "prompt_structure": model.get_prompt_structure(),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def get_capability_tips(self, model_id: str, capability: str) -> List[str]:
        """
        특정 모델의 특정 기능에 대한 최적화 팁을 반환
        
        Args:
            model_id: 모델 ID
            capability: 기능 이름
            
        Returns:
            최적화 팁 목록
        """
        if model_id not in self.models:
            raise ValueError(f"Model ID '{model_id}' not found")
        
        return self.models[model_id].get_capability_specific_tips(capability)
    
    def batch_optimize(self, model_ids: List[str], analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        여러 모델에 대해 일괄적으로 프롬프트 최적화 수행
        
        Args:
            model_ids: 대상 모델 ID 목록
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            모델별 최적화 결과를 포함한 딕셔너리
        """
        results = {}
        
        for model_id in model_ids:
            try:
                results[model_id] = self.optimize_prompt(model_id, analysis_result, intent_result)
            except Exception as e:
                logger.error(f"Error optimizing prompt for model {model_id}: {str(e)}")
                results[model_id] = {"error": str(e)}
        
        return results 