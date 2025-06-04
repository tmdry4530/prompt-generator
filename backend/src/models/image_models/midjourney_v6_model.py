"""
Midjourney v6 모델 최적화 모듈: Midjourney v6 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class MidjourneyV6Model(BaseModel):
    """
    Midjourney v6 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """Midjourney v6 모델 클래스 초기화"""
        super().__init__(
            model_id="midjourney-v6",
            model_name="Midjourney v6",
            provider="Midjourney"
        )
        self.capabilities = [
            "image_generation",
            "photorealistic_rendering",
            "artistic_rendering",
            "concept_visualization",
            "style_transfer",
            "parameter_customization"
        ]
        self.max_tokens = 1000  # 프롬프트 최대 길이
        self.supports_multimodal = False
        self.best_practices = [
            "명확하고 간결한 설명 제공",
            "매개변수 활용 (--ar, --v, --s, --q, --c)",
            "스타일과 분위기 명시",
            "참조 아티스트나 스타일 언급",
            "부정적 프롬프트 활용 (--no)",
            "이미지 참조 활용 가능"
        ]
        
        # Midjourney v6에 최적화된 주제 템플릿
        self.subject_templates = {
            "landscape": "{description}, {time_of_day}, {weather}, {perspective}, {style}",
            "portrait": "{description}, {pose}, {expression}, {lighting}, {background}, {style}",
            "product": "{product_name}, {product_details}, {background}, {lighting}, {angle}, {style}",
            "concept_art": "{concept_description}, {style}, {mood}, {color_palette}, {details}",
            "abstract": "{theme}, {style}, {color_palette}, {texture}, {composition}, {details}",
            "architecture": "{building_type}, {architectural_style}, {materials}, {surroundings}, {time_of_day}, {style}",
            "food": "{food_name}, {presentation}, {garnish}, {plating}, {background}, {lighting}, {style}"
        }
        
        # 스타일 템플릿
        self.style_templates = {
            "photorealistic": "photorealistic, highly detailed, 8k, ultra realistic, photography",
            "cinematic": "cinematic, movie scene, film still, dramatic lighting, cinematic composition",
            "anime": "anime style, manga, vibrant colors, clean lines, 2D animation",
            "digital_art": "digital art, digital painting, detailed, vibrant colors, computer graphics",
            "oil_painting": "oil painting, textured canvas, thick brushstrokes, classical painting technique",
            "watercolor": "watercolor painting, soft edges, flowing colors, transparent washes",
            "3d_render": "3D render, octane render, blender, realistic textures, volumetric lighting",
            "pixel_art": "pixel art, retro game style, limited color palette, pixelated details",
            "minimalist": "minimalist, simple shapes, limited color palette, clean composition",
            "fantasy": "fantasy art, magical, mystical, ethereal, otherworldly"
        }
        
        # 매개변수 템플릿
        self.parameter_templates = {
            "aspect_ratio": {
                "square": "--ar 1:1",
                "portrait": "--ar 2:3",
                "landscape": "--ar 3:2",
                "wide": "--ar 16:9",
                "ultrawide": "--ar 21:9",
                "panorama": "--ar 3:1"
            },
            "stylize": {
                "low": "--s 50",
                "medium": "--s 100",
                "high": "--s 250",
                "very_high": "--s 750"
            },
            "quality": {
                "draft": "--q .5",
                "normal": "--q 1",
                "high": "--q 2"
            },
            "chaos": {
                "low": "--c 10",
                "medium": "--c 25",
                "high": "--c 50",
                "very_high": "--c 100"
            },
            "version": {
                "default": "--v 6",
                "niji": "--niji 6"
            }
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        Midjourney v6 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        return {
            "components": [
                "subject_description",
                "style_specification",
                "details_and_modifiers",
                "parameters",
                "negative_prompt"
            ],
            "recommended_order": [
                "subject_description",
                "style_specification",
                "details_and_modifiers",
                "parameters",
                "negative_prompt"
            ],
            "optional_components": [
                "details_and_modifiers",
                "parameters",
                "negative_prompt"
            ]
        }
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 Midjourney v6에 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        # 1. 주제 설명 생성
        subject = self._generate_subject(analysis_result, intent_result)
        
        # 2. 스타일 명세 생성
        style = self._generate_style(analysis_result, intent_result)
        
        # 3. 세부 사항 및 수정자 생성
        details = self._generate_details(analysis_result, intent_result)
        
        # 4. 매개변수 생성
        parameters = self._generate_parameters(analysis_result, intent_result)
        
        # 5. 부정적 프롬프트 생성
        negative = self._generate_negative_prompt(analysis_result, intent_result)
        
        # 6. 최종 프롬프트 조합
        prompt_parts = []
        
        if subject:
            prompt_parts.append(subject)
            
        if style and style not in subject:
            prompt_parts.append(style)
            
        if details:
            prompt_parts.append(details)
        
        # 주요 프롬프트 부분 조합
        main_prompt = ", ".join(filter(None, prompt_parts))
        
        # 공통 규칙 적용
        main_prompt = self.apply_common_rules(main_prompt)
        
        # 매개변수와 부정적 프롬프트 추가
        if parameters:
            main_prompt = f"{main_prompt} {parameters}"
        
        if negative:
            main_prompt = f"{main_prompt} --no {negative}"
        
        return main_prompt
    
    def _generate_subject(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """주제 설명을 생성합니다."""
        # 기본 주제 설명
        input_text = analysis_result.get("input_text", "")
        
        # 주제 유형 감지
        subject_type = self._detect_subject_type(input_text)
        
        # 주제 세부 정보 추출
        subject_details = self._extract_subject_details(input_text, subject_type)
        
        # 주제 템플릿 선택 및 적용
        if subject_type in self.subject_templates:
            template = self.subject_templates[subject_type]
            
            # 템플릿 변수 채우기
            for key, value in subject_details.items():
                placeholder = "{" + key + "}"
                if placeholder in template and value:
                    template = template.replace(placeholder, value)
                else:
                    # 값이 없는 플레이스홀더 제거
                    template = template.replace(placeholder, "")
            
            # 남은 플레이스홀더 제거
            template = re.sub(r'\{[^}]*\}', '', template)
            
            # 연속된 쉼표 및 공백 정리
            template = re.sub(r',\s*,', ',', template)
            template = re.sub(r',\s*$', '', template)
            
            return template
        
        # 템플릿이 없으면 원본 텍스트 반환
        return input_text
    
    def _detect_subject_type(self, text: str) -> str:
        """입력 텍스트에서 주제 유형을 감지합니다."""
        # 간단한 키워드 기반 감지 (실제로는 더 복잡한 분류 로직 필요)
        keywords = {
            "landscape": ["풍경", "자연", "산", "바다", "호수", "숲", "하늘", "일몰", "일출"],
            "portrait": ["인물", "사람", "얼굴", "초상화", "셀카", "프로필"],
            "product": ["제품", "상품", "물건", "광고", "쇼핑", "판매"],
            "concept_art": ["컨셉", "아트", "판타지", "미래", "상상", "창의적"],
            "abstract": ["추상", "비현실적", "기하학적", "패턴", "형태"],
            "architecture": ["건물", "건축", "구조물", "도시", "인테리어", "외관"],
            "food": ["음식", "요리", "식사", "디저트", "음료", "맛있는"]
        }
        
        # 텍스트를 소문자로 변환
        text_lower = text.lower()
        
        # 각 유형별 키워드 매칭 점수 계산
        scores = {}
        for subject_type, type_keywords in keywords.items():
            score = sum(1 for keyword in type_keywords if keyword in text_lower)
            scores[subject_type] = score
        
        # 가장 높은 점수의 유형 반환
        if scores:
            max_type = max(scores.items(), key=lambda x: x[1])
            if max_type[1] > 0:
                return max_type[0]
        
        # 기본값은 landscape
        return "landscape"
    
    def _extract_subject_details(self, text: str, subject_type: str) -> Dict[str, str]:
        """입력 텍스트에서 주제 세부 정보를 추출합니다."""
        # 기본 세부 정보
        details = {
            "description": text
        }
        
        # 주제 유형별 추가 세부 정보
        if subject_type == "landscape":
            # 시간대 추출
            time_patterns = ["아침", "낮", "저녁", "밤", "일출", "일몰", "황혼", "새벽"]
            for pattern in time_patterns:
                if pattern in text:
                    details["time_of_day"] = pattern
                    break
            
            # 날씨 추출
            weather_patterns = ["맑은", "흐린", "비", "눈", "안개", "폭풍", "구름"]
            for pattern in weather_patterns:
                if pattern in text:
                    details["weather"] = pattern
                    break
            
            # 시점 추출
            perspective_patterns = ["조감도", "항공", "드론", "위에서", "아래에서", "멀리서", "가까이서"]
            for pattern in perspective_patterns:
                if pattern in text:
                    details["perspective"] = pattern
                    break
        
        elif subject_type == "portrait":
            # 포즈 추출
            pose_patterns = ["서있는", "앉아있는", "누워있는", "걷는", "뛰는", "기대어 있는"]
            for pattern in pose_patterns:
                if pattern in text:
                    details["pose"] = pattern
                    break
            
            # 표정 추출
            expression_patterns = ["웃는", "미소", "진지한", "슬픈", "화난", "놀란", "평온한"]
            for pattern in expression_patterns:
                if pattern in text:
                    details["expression"] = pattern
                    break
            
            # 조명 추출
            lighting_patterns = ["자연광", "스튜디오", "백라이트", "측면광", "부드러운 조명", "강한 조명"]
            for pattern in lighting_patterns:
                if pattern in text:
                    details["lighting"] = pattern
                    break
            
            # 배경 추출
            background_patterns = ["실내", "실외", "자연", "도시", "단색", "흐린", "스튜디오"]
            for pattern in background_patterns:
                if pattern in text:
                    details["background"] = pattern
                    break
        
        # 다른 주제 유형에 대한 세부 정보 추출 로직 추가 가능
        
        return details
    
    def _generate_style(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """스타일 명세를 생성합니다."""
        # 스타일 정보 추출
        styles = analysis_result.get("style", [])
        style_text = ""
        
        # 스타일이 명시적으로 지정된 경우
        if styles:
            if isinstance(styles[0], tuple):
                style_name = styles[0][0]
            else:
                style_name = styles[0]
                
            # 템플릿에서 스타일 찾기
            if style_name in self.style_templates:
                style_text = self.style_templates[style_name]
            else:
                style_text = style_name
        else:
            # 기본 스타일은 photorealistic
            style_text = self.style_templates["photorealistic"]
        
        return style_text
    
    def _generate_details(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """세부 사항 및 수정자를 생성합니다."""
        details_parts = []
        
        # 색상 정보 추출
        colors = analysis_result.get("colors", [])
        if colors:
            details_parts.append(", ".join(colors) + " color palette")
        
        # 분위기 정보 추출
        mood = analysis_result.get("mood", "")
        if mood:
            mood_map = {
                "warm": "warm atmosphere, cozy feeling",
                "cool": "cool atmosphere, refreshing feeling",
                "peaceful": "peaceful atmosphere, serene feeling",
                "dramatic": "dramatic atmosphere, intense feeling",
                "mysterious": "mysterious atmosphere, enigmatic feeling",
                "romantic": "romantic atmosphere, emotional feeling",
                "energetic": "energetic atmosphere, dynamic feeling",
                "nostalgic": "nostalgic atmosphere, reminiscent feeling",
                "futuristic": "futuristic atmosphere, high-tech feeling",
                "vintage": "vintage atmosphere, classic feeling"
            }
            details_parts.append(mood_map.get(mood, mood))
        
        # 조명 정보 추출
        lighting = analysis_result.get("lighting", "")
        if lighting:
            lighting_map = {
                "natural": "natural lighting, soft sunlight",
                "golden_hour": "golden hour lighting, warm orange light, long shadows",
                "blue_hour": "blue hour lighting, blue tones, twilight",
                "dramatic": "dramatic lighting, strong contrast, sharp shadows",
                "studio": "studio lighting, even illumination, professional setup",
                "backlight": "backlight, silhouette effect, glowing edges",
                "neon": "neon lighting, vibrant colored artificial lights, urban atmosphere",
                "candlelight": "candlelight, warm orange glow, soft shadows",
                "moonlight": "moonlight, blue tones, soft shadows, mysterious atmosphere"
            }
            details_parts.append(lighting_map.get(lighting, lighting))
        
        # 추가 세부 사항
        details_parts.append("highly detailed")
        details_parts.append("intricate")
        details_parts.append("sharp focus")
        
        # 세부 사항 조합
        if details_parts:
            return ", ".join(details_parts)
        
        return ""
    
    def _generate_parameters(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """매개변수를 생성합니다."""
        parameters = []
        
        # 종횡비 매개변수
        aspect_ratio = analysis_result.get("aspect_ratio", "")
        if aspect_ratio in self.parameter_templates["aspect_ratio"]:
            parameters.append(self.parameter_templates["aspect_ratio"][aspect_ratio])
        else:
            # 주제 유형에 따른 기본 종횡비 선택
            subject_type = self._detect_subject_type(analysis_result.get("input_text", ""))
            if subject_type == "landscape":
                parameters.append(self.parameter_templates["aspect_ratio"]["landscape"])
            elif subject_type == "portrait":
                parameters.append(self.parameter_templates["aspect_ratio"]["portrait"])
            else:
                parameters.append(self.parameter_templates["aspect_ratio"]["square"])
        
        # 스타일화 매개변수
        stylize = analysis_result.get("stylize", "medium")
        if stylize in self.parameter_templates["stylize"]:
            parameters.append(self.parameter_templates["stylize"][stylize])
        else:
            parameters.append(self.parameter_templates["stylize"]["medium"])
        
        # 품질 매개변수
        quality = analysis_result.get("quality", "high")
        if quality in self.parameter_templates["quality"]:
            parameters.append(self.parameter_templates["quality"][quality])
        else:
            parameters.append(self.parameter_templates["quality"]["high"])
        
        # 혼돈 매개변수
        chaos = analysis_result.get("chaos", "")
        if chaos in self.parameter_templates["chaos"]:
            parameters.append(self.parameter_templates["chaos"][chaos])
        else:
            parameters.append(self.parameter_templates["chaos"]["medium"])
        
        # 버전 매개변수
        version = analysis_result.get("version", "default")
        if version in self.parameter_templates["version"]:
            parameters.append(self.parameter_templates["version"][version])
        else:
            parameters.append(self.parameter_templates["version"]["default"])