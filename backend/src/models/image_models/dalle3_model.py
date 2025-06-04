"""
DALL-E 3 모델 최적화 모듈: DALL-E 3 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class DALLE3Model(BaseModel):
    """
    DALL-E 3 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """DALL-E 3 모델 클래스 초기화"""
        super().__init__(
            model_id="dalle-3",
            model_name="DALL-E 3",
            provider="OpenAI"
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
            "상세하고 구체적인 설명 제공",
            "시각적 요소 명확히 설명",
            "구도와 시점 지정",
            "스타일과 분위기 명시",
            "참조 아티스트나 스타일 언급",
            "간결하고 명확한 문장 사용"
        ]
        
        # DALL-E 3에 최적화된 주제 템플릿
        self.subject_templates = {
            "landscape": "{description}의 풍경, {time_of_day}, {weather}, {perspective}",
            "portrait": "{description}의 인물 사진, {pose}, {expression}, {lighting}, {background}",
            "product": "{product_name} 제품 사진, {product_details}, {background}, {lighting}, {angle}",
            "concept_art": "{concept_description}의 컨셉 아트, {style}, {mood}, {color_palette}",
            "abstract": "{theme}을(를) 주제로 한 추상 이미지, {style}, {color_palette}, {texture}, {composition}",
            "architecture": "{building_type} 건축물, {architectural_style}, {materials}, {surroundings}, {time_of_day}",
            "food": "{food_name} 음식 사진, {presentation}, {garnish}, {plating}, {background}, {lighting}"
        }
        
        # 스타일 템플릿
        self.style_templates = {
            "photorealistic": "포토리얼리스틱한 스타일, 고해상도, 세밀한 디테일, 사실적인 조명과 그림자",
            "cinematic": "영화적인 스타일, 시네마틱한 구도, 드라마틱한 조명, 영화 장면 같은 분위기",
            "anime": "애니메이션 스타일, 선명한 윤곽선, 밝은 색상, 만화적 표현",
            "digital_art": "디지털 아트 스타일, 세밀한 디테일, 풍부한 색감, 컴퓨터 그래픽",
            "oil_painting": "유화 스타일, 두꺼운 붓 터치, 질감이 느껴지는 캔버스, 고전적인 유화 기법",
            "watercolor": "수채화 스타일, 투명한 색감, 부드러운 경계, 물감이 번지는 효과",
            "3d_render": "3D 렌더링 스타일, 정교한 모델링, 사실적인 텍스처, 볼륨감 있는 조명",
            "pixel_art": "픽셀 아트 스타일, 레트로 게임 그래픽, 제한된 색 팔레트, 픽셀화된 디테일",
            "minimalist": "미니멀리스트 스타일, 단순한 형태, 제한된 색상, 깔끔한 구성",
            "fantasy": "판타지 스타일, 마법적인 요소, 초현실적인 풍경, 신비로운 분위기"
        }
        
        # 구도 템플릿
        self.composition_templates = {
            "wide_shot": "와이드 샷, 넓은 시야, 전체 장면 포착",
            "close_up": "클로즈업, 세부 디테일 강조, 근접 촬영",
            "aerial_view": "조감도, 위에서 내려다보는 시점, 드론 시점",
            "dutch_angle": "더치 앵글, 기울어진 구도, 역동적인 느낌",
            "symmetrical": "대칭 구도, 균형 잡힌 배치, 중앙 정렬",
            "rule_of_thirds": "삼분할 구도, 주요 요소가 교차점에 위치",
            "golden_ratio": "황금비율 구도, 자연스러운 흐름, 조화로운 배치",
            "leading_lines": "유도선 구도, 시선을 이끄는 선, 깊이감 있는 구성",
            "framing": "프레이밍 구도, 자연적 프레임 활용, 액자 효과"
        }
        
        # 조명 템플릿
        self.lighting_templates = {
            "natural": "자연광, 부드러운 햇빛, 균일한 조명",
            "golden_hour": "황금빛 시간, 따뜻한 주황색 조명, 긴 그림자",
            "blue_hour": "블루 아워, 푸른 톤, 황혼, 차분한 분위기",
            "dramatic": "드라마틱한 조명, 강한 대비, 선명한 그림자",
            "studio": "스튜디오 조명, 균일한 빛, 전문적인 설정",
            "backlight": "역광, 실루엣 효과, 빛나는 윤곽선",
            "neon": "네온 조명, 선명한 색상의 인공 조명, 도시적 분위기",
            "candlelight": "촛불 조명, 따뜻한 주황색 빛, 부드러운 그림자",
            "moonlight": "달빛, 푸른 색조, 부드러운 그림자, 신비로운 분위기"
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        DALL-E 3 모델에 최적화된 프롬프트 구조를 반환합니다.
        
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
                "technical_specifications"
            ],
            "recommended_order": [
                "subject_description",
                "style_specification",
                "composition_details",
                "lighting_details",
                "color_palette",
                "mood_atmosphere",
                "technical_specifications"
            ],
            "optional_components": [
                "color_palette",
                "mood_atmosphere",
                "technical_specifications"
            ]
        }
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 DALL-E 3에 최적화된 프롬프트를 생성합니다.
        
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
        
        # 8. 최종 프롬프트 조합
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
        
        return optimized_prompt
    
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
    
    def _generate_mood(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """분위기/분위기를 생성합니다."""
        # 분위기 정보 추출
        mood = analysis_result.get("mood", "")
        
        if mood:
            mood_map = {
                "warm": "따뜻한 분위기, 아늑한 느낌",
                "cool": "차가운 분위기, 시원한 느낌",
                "peaceful": "평화로운 분위기, 고요한 느낌",
                "dramatic": "드라마틱한 분위기, 강렬한 느낌",
                "mysterious": "신비로운 분위기, 비밀스러운 느낌",
                "romantic": "로맨틱한 분위기, 감성적인 느낌",
                "energetic": "활기찬 분위기, 역동적인 느낌",
                "nostalgic": "노스탤직한 분위기, 향수를 불러일으키는 느낌",
                "futuristic": "미래적인 분위기, 첨단 기술적인 느낌",
                "vintage": "빈티지한 분위기, 클래식한 느낌"
            }
            
            return mood_map.get(mood, mood)
        
        # 기본값은 빈 문자열 (분위기 지정 안 함)
        return ""
    
    def _generate_technical(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """기술적 명세를 생성합니다."""
        technical_parts = []

        # 해상도 설정
        resolution = analysis_result.get("resolution", "1024x1024")
        technical_parts.append(f"해상도: {resolution}")
        
        # 품질 설정
        quality = analysis_result.get("quality", "standard")
        technical_parts.append(f"품질: {quality}")
        
        # 프레임 설정
        frame_rate = analysis_result.get("frame_rate", "24fps")
        technical_parts.append(f"프레임 속도: {frame_rate}")