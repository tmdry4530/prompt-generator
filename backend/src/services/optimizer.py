"""
프롬프트 최적화 엔진: 사용자 입력을 분석하고 AI 모델별로 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List, Optional
import importlib
import os
import re

from ..utils.input_analyzer import InputAnalyzer
<<<<<<< HEAD
=======
from ..utils.intent_detector import IntentDetector
>>>>>>> 18484904e94c2c1fa8167b2fc37183a158c51fff
from ..models.base_model import BaseModel

class PromptOptimizer:
    """
    프롬프트 최적화 엔진 클래스
    
    사용자 입력을 분석하고 선택된 AI 모델에 최적화된 프롬프트를 생성합니다.
    """
    
    def __init__(self):
        """프롬프트 최적화 엔진 초기화"""
        self.input_analyzer = InputAnalyzer()
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """사용 가능한 모든 모델을 동적으로 로드합니다."""
        # 텍스트 모델 로드
        self._load_models_from_directory('text_models')
        
        # 이미지 모델 로드
        self._load_models_from_directory('image_models')
        
        # 비디오 모델 로드
        self._load_models_from_directory('video_models')
        
        # 음악 모델 로드
        self._load_models_from_directory('music_models')
    
    def _load_models_from_directory(self, directory: str):
        """지정된 디렉토리에서 모델을 로드합니다."""
        try:
            # 모듈 경로 생성
            module_path = f'..models.{directory}'
            
<<<<<<< HEAD
            # 모듈 동적 로드
            module = importlib.import_module(module_path, package=__package__)
=======
            # 디렉토리 내 모든 Python 파일 가져오기
            # __file__ is optimizer.py, so dirname is services. '..' goes to src, then 'models'
            module_dir = os.path.join(os.path.dirname(__file__), '..', 'models', directory)
            
            if not os.path.exists(module_dir):
                print(f"Model directory not found: {module_dir}") # Added a print for debugging
                return
            
            for filename in os.listdir(module_dir):
                if filename.endswith('.py') and not filename.startswith('__'):
                    # 파일 이름에서 모듈 이름 추출
                    module_name = filename[:-3]
                    
                    try:
                        # 모듈 동적 로드
                        module = importlib.import_module(f'{module_path}.{module_name}', package=__package__)
>>>>>>> 18484904e94c2c1fa8167b2fc37183a158c51fff
                        
            # __all__ 리스트에서 클래스 이름들 가져오기
            if hasattr(module, '__all__'):
                for class_name in module.__all__:
                    try:
                        # 클래스 가져오기
                        model_class = getattr(module, class_name)
                            
                        # BaseModel을 상속받은 클래스인지 확인
                        if isinstance(model_class, type) and issubclass(model_class, BaseModel) and model_class is not BaseModel:
                            # 모델 인스턴스 생성 및 저장
                            model_instance = model_class()
                            self.models[model_instance.model_id] = model_instance
                            print(f"모델 로드 성공: {model_instance.model_id} ({model_instance.model_name})")
                    except Exception as e:
                        print(f"모델 클래스 로드 중 오류 발생: {class_name} - {str(e)}")
            
        except Exception as e:
            print(f"모델 디렉토리 로드 중 오류 발생: {directory} - {str(e)}")
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        사용 가능한 모든 모델 정보를 반환합니다.
        
        Returns:
            모델 정보 목록
        """
        models_info = []
        
        for model_id, model in self.models.items():
            models_info.append({
                "model_id": model_id,
                "model_name": model.model_name,
                "provider": model.provider,
                "capabilities": model.capabilities,
                "supports_multimodal": model.supports_multimodal
            })
        
        return models_info
    
    def optimize_prompt(self, input_text: str, model_id: str, additional_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        사용자 입력을 분석하고 선택된 모델에 최적화된 프롬프트를 생성합니다.
        
        Args:
            input_text: 사용자가 입력한 기본 요청 텍스트
            model_id: 최적화할 대상 모델 ID
            additional_params: 추가 매개변수 (선택 사항)
            
        Returns:
            최적화된 프롬프트 및 관련 정보를 담은 딕셔너리
        """
        if not additional_params:
            additional_params = {}
        
        # 모델 존재 여부 확인
        if model_id not in self.models:
            return {
                "success": False,
                "error": f"지원하지 않는 모델 ID: {model_id}",
                "available_models": list(self.models.keys())
            }
        
        try:
            # 입력 분석
            analysis_result = self.input_analyzer.analyze(input_text, model_id)
            
            # 의도 결과 (기본값 설정)
            intent_result = {
                "primary_intent": ("generate_content", 0.8),
                "is_creative": False,
                "is_technical": False,
                "urgency_level": "medium"
            }
            
            # 선택된 모델 가져오기
            model = self.models[model_id]
            
            # 추가 매개변수 병합
            analysis_result.update(additional_params)
            
            # 프롬프트 최적화
            optimized_prompt = model.optimize_prompt(analysis_result, intent_result)
            
            # 모델별 생성 매개변수 가져오기 (이미지/비디오 모델용)
            generation_params = {}
            if hasattr(model, 'get_generation_parameters'):
                generation_params = model.get_generation_parameters(analysis_result, intent_result)
            
            # 모델 정보 가져오기
            model_info = model.get_model_info()
            
            # 프롬프트 구조 가져오기
            prompt_structure = model.get_prompt_structure()
            
            # 결과 반환
            return {
                "success": True,
                "original_input": input_text,
                "optimized_prompt": optimized_prompt,
                "model_id": model_id,
                "model_info": model_info,
                "prompt_structure": prompt_structure,
                "generation_params": generation_params,
                "analysis_result": analysis_result,
                "intent_result": intent_result
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"프롬프트 최적화 중 오류 발생: {str(e)}",
                "original_input": input_text,
                "model_id": model_id
            }
    
    def get_model_specific_tips(self, model_id: str, capability: Optional[str] = None) -> List[str]:
        """
        특정 모델 및 기능에 대한 최적화 팁을 반환합니다.
        
        Args:
            model_id: 모델 ID
            capability: 기능 이름 (선택 사항)
            
        Returns:
            최적화 팁 목록
        """
        # 모델 존재 여부 확인
        if model_id not in self.models:
            return [f"지원하지 않는 모델 ID: {model_id}"]
        
        # 모델 가져오기
        model = self.models[model_id]
        
        # 기능이 지정되지 않은 경우 모델의 첫 번째 기능 사용
        if not capability and model.capabilities:
            capability = model.capabilities[0]
        
        # 모델별 팁 가져오기
        return model.get_capability_specific_tips(capability)
    
    def get_model_prompt_structure(self, model_id: str) -> Dict[str, Any]:
        """
        특정 모델의 프롬프트 구조를 반환합니다.
        
        Args:
            model_id: 모델 ID
            
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        # 모델 존재 여부 확인
        if model_id not in self.models:
            return {"error": f"지원하지 않는 모델 ID: {model_id}"}
        
        # 모델 가져오기
        model = self.models[model_id]
        
        # 프롬프트 구조 반환
        return model.get_prompt_structure()
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        특정 모델의 정보를 반환합니다.
        
        Args:
            model_id: 모델 ID
            
        Returns:
            모델 정보를 담은 딕셔너리
        """
        # 모델 존재 여부 확인
        if model_id not in self.models:
            return {"error": f"지원하지 않는 모델 ID: {model_id}"}
        
        # 모델 가져오기
        model = self.models[model_id]
        
        # 모델 정보 반환
        return model.get_model_info()
    
    def compare_models(self, model_ids: List[str]) -> Dict[str, Any]:
        """
        여러 모델을 비교합니다.
        
        Args:
            model_ids: 비교할 모델 ID 목록
            
        Returns:
            모델 비교 정보를 담은 딕셔너리
        """
        comparison = {
            "models": [],
            "capabilities": {},
            "providers": {},
            "multimodal_support": {}
        }
        
        for model_id in model_ids:
            if model_id in self.models:
                model = self.models[model_id]
                model_info = model.get_model_info()
                
                # 모델 정보 추가
                comparison["models"].append(model_info)
                
                # 기능별 지원 현황 추가
                for capability in model_info["capabilities"]:
                    if capability not in comparison["capabilities"]:
                        comparison["capabilities"][capability] = []
                    comparison["capabilities"][capability].append(model_id)
                
                # 제공업체별 모델 추가
                provider = model_info["provider"]
                if provider not in comparison["providers"]:
                    comparison["providers"][provider] = []
                comparison["providers"][provider].append(model_id)
                
                # 멀티모달 지원 현황 추가
                supports_multimodal = model_info["supports_multimodal"]
                multimodal_key = "supported" if supports_multimodal else "not_supported"
                if multimodal_key not in comparison["multimodal_support"]:
                    comparison["multimodal_support"][multimodal_key] = []
                comparison["multimodal_support"][multimodal_key].append(model_id)
        
        return comparison
