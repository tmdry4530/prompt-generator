from typing import Any, Dict, List

class BaseModel:
    """Base class for all models."""

    model_id: str = ""
    model_name: str = ""
    provider: str = ""
    capabilities: List[str] = []
    supports_multimodal: bool = False
    max_tokens: int = 0
    best_practices: List[str] = []

    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        raise NotImplementedError

    def get_model_info(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "model_name": self.model_name,
            "provider": self.provider,
            "capabilities": self.capabilities,
            "supports_multimodal": self.supports_multimodal,
        }

    def get_prompt_structure(self) -> Dict[str, Any]:
        return {"components": [], "recommended_order": [], "optional_components": []}

    def get_capability_specific_tips(self, capability: str) -> List[str]:
        return self.best_practices

    def get_generation_parameters(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> Dict[str, Any]:
        return {}
