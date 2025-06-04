"""
Imagen 3 모델 최적화 모듈: Imagen 3 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class Imagen3Model(BaseModel):
    """
    Imagen 3 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """Imagen 3 모델 클래스 초기화"""
        super().__init__(
            model_id="imagen-3",
            model_name="Imagen 3",
            provider="Google"
        )
        self.capabilities = [
            "image_generation",
            "photorealistic_rendering",
            "artistic_rendering",
            "concept_visualization",
            "style_transfer"
        ]
        self.max_tokens = 1000  # 프롬프트 최대 길이
        self.supports_multimodal = False
        self.best_practices = [
            "상세한 시각적 설명 제공",
            "구체적인 스타일과 분위기 명시",
            "구도와 시점 지정",
            "색상 팔레트 설명",
            "참조 아티스트나 스타일 언급",
            "부정적 프롬프트 활용"
        ]
        
        # Imagen 3에 최적화된 주제 템플릿
        self.subject_templates = {
            "landscape": "자연 풍경: {description}, {time_of_day}, {weather}, {perspective}",
            "portrait": "인물 사진: {description}, {pose}, {expression}, {lighting}, {background}",
            "product": "제품 사진: {product_name}, {product_details}, {background}, {lighting}, {angle}",
            "concept_art": "컨셉 아트: {concept_description}, {style}, {mood}, {color_palette}",
            "abstract": "추상 이미지: {theme}, {style}, {color_palette}, {texture}, {composition}",
            "architecture": "건축물: {building_type}, {architectural_style}, {materials}, {surroundings}, {time_of_day}",
            "food": "음식 사진: {food_name}, {presentation}, {garnish}, {plating}, {background}, {lighting}"
        }
        
        # 스타일 템플릿
        self.style_templates = {
            "photorealistic": "포토리얼리스틱, 고해상도, 세밀한 디테일, 사실적인 조명과 그림자, 자연스러운 색감",
            "cinematic": "영화적인, 시네마틱, 드라마틱한 조명, 영화 장면 같은, 시네마토그래피, 영화 스틸컷",
            "anime": "애니메이션 스타일, 일본 애니메이션, 선명한 윤곽선, 밝은 색상, 만화적 표현",
            "digital_art": "디지털 아트, 디지털 페인팅, 세밀한 디테일, 풍부한 색감, 컴퓨터 그래픽",
            "oil_painting": "유화 스타일, 두꺼운 붓 터치, 질감이 느껴지는, 캔버스 위의 페인팅, 고전적인 유화 기법",
            "watercolor": "수채화 스타일, 투명한 색감, 부드러운 경계, 물감이 번지는 효과, 가벼운 터치",
            "3d_render": "3D 렌더링, 컴퓨터 그래픽, 정교한 모델링, 사실적인 텍스처, 볼륨감 있는 조명",
            "pixel_art": "픽셀 아트, 레트로 게임 스타일, 제한된 색 팔레트, 픽셀화된 디테일, 8비트/16비트 스타일",
            "minimalist": "미니멀리스트, 단순한 형태, 제한된 색상, 깔끔한 구성, 불필요한 요소 제거",
            "fantasy": "판타지 스타일, 마법적인 요소, 초현실적인 풍경, 신비로운 분위기, 환상적인 생물"
        }
        
        # 구도 템플릿
        self.composition_templates = {
            "wide_shot": "와이드 샷, 넓은 시야, 전체 장면 포착, 풍경 중심",
            "close_up": "클로즈업, 세부 디테일 강조, 근접 촬영, 주제에 집중",
            "aerial_view": "조감도, 위에서 내려다보는 시점, 드론 시점, 전체 조망",
            "dutch_angle": "더치 앵글, 기울어진 구도, 역동적인 느낌, 불안정한 분위기",
            "symmetrical": "대칭 구도, 균형 잡힌 배치, 중앙 정렬, 정돈된 느낌",
            "rule_of_thirds": "삼분할 구도, 주요 요소가 교차점에 위치, 균형 잡힌 배치",
            "golden_ratio": "황금비율 구도, 자연스러운 흐름, 조화로운 배치",
            "leading_lines": "유도선 구도, 시선을 이끄는 선, 깊이감 있는 구성",
            "framing": "프레이밍 구도, 자연적 프레임 활용, 액자 효과, 주제 강조"
        }
        
        # 조명 템플릿
        self.lighting_templates = {
            "natural": "자연광, 부드러운 햇빛, 균일한 조명, 자연스러운 그림자",
            "golden_hour": "황금빛 시간, 따뜻한 주황색 조명, 긴 그림자, 로맨틱한 분위기",
            "blue_hour": "블루 아워, 푸른 톤, 황혼, 차분한 분위기",
            "dramatic": "드라마틱한 조명, 강한 대비, 선명한 그림자, 집중 조명",
            "studio": "스튜디오 조명, 균일한 빛, 전문적인 설정, 깔끔한 배경",
            "backlight": "역광, 실루엣 효과, 빛나는 윤곽선, 신비로운 분위기",
            "neon": "네온 조명, 선명한 색상의 인공 조명, 도시적 분위기, 사이버펑크",
            "candlelight": "촛불 조명, 따뜻한 주황색 빛, 부드러운 그림자, 아늑한 분위기",
            "moonlight": "달빛, 푸른 색조, 부드러운 그림자, 신비로운 분위기"
        }
        
        # 부정적 프롬프트 템플릿
        self.negative_prompt_templates = {
            "general": "저품질, 흐릿함, 왜곡된 비율, 기형적인 특징, 비현실적인 색상, 불균형한 구도",
            "portrait": "왜곡된 얼굴, 비현실적인 피부, 기형적인 신체 비율, 흐릿한 얼굴 특징, 부자연스러운 포즈",
            "landscape": "흐릿한 배경, 불균형한 지평선, 부자연스러운 색상, 왜곡된 원근법, 비현실적인 조명",
            "product": "저품질 제품 이미지, 흐릿한 디테일, 왜곡된 제품 형태, 부자연스러운 그림자, 비현실적인 반사",
            "text": "텍스트, 글자, 워터마크, 서명, 로고, 잘못된 글자, 흐릿한 텍스트"
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        Imagen 3 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        return {
            "components": [
                "subject_description",
                "style_specification",
                "composition_details",
                "lighting_details",
                "color_palette",
                "mood_atmosphere",
                "technical_specifications",
                "negative_prompt"
            ],
            "recommended_order": [
                "subject_description",
                "style_specification",
                "composition_details",
                "lighting_details",
                "color_palette",
                "mood_atmosphere",
                "technical_specifications",
                "negative_prompt"
            ],
            "optional_components": [
                "color_palette",
                "mood_atmosphere",
                "technical_specifications",
                "negative_prompt"
            ]
        }
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 Imagen 3에 최적화된 프롬프트를 생성합니다.
        
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
        
        # 3. 구도 세부사항 생성
        composition = self._generate_composition(analysis_result, intent_result)
        
        # 4. 조명 세부사항 생성
        lighting = self._generate_lighting(analysis_result, intent_result)
        
        # 5. 색상 팔레트 생성
        color_palette = self._generate_color_palette(analysis_result, intent_result)
        
        # 6. 분위기/분위기 생성
        mood = self._generate_mood(analysis_result, intent_result)
        
        # 7. 기술적 명세 생성
        technical = self._generate_technical(analysis_result, intent_result)
        
        # 8. 부정적 프롬프트 생성
        negative = self._generate_negative_prompt(analysis_result, intent_result)
        
        # 9. 최종 프롬프트 조합
        prompt_parts = []
        
        if subject:
            prompt_parts.append(subject)
            
        if style:
            prompt_parts.append(style)
            
        if composition:
            prompt_parts.append(composition)
            
        if lighting:
            prompt_parts.append(lighting)
            
        if color_palette:
            prompt_parts.append(color_palette)
            
        if mood:
            prompt_parts.append(mood)
            
        if technical:
            prompt_parts.append(technical)
        
        # 최종 프롬프트 생성
        optimized_prompt = ", ".join(filter(None, prompt_parts))
        
        # 공통 규칙 적용
        optimized_prompt = self.apply_common_rules(optimized_prompt)
        
        # 부정적 프롬프트가 있으면 추가
        if negative:
            optimized_prompt = f"Prompt: {optimized_prompt}\nNegative prompt: {negative}"
        
        return optimized_prompt
    
    def get_generation_parameters(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Imagen 3 모델의 이미지 생성 매개변수를 반환합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            생성 매개변수를 담은 딕셔너리
        """
        # 복잡성에 따른 기본 매개변수 설정
        complexity = analysis_result.get("complexity", "medium")
        
        # 기본 생성 매개변수
        generation_params = {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "quality": "standard",
            "format": "png"
        }
        
        # 주제 유형에 따른 해상도 조정
        subject_type = self._detect_subject_type(analysis_result.get("input_text", ""))
        
        if subject_type == "portrait":
            generation_params.update({
                "width": 768,
                "height": 1024,
                "aspect_ratio": "3:4"
            })
        elif subject_type == "landscape":
            generation_params.update({
                "width": 1024,
                "height": 768,
                "aspect_ratio": "4:3"
            })
        elif subject_type == "product":
            generation_params.update({
                "width": 1024,
                "height": 1024,
                "aspect_ratio": "1:1",
                "background_removal": True
            })
        
        # 복잡성에 따른 품질 조정
        if complexity == "high":
            generation_params.update({
                "width": 1280,
                "height": 1280,
                "num_inference_steps": 75,
                "guidance_scale": 8.0,
                "quality": "premium",
                "detail_enhancement": True
            })
        elif complexity == "low":
            generation_params.update({
                "num_inference_steps": 30,
                "guidance_scale": 6.0,
                "quality": "fast"
            })
        
        # 스타일에 따른 조정
        styles = analysis_result.get("style", [])
        if styles:
            style_name = styles[0][0] if isinstance(styles[0], tuple) else styles[0]
            
            if style_name == "photorealistic":
                generation_params.update({
                    "sampler": "DPM++ 2M Karras",
                    "guidance_scale": 7.0,
                    "realism_boost": True
                })
            elif style_name == "artistic":
                generation_params.update({
                    "sampler": "Euler a",
                    "guidance_scale": 8.5,
                    "artistic_enhancement": True
                })
            elif style_name == "anime":
                generation_params.update({
                    "sampler": "DPM++ SDE Karras",
                    "guidance_scale": 9.0,
                    "anime_style": True
                })
        
        # Imagen 3 특화 매개변수
        generation_params.update({
            "text_rendering": True,
            "safety_filter": True,
            "watermark": False,
            "enhance_details": True
        })
        
        return generation_params
    
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
    
    def _generate_composition(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """구도 세부사항을 생성합니다."""
        # 구도 정보 추출
        composition = analysis_result.get("composition", "")
        
        # 구도가 명시적으로 지정된 경우
        if composition:
            # 템플릿에서 구도 찾기
            if composition in self.composition_templates:
                return self.composition_templates[composition]
            else:
                return composition
        
        # 주제 유형에 따른 기본 구도 선택
        subject_type = self._detect_subject_type(analysis_result.get("input_text", ""))
        
        if subject_type == "landscape":
            return self.composition_templates["wide_shot"]
        elif subject_type == "portrait":
            return self.composition_templates["rule_of_thirds"]
        elif subject_type == "product":
            return self.composition_templates["close_up"]
        
        # 기본 구도는 rule_of_thirds
        return self.composition_templates["rule_of_thirds"]
    
    def _generate_lighting(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """조명 세부사항을 생성합니다."""
        # 조명 정보 추출
        lighting = analysis_result.get("lighting", "")
        
        # 조명이 명시적으로 지정된 경우
        if lighting:
            # 템플릿에서 조명 찾기
            if lighting in self.lighting_templates:
                return self.lighting_templates[lighting]
            else:
                return lighting
        
        # 주제 유형에 따른 기본 조명 선택
        subject_type = self._detect_subject_type(analysis_result.get("input_text", ""))
        
        if subject_type == "landscape":
            return self.lighting_templates["golden_hour"]
        elif subject_type == "portrait":
            return self.lighting_templates["natural"]
        elif subject_type == "product":
            return self.lighting_templates["studio"]
        
        # 기본 조명은 natural
        return self.lighting_templates["natural"]
    
    def _generate_color_palette(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """색상 팔레트를 생성합니다."""
        # 색상 정보 추출
        colors = analysis_result.get("colors", [])
        
        if colors:
            # 색상 목록을 문자열로 변환
            color_text = ", ".join(colors)
            return f"색상 팔레트: {color_text}"
        
        # 분위기에 따른 기본 색상 팔레트 선택
        mood = analysis_result.get("mood", "")
        
        if mood == "warm":
            return "따뜻한 색상 팔레트, 주황색, 노란색, 빨간색 계열"
        elif mood == "cool":
            return "차가운 색상 팔레트, 파란색, 보라색, 청록색 계열"
        elif mood == "neutral":
            return "중립적인 색상 팔레트, 베이지, 회색, 갈색 계열"
        elif mood == "vibrant":
            return "선명한 색상 팔레트, 강렬한 원색, 높은 채도"
        elif mood == "pastel":
            return "파스텔 색상 팔레트, 부드러운 색조, 낮은 채도"
        
        # 기본값은 빈 문자열 (색상 팔레트 지정 안 함)
        return ""
    
    def _generate_technical(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """기술적 명세를 생성합니다."""
        # 복잡성에 따른 기술적 명세
        complexity = analysis_result.get("complexity", "medium")
        
        technical_specs = []
        
        if complexity == "high":
            technical_specs.extend([
                "8K 해상도",
                "초고해상도",
                "세밀한 디테일",
                "고품질 렌더링",
                "전문가 수준의 품질"
            ])
        elif complexity == "medium":
            technical_specs.extend([
                "고해상도",
                "상세한 묘사",
                "전문적인 품질"
            ])
        else:  # low
            technical_specs.extend([
                "표준 해상도",
                "깔끔한 이미지"
            ])
        
        # 구조 힌트에 따른 기술적 명세 추가
        structure_hints = analysis_result.get("structure_hints", {})
        if structure_hints.get("format") == "photorealistic":
            technical_specs.append("사진 사실적 렌더링")
        
        # Imagen 3 특화 기술적 명세
        technical_specs.extend([
            "Imagen 3 품질",
            "정확한 텍스트 렌더링",
            "자연스러운 색상 재현"
        ])
        
        if technical_specs:
            return ", ".join(technical_specs)
        
        return ""
    
    def _generate_mood(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """분위기를 생성합니다."""
        # 분위기 정보 추출
        moods = analysis_result.get("moods", [])
        mood_text = ""
        
        # 분위기가 명시적으로 지정된 경우
        if moods:
            if isinstance(moods[0], tuple):
                mood_name = moods[0][0]
            else:
                mood_name = moods[0]
                
            mood_text = f"분위기: {mood_name}"
        else:
            # 주제 유형에 따른 기본 분위기 선택
            subject_type = self._detect_subject_type(analysis_result.get("input_text", ""))
            
            if subject_type == "landscape":
                mood_text = "평화롭고 고요한 분위기"
            elif subject_type == "portrait":
                mood_text = "자연스럽고 친근한 분위기"
            elif subject_type == "product":
                mood_text = "전문적이고 깔끔한 분위기"
            else:
                mood_text = "균형 잡힌 분위기"
        
        return mood_text
    
    def _generate_negative_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """부정적 프롬프트를 생성합니다."""
        # 주제 유형에 따른 부정적 프롬프트 선택
        subject_type = self._detect_subject_type(analysis_result.get("input_text", ""))
        
        negative_parts = []
        
        # 기본 부정적 프롬프트
        negative_parts.append(self.negative_prompt_templates["general"])
        
        # 주제별 부정적 프롬프트 추가
        if subject_type in self.negative_prompt_templates:
            negative_parts.append(self.negative_prompt_templates[subject_type])
        
        # 복잡성에 따른 부정적 프롬프트 조정
        complexity = analysis_result.get("complexity", "medium")
        if complexity == "high":
            negative_parts.append("단순한 구성, 낮은 품질, 부정확한 묘사")
        elif complexity == "low":
            negative_parts.append("과도하게 복잡한 구성, 불필요한 세부 사항")
        
        # 제약 조건에서 텍스트 제외 요청이 있으면 텍스트 관련 부정적 프롬프트 추가
        constraints = analysis_result.get("constraints", {})
        if "텍스트" in str(constraints.get("exclude", [])):
            negative_parts.append(self.negative_prompt_templates["text"])
        
        # 중복 제거 후 결합
        unique_negative_parts = list(set(negative_parts))
        return ", ".join(unique_negative_parts)