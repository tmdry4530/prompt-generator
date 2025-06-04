"""
Sora 모델 최적화 모듈: Sora 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class SoraModel(BaseModel):
    """
    Sora 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """Sora 모델 클래스 초기화"""
        super().__init__(
            model_id="sora",
            model_name="Sora",
            provider="OpenAI"
        )
        self.capabilities = [
            "video_generation",
            "scene_transition",
            "camera_movement",
            "character_animation",
            "visual_effects",
            "narrative_control",
            "physical_simulation"
        ]
        self.max_tokens = 1000  # 프롬프트 최대 길이
        self.supports_multimodal = False
        self.best_practices = [
            "상세하고 구체적인 장면 설명 제공",
            "물리적 상호작용과 움직임 명시",
            "시각적 스타일과 분위기 설정",
            "카메라 움직임과 시점 지정",
            "시간적 흐름과 내러티브 구조화",
            "공간적 관계와 환경 설명"
        ]
        
        # Sora에 최적화된 장면 템플릿
        self.scene_templates = {
            "nature": "{location}의 자연 풍경, {time_of_day}, {weather}, {camera_movement}, {style}",
            "urban": "{location}의 도시 풍경, {time_of_day}, {activity}, {camera_movement}, {style}",
            "character": "{character}가 {action}하는 장면, {location}, {time_of_day}, {camera_movement}, {style}",
            "narrative": "{setting}에서 {character}가 {action}하고 {result}하는 이야기, {camera_movement}, {style}",
            "abstract": "{theme}을(를) 표현한 추상적 영상, {visual_elements}, {movement}, {style}",
            "physical": "{objects}의 물리적 상호작용, {forces}, {movement}, {camera_movement}, {style}",
            "fantasy": "{fantasy_setting}의 환상적인 장면, {magical_elements}, {camera_movement}, {style}"
        }
        
        # 스타일 템플릿
        self.style_templates = {
            "cinematic": "영화적인 스타일, 시네마틱한 구도, 영화 같은 색감과 조명, 영화 품질의 비주얼",
            "documentary": "다큐멘터리 스타일, 사실적인 표현, 자연스러운 조명, 관찰자적 시점",
            "animation": "애니메이션 스타일, 생동감 있는 움직임, 선명한 색상, 과장된 표현",
            "vintage": "빈티지 스타일, 필름 그레인, 레트로한 색감, 아날로그 느낌, 오래된 영화 분위기",
            "futuristic": "미래적인 스타일, 첨단 기술적 요소, 세련된 디자인, 미래 도시 분위기, 하이테크 시각 효과",
            "dreamy": "몽환적인 스타일, 부드러운 포커스, 환상적인 분위기, 꿈같은 색감, 초현실적 요소",
            "hyperrealistic": "초현실적 스타일, 극도로 세밀한 디테일, 완벽한 물리 시뮬레이션, 사실적인 질감과 조명",
            "stylized": "양식화된 스타일, 독특한 미학, 과장된 특징, 예술적 해석, 비사실적 표현",
            "minimalist": "미니멀리스트 스타일, 단순한 형태, 제한된 색상 팔레트, 깔끔한 구성, 불필요한 요소 제거",
            "fantasy": "판타지 스타일, 마법적인 요소, 초현실적인 풍경, 신비로운 분위기, 환상적인 생물과 현상"
        }
        
        # 카메라 움직임 템플릿
        self.camera_movement_templates = {
            "static": "고정된 카메라, 움직임 없음, 안정적인 프레임",
            "pan": "패닝 샷, 카메라가 수평으로 움직임, 풍경이나 환경을 보여주는 움직임",
            "tilt": "틸트 샷, 카메라가 수직으로 움직임, 위아래로 시선 이동",
            "tracking": "트래킹 샷, 카메라가 피사체를 따라 움직임, 일정한 거리 유지",
            "dolly": "돌리 샷, 카메라가 앞뒤로 움직임, 피사체에 접근하거나 멀어짐",
            "zoom": "줌 샷, 카메라가 확대/축소됨, 시점 변화 없이 시야 조정",
            "aerial": "항공 샷, 위에서 내려다보는 시점, 넓은 풍경이나 환경 조망",
            "crane": "크레인 샷, 카메라가 위아래로 움직임, 높은 곳에서 낮은 곳으로 이동",
            "steadicam": "스테디캠 샷, 부드럽게 움직이는 카메라, 자연스러운 시점 이동",
            "handheld": "핸드헬드 샷, 약간 흔들리는 카메라, 현실감과 긴장감 부여"
        }
        
        # 물리적 상호작용 템플릿
        self.physical_interaction_templates = {
            "gravity": "중력에 의한 자연스러운 낙하, 물체가 땅으로 떨어짐",
            "collision": "물체 간의 충돌, 충격과 반동, 물리적 상호작용",
            "fluid": "유체의 흐름과 움직임, 물, 연기, 안개 등의 자연스러운 시뮬레이션",
            "wind": "바람에 의한 움직임, 나뭇잎, 머리카락, 옷 등이 바람에 흔들림",
            "deformation": "물체의 변형, 구부러짐, 찌그러짐, 늘어남 등의 물리적 변화",
            "particle": "입자 효과, 먼지, 불꽃, 빗방울 등의 미세한 입자 움직임",
            "soft_body": "부드러운 물체의 움직임, 천, 젤리, 고무 등의 자연스러운 변형",
            "rigid_body": "단단한 물체의 움직임, 돌, 금속, 나무 등의 물리적 상호작용",
            "chain_reaction": "연쇄 반응, 도미노 효과, 하나의 움직임이 다른 움직임을 유발"
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        Sora 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        return {
            "components": [
                "scene_description",
                "physical_interactions",
                "camera_movements",
                "visual_style",
                "temporal_flow",
                "spatial_relationships",
                "lighting_atmosphere",
                "technical_specifications"
            ],
            "recommended_order": [
                "scene_description",
                "physical_interactions",
                "camera_movements",
                "visual_style",
                "temporal_flow",
                "spatial_relationships",
                "lighting_atmosphere",
                "technical_specifications"
            ],
            "optional_components": [
                "physical_interactions",
                "temporal_flow",
                "spatial_relationships",
                "lighting_atmosphere",
                "technical_specifications"
            ]
        }
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 Sora에 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        # 1. 장면 설명 생성
        scene = self._generate_scene(analysis_result, intent_result)
        
        # 2. 물리적 상호작용 생성
        physics = self._generate_physics(analysis_result, intent_result)
        
        # 3. 카메라 움직임 생성
        camera = self._generate_camera_movements(analysis_result, intent_result)
        
        # 4. 시각적 스타일 생성
        style = self._generate_style(analysis_result, intent_result)
        
        # 5. 시간적 흐름 생성
        temporal = self._generate_temporal_flow(analysis_result, intent_result)
        
        # 6. 공간적 관계 생성
        spatial = self._generate_spatial_relationships(analysis_result, intent_result)
        
        # 7. 조명과 분위기 생성
        lighting = self._generate_lighting(analysis_result, intent_result)
        
        # 8. 기술적 명세 생성
        technical = self._generate_technical(analysis_result, intent_result)
        
        # 9. 최종 프롬프트 조합
        # Sora는 단일 문단 형식의 상세한 설명을 선호함
        prompt_parts = []
        
        # 장면 설명 (필수)
        if scene:
            prompt_parts.append(scene)
        
        # 물리적 상호작용
        if physics:
            prompt_parts.append(physics)
        
        # 카메라 움직임
        if camera:
            prompt_parts.append(camera)
        
        # 시각적 스타일
        if style:
            prompt_parts.append(style)
        
        # 시간적 흐름
        if temporal:
            prompt_parts.append(temporal)
        
        # 공간적 관계
        if spatial:
            prompt_parts.append(spatial)
        
        # 조명과 분위기
        if lighting:
            prompt_parts.append(lighting)
        
        # 기술적 명세
        if technical:
            prompt_parts.append(technical)
        
        # 최종 프롬프트 생성 (단일 문단)
        optimized_prompt = " ".join(filter(None, prompt_parts))
        
        # 공통 규칙 적용
        optimized_prompt = self.apply_common_rules(optimized_prompt)
        
        return optimized_prompt
    
    def get_generation_parameters(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sora 모델의 비디오 생성 매개변수를 반환합니다.
        
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
            "duration": 15,  # 기본 15초
            "resolution": "1024x576",
            "fps": 24,
            "quality": "high",
            "format": "mp4"
        }
        
        # 복잡성에 따른 조정
        if complexity == "high":
            generation_params.update({
                "duration": 30,  # 30초
                "resolution": "1280x720",
                "quality": "ultra",
                "camera_movements": ["pan", "zoom", "track"],
                "scene_complexity": "high"
            })
        elif complexity == "low":
            generation_params.update({
                "duration": 10,  # 10초
                "resolution": "720x480",
                "camera_movements": ["static"],
                "scene_complexity": "simple"
            })
        else:  # medium
            generation_params.update({
                "duration": 15,  # 15초
                "camera_movements": ["pan", "zoom"],
                "scene_complexity": "medium"
            })
        
        # 스타일에 따른 조정
        styles = analysis_result.get("style", [])
        if styles:
            style_name = styles[0][0] if isinstance(styles[0], tuple) else styles[0]
            
            if style_name == "cinematic":
                generation_params.update({
                    "fps": 30,
                    "aspect_ratio": "16:9",
                    "color_grading": "cinematic"
                })
            elif style_name == "anime":
                generation_params.update({
                    "style": "animated",
                    "frame_rate": "12"
                })
            elif style_name == "photorealistic":
                generation_params.update({
                    "realism": "high",
                    "physics": "accurate"
                })
        
        # 비디오 특화 매개변수 추가
        generation_params.update({
            "temporal_consistency": True,
            "physics_simulation": True,
            "character_consistency": True,
            "scene_transitions": "smooth"
        })
        
        return generation_params
    
    def _generate_scene(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """장면 설명을 생성합니다."""
        # 기본 장면 설명
        input_text = analysis_result.get("input_text", "")
        
        # 장면 유형 감지
        scene_type = self._detect_scene_type(input_text)
        
        # 장면 세부 정보 추출
        scene_details = self._extract_scene_details(input_text, scene_type)
        
        # 장면 템플릿 선택 및 적용
        if scene_type in self.scene_templates:
            template = self.scene_templates[scene_type]
            
            # 템플릿 변수 채우기
            for key, value in scene_details.items():
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
    
    def _detect_scene_type(self, text: str) -> str:
        """입력 텍스트에서 장면 유형을 감지합니다."""
        # 간단한 키워드 기반 감지 (실제로는 더 복잡한 분류 로직 필요)
        keywords = {
            "nature": ["자연", "풍경", "산", "바다", "호수", "숲", "하늘", "일몰", "일출"],
            "urban": ["도시", "거리", "건물", "도로", "교통", "사람들", "번화가"],
            "character": ["인물", "사람", "캐릭터", "행동", "활동", "움직임"],
            "narrative": ["이야기", "스토리", "내러티브", "플롯", "사건", "전개"],
            "abstract": ["추상", "비현실적", "예술적", "실험적", "개념적"],
            "physical": ["물리", "중력", "충돌", "폭발", "낙하", "물", "유체", "역학"],
            "fantasy": ["판타지", "마법", "초현실", "환상", "신비", "초자연적"]
        }
        
        # 텍스트를 소문자로 변환
        text_lower = text.lower()
        
        # 각 유형별 키워드 매칭 점수 계산
        scores = {}
        for scene_type, type_keywords in keywords.items():
            score = sum(1 for keyword in type_keywords if keyword in text_lower)
            scores[scene_type] = score
        
        # 가장 높은 점수의 유형 반환
        if scores:
            max_type = max(scores.items(), key=lambda x: x[1])
            if max_type[1] > 0:
                return max_type[0]
        
        # 기본값은 narrative
        return "narrative"
    
    def _extract_scene_details(self, text: str, scene_type: str) -> Dict[str, str]:
        """입력 텍스트에서 장면 세부 정보를 추출합니다."""
        # 기본 세부 정보
        details = {}
        
        # 장면 유형별 추가 세부 정보
        if scene_type == "nature":
            # 위치 추출
            location_patterns = ["산", "바다", "호수", "숲", "강", "계곡", "해변", "들판", "사막"]
            for pattern in location_patterns:
                if pattern in text:
                    details["location"] = pattern
                    break
            
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
            
            # 카메라 움직임 추출
            camera_patterns = ["패닝", "틸트", "줌", "트래킹", "고정", "항공", "드론"]
            for pattern in camera_patterns:
                if pattern in text:
                    details["camera_movement"] = pattern
                    break
            
            # 스타일 추출
            style_patterns = ["영화적", "다큐멘터리", "타임랩스", "슬로우 모션", "드라마틱"]
            for pattern in style_patterns:
                if pattern in text:
                    details["style"] = pattern
                    break
        
        elif scene_type == "physical":
            # 물체 추출
            object_patterns = ["공", "물", "액체", "불", "연기", "돌", "나무", "금속", "유리"]
            for pattern in object_patterns:
                if pattern in text:
                    details["objects"] = pattern
                    break
            
            # 힘 추출
            force_patterns = ["중력", "충돌", "폭발", "바람", "압력", "마찰", "탄성"]
            for pattern in force_patterns:
                if pattern in text:
                    details["forces"] = pattern
                    break
            
            # 움직임 추출
            movement_patterns = ["낙하", "회전", "진동", "흐름", "튕김", "충돌", "폭발"]
            for pattern in movement_patterns:
                if pattern in text:
                    details["movement"] = pattern
                    break
            
            # 카메라 움직임 추출
            camera_patterns = ["패닝", "틸트", "줌", "트래킹", "고정", "슬로우 모션"]
            for pattern in camera_patterns:
                if pattern in text:
                    details["camera_movement"] = pattern
                    break
            
            # 스타일 추출
            style_patterns = ["사실적", "과학적", "초현실적", "영화적", "실험적"]
            for pattern in style_patterns:
                if pattern in text:
                    details["style"] = pattern
                    break
        
        # 다른 장면 유형에 대한 세부 정보 추출 로직 추가 가능
        
        # 기본 설명 추가
        details["description"] = text
        
        return details
    
    def _generate_physics(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """물리적 상호작용을 생성합니다."""
        # 물리적 상호작용 정보 추출
        physics = analysis_result.get("physics", [])
        
        # 물리적 상호작용이 명시적으로 지정된 경우
        if physics:
            physics_texts = []
            for interaction in physics:
                if interaction in self.physical_interaction_templates:
                    physics_texts.append(self.physical_interaction_templates[interaction])
                else:
                    physics_texts.append(interaction)
            
            return "물리적 상호작용: " + ", ".join(physics_texts)
        
        # 장면 유형에 따른 기본 물리적 상호작용 선택
        scene_type = self._detect_scene_type(analysis_result.get("input_text", ""))
        
        if scene_type == "nature":
            return "자연스러운 물리적 상호작용: 나뭇잎이 바람에 흔들리고, 물이 자연스럽게 흐르며, 빛이 표면에 반사됩니다."
        elif scene_type == "urban":
            return "도시 환경의 물리적 상호작용: 사람들의 자연스러운 움직임, 차량의 흐름, 빛이 건물 표면에 반사됩니다."
        elif scene_type == "physical":
            return "정확한 물리 시뮬레이션: 중력에 의한 자연스러운 낙하, 물체 간의 사실적인 충돌과 반응, 관성과 마찰력의 영향이 명확하게 표현됩니다."
        
        # 기본 물리적 상호작용
        return "사실적인 물리 법칙을 따르는 자연스러운 움직임과 상호작용"
    
    def _generate_camera_movements(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """카메라 움직임을 생성합니다."""
        # 카메라 움직임 정보 추출
        camera_movements = analysis_result.get("camera_movements", [])
        
        # 카메라 움직임이 명시적으로 지정된 경우
        if camera_movements:
            movement_texts = []
            for movement in camera_movements:
                if movement in self.camera_movement_templates:
                    movement_texts.append(self.camera_movement_templates[movement])
                else:
                    movement_texts.append(movement)
            
            return "카메라 움직임: " + ", ".join(movement_texts)
        
        # 장면 유형에 따른 기본 카메라 움직임 선택
        scene_type = self._detect_scene_type(analysis_result.get("input_text", ""))
        
        if scene_type == "nature":
            return "부드러운 패닝 샷으로 자연 풍경을 보여주고, 중간에 드론 항공 샷으로 넓은 시야를 제공합니다."
        elif scene_type == "urban":
            return "도시 풍경을 보여주는 크레인 샷으로 시작하여, 트래킹 샷으로 거리의 활동을 따라갑니다."
        elif scene_type == "character":
            return "캐릭터를 따라가는 부드러운 트래킹 샷, 감정을 강조하는 클로즈업 샷이 포함됩니다."
        elif scene_type == "physical":
            return "물리적 상호작용을 명확히 보여주는 최적의 각도, 중요한 순간에는 슬로우 모션으로 세부 사항을 강조합니다."
        
        # 기본 카메라 움직임
        return "영상의 내용과 분위기에 맞는 자연스러운 카메라 움직임"
    
    def _generate_style(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """시각적 스타일을 생성합니다."""
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
        
        return style_text
    
    def _generate_temporal_flow(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """시간적 흐름을 생성합니다."""
        # 시간적 흐름 정보 추출
        temporal_flow = analysis_result.get("temporal_flow", [])
        
        # 시간적 흐름이 명시적으로 지정된 경우