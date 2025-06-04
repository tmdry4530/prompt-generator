from __future__ import annotations

import re
from typing import Any, Dict, List

from ..base_model import BaseModel


class Imagen3Model(BaseModel):
    """Simplified Imagen 3 model for tests."""

    model_id = "imagen-3"
    model_name = "Imagen 3"
    provider = "Google"
    supports_multimodal = False
    max_tokens = 1000
    capabilities = [
        "image_generation",
        "photorealistic_rendering",
        "artistic_rendering",
        "concept_visualization",
        "style_transfer",
    ]

    def __init__(self) -> None:
        self.subject_templates = {
            "portrait": "A detailed portrait of {description}.",
            "landscape": "A breathtaking landscape featuring {description}.",
            "product": "Product shot of {description}.",
            "concept_art": "Concept art of {description}.",
            "abstract": "Abstract visualization of {description}.",
            "architecture": "Architectural photograph of {description}.",
            "food": "Delicious food shot of {description}.",
        }
        self.style_templates = {
            "photorealistic": "photorealistic style",
            "cinematic": "cinematic style",
            "anime": "anime style",
            "digital_art": "digital art style",
            "oil_painting": "oil painting style",
            "watercolor": "watercolor style",
            "3d_render": "3D render style",
            "pixel_art": "pixel art style",
            "minimalist": "minimalist style",
            "fantasy": "fantasy style",
        }
        self.composition_templates = {
            "wide_shot": "wide shot composition",
            "close_up": "close up composition",
            "rule_of_thirds": "rule of thirds composition",
        }
        self.lighting_templates = {
            "natural": "natural lighting",
            "golden_hour": "golden hour lighting",
            "dramatic": "dramatic lighting",
        }
        self.negative_prompt_templates = {
            "default": "low quality, blurry, distorted",
        }
        self.best_practices = [
            "Use descriptive language",
            "Specify desired style",
        ]

    # ------------------------------------------------------------------
    # Prompt structure information
    # ------------------------------------------------------------------
    def get_prompt_structure(self) -> Dict[str, Any]:
        return {
            "components": [
                "subject_description",
                "style_specification",
                "composition_details",
                "lighting_details",
            ],
            "recommended_order": [
                "subject_description",
                "style_specification",
                "composition_details",
                "lighting_details",
            ],
            "optional_components": ["color_palette", "technical_spec"],
        }

    # ------------------------------------------------------------------
    # Subject analysis helpers
    # ------------------------------------------------------------------
    def _detect_subject_type(self, text: str) -> str:
        text_l = text.lower()
        if any(w in text_l for w in ["portrait", "초상화", "인물"]):
            return "portrait"
        if any(w in text_l for w in ["landscape", "풍경", "산"]):
            return "landscape"
        if "제품" in text_l or "product" in text_l:
            return "product"
        if "concept" in text_l or "컨셉" in text_l:
            return "concept_art"
        if "abstract" in text_l or "추상" in text_l:
            return "abstract"
        if "architecture" in text_l or "건물" in text_l or "대성당" in text_l:
            return "architecture"
        if "food" in text_l or "요리" in text_l or "파스타" in text_l:
            return "food"
        return "general"

    def _extract_subject_details(self, text: str, subject_type: str) -> Dict[str, str]:
        details = {"description": text}
        if subject_type == "portrait":
            if match := re.search(r"(웃는|smiling)", text, re.I):
                details["expression"] = match.group(1)
            if "자연광" in text:
                details["lighting"] = "자연광"
        elif subject_type == "landscape":
            if "일몰" in text or "sunset" in text:
                details["time_of_day"] = "일몰"
            if "흐린" in text:
                details["weather"] = "흐린"
            if "항공" in text or "aerial" in text:
                details["perspective"] = "항공"
        return details

    # ------------------------------------------------------------------
    # Prompt component generators
    # ------------------------------------------------------------------
    def _generate_style(self, analysis: Dict[str, Any], intent: Dict[str, Any]) -> str:
        if analysis.get("style"):
            style = analysis["style"][0][0]
            return self.style_templates.get(style, "")
        return ""

    def _generate_composition(self, analysis: Dict[str, Any], intent: Dict[str, Any]) -> str:
        comp = analysis.get("composition")
        if comp:
            return self.composition_templates.get(comp, "")
        return ""

    def _generate_lighting(self, analysis: Dict[str, Any], intent: Dict[str, Any]) -> str:
        light = analysis.get("lighting")
        if light:
            return self.lighting_templates.get(light, "")
        return ""

    def _generate_color_palette(self, analysis: Dict[str, Any], intent: Dict[str, Any]) -> str:
        if colors := analysis.get("colors"):
            return ", ".join(colors)
        mood = analysis.get("mood")
        if mood == "warm":
            return "따뜻한, 주황색, 노란색"
        if mood == "cool":
            return "차가운, 파란색, 보라색"
        return ""

    def _generate_negative_prompt(self, analysis: Dict[str, Any], intent: Dict[str, Any]) -> str:
        return self.negative_prompt_templates["default"]

    def _generate_technical(self, analysis: Dict[str, Any], intent: Dict[str, Any]) -> str:
        complexity = analysis.get("complexity", "medium")
        if complexity == "high":
            return "8K, 초고해상도, 세밀한"
        if complexity == "low":
            return "표준 해상도, 깔끔한"
        return "고해상도, 상세한"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        text = analysis_result.get("input_text", "")
        subject_type = self._detect_subject_type(text)
        details = self._extract_subject_details(text, subject_type)
        parts: List[str] = [details["description"]]

        style = self._generate_style(analysis_result, intent_result)
        if style:
            parts.append(style)
        comp = self._generate_composition(analysis_result, intent_result)
        if comp:
            parts.append(comp)
        light = self._generate_lighting(analysis_result, intent_result)
        if light:
            parts.append(light)
        palette = self._generate_color_palette(analysis_result, intent_result)
        if palette:
            parts.append(palette)
        tech = self._generate_technical(analysis_result, intent_result)
        if tech:
            parts.append(tech)
        negative = self._generate_negative_prompt(analysis_result, intent_result)
        parts.append(f"Negative prompt: {negative}")
        return ", ".join(parts)

    def get_generation_parameters(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> Dict[str, Any]:
        complexity = analysis_result.get("complexity", "medium")
        params = {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "quality": "standard",
            "format": "png",
        }
        if complexity == "high":
            params.update({"width": 1280, "height": 1280, "num_inference_steps": 75, "quality": "premium"})
        elif complexity == "low":
            params.update({"width": 768, "height": 768, "num_inference_steps": 30, "quality": "fast"})

        text = analysis_result.get("input_text", "").lower()
        if "초상화" in text or "portrait" in text:
            params["aspect_ratio"] = "3:4"
        elif "풍경" in text or "landscape" in text:
            params["aspect_ratio"] = "4:3"
        elif "제품" in text or "product" in text:
            params["aspect_ratio"] = "1:1"
        return params

    def get_capability_specific_tips(self, capability: str) -> List[str]:
        return self.best_practices
