"""
Google Veo 3 모델 최적화 모듈: Google Veo 3 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class GoogleVeo3Model(BaseModel):
    """
    Google Veo 3 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """Google Veo 3 모델 클래스 초기화"""
        super().__init__(
            model_id="google-veo-3",
            model_name="Google Veo 3",
            provider="Google"
        )
        self.capabilities = [
            "video_generation",
            "scene_transition",
            "camera_movement",
            "character_animation",
            "visual_effects",
            "narrative_control"
        ]
        self.max_tokens = 1500  # 프롬프트 최대 길이
        self.supports_multimodal = False
        self.best_practices = [
            "명확한 장면 설명 제공",
            "카메라 움직임과 전환 명시",
            "시간적 흐름과 내러티브 구조화",
            "시각적 스타일과 분위기 설정",
            "캐릭터 동작과 상호작용 설명",
            "장면별 세부 사항 제공"
        ]
        
        # Google Veo 3에 최적화된 장면 템플릿
        self.scene_templates = {
            "nature": "{location}의 자연 풍경, {time_of_day}, {weather}, {camera_movement}, {style}",
            "urban": "{location}의 도시 풍경, {time_of_day}, {activity}, {camera_movement}, {style}",
            "character": "{character}가 {action}하는 장면, {location}, {time_of_day}, {camera_movement}, {style}",
            "narrative": "{setting}에서 {character}가 {action}하고 {result}하는 이야기, {camera_movement}, {style}",
            "abstract": "{theme}을(를) 표현한 추상적 영상, {visual_elements}, {movement}, {style}",
            "product": "{product_name} 제품 영상, {product_details}, {background}, {camera_movement}, {style}",
            "travel": "{location} 여행 영상, {landmarks}, {activities}, {camera_movement}, {style}"
        }
        
        # 스타일 템플릿
        self.style_templates = {
            "cinematic": "영화적인 스타일, 시네마틱한 구도, 영화 같은 색감과 조명",
            "documentary": "다큐멘터리 스타일, 사실적인 표현, 자연스러운 조명",
            "animation": "애니메이션 스타일, 생동감 있는 움직임, 선명한 색상",
            "vintage": "빈티지 스타일, 필름 그레인, 레트로한 색감, 아날로그 느낌",
            "futuristic": "미래적인 스타일, 첨단 기술적 요소, 세련된 디자인, 미래 도시 분위기",
            "dreamy": "몽환적인 스타일, 부드러운 포커스, 환상적인 분위기, 꿈같은 색감",
            "aerial": "항공 촬영 스타일, 드론 시점, 넓은 풍경, 부드러운 움직임",
            "timelapse": "타임랩스 스타일, 시간의 흐름 압축, 빠른 움직임, 자연스러운 전환",
            "slowmotion": "슬로우 모션 스타일, 느린 움직임, 세부 동작 강조, 드라마틱한 효과",
            "handheld": "핸드헬드 스타일, 약간의 흔들림, 다큐멘터리 느낌, 현장감"
        }
        
        # 카메라 움직임 템플릿
        self.camera_movement_templates = {
            "static": "고정된 카메라, 움직임 없음",
            "pan": "패닝 샷, 카메라가 수평으로 움직임",
            "tilt": "틸트 샷, 카메라가 수직으로 움직임",
            "tracking": "트래킹 샷, 카메라가 피사체를 따라 움직임",
            "dolly": "돌리 샷, 카메라가 앞뒤로 움직임",
            "zoom": "줌 샷, 카메라가 확대/축소됨",
            "aerial": "항공 샷, 위에서 내려다보는 시점",
            "crane": "크레인 샷, 카메라가 위아래로 움직임",
            "steadicam": "스테디캠 샷, 부드럽게 움직이는 카메라",
            "handheld": "핸드헬드 샷, 약간 흔들리는 카메라"
        }
        
        # 전환 템플릿
        self.transition_templates = {
            "cut": "컷 전환, 즉각적인 장면 변화",
            "fade": "페이드 전환, 점진적으로 어두워지거나 밝아짐",
            "dissolve": "디졸브 전환, 장면이 서서히 겹쳐짐",
            "wipe": "와이프 전환, 한 장면이 다른 장면을 밀어냄",
            "zoom": "줌 전환, 확대/축소를 통한 장면 변화",
            "whip_pan": "휩 팬 전환, 빠른 패닝을 통한 장면 변화",
            "morph": "모프 전환, 한 형태가 다른 형태로 변형됨",
            "match_cut": "매치 컷 전환, 유사한 구도나 동작으로 연결",
            "time_lapse": "타임랩스 전환, 시간의 흐름을 압축",
            "slow_motion": "슬로우 모션 전환, 시간을 늘려 세부 동작 강조"
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        Google Veo 3 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        return {
            "components": [
                "video_concept",
                "scene_descriptions",
                "camera_movements",
                "transitions",
                "visual_style",
                "audio_description",
                "narrative_flow",
                "technical_specifications"
            ],
            "recommended_order": [
                "video_concept",
                "scene_descriptions",
                "camera_movements",
                "transitions",
                "visual_style",
                "audio_description",
                "narrative_flow",
                "technical_specifications"
            ],
            "optional_components": [
                "audio_description",
                "narrative_flow",
                "technical_specifications"
            ]
        }
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 Google Veo 3에 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        # 1. 비디오 컨셉 생성
        concept = self._generate_concept(analysis_result, intent_result)
        
        # 2. 장면 설명 생성
        scenes = self._generate_scenes(analysis_result, intent_result)
        
        # 3. 카메라 움직임 생성
        camera = self._generate_camera_movements(analysis_result, intent_result)
        
        # 4. 전환 생성
        transitions = self._generate_transitions(analysis_result, intent_result)
        
        # 5. 시각적 스타일 생성
        style = self._generate_style(analysis_result, intent_result)
        
        # 6. 오디오 설명 생성
        audio = self._generate_audio(analysis_result, intent_result)
        
        # 7. 내러티브 흐름 생성
        narrative = self._generate_narrative(analysis_result, intent_result)
        
        # 8. 기술적 명세 생성
        technical = self._generate_technical(analysis_result, intent_result)
        
        # 9. 최종 프롬프트 조합
        prompt_parts = []
        
        # 비디오 컨셉
        if concept:
            prompt_parts.append(f"비디오 컨셉: {concept}")
        
        # 장면 설명
        if scenes:
            prompt_parts.append(f"장면 설명: {scenes}")
        
        # 카메라 움직임
        if camera:
            prompt_parts.append(f"카메라 움직임: {camera}")
        
        # 전환
        if transitions:
            prompt_parts.append(f"전환: {transitions}")
        
        # 시각적 스타일
        if style:
            prompt_parts.append(f"시각적 스타일: {style}")
        
        # 오디오 설명
        if audio:
            prompt_parts.append(f"오디오: {audio}")
        
        # 내러티브 흐름
        if narrative:
            prompt_parts.append(f"내러티브: {narrative}")
        
        # 기술적 명세
        if technical:
            prompt_parts.append(f"기술적 명세: {technical}")
        
        # 최종 프롬프트 생성
        optimized_prompt = "\n\n".join(filter(None, prompt_parts))
        
        # 공통 규칙 적용
        optimized_prompt = self.apply_common_rules(optimized_prompt)
        
        return optimized_prompt
    
    def _generate_concept(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """비디오 컨셉을 생성합니다."""
        # 기본 컨셉 설명
        input_text = analysis_result.get("input_text", "")
        
        # 컨셉 유형 감지
        concept_type = self._detect_concept_type(input_text)
        
        # 컨셉 세부 정보 추출
        concept_details = self._extract_concept_details(input_text, concept_type)
        
        # 컨셉 템플릿 선택 및 적용
        if concept_type in self.scene_templates:
            template = self.scene_templates[concept_type]
            
            # 템플릿 변수 채우기
            for key, value in concept_details.items():
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
    
    def _detect_concept_type(self, text: str) -> str:
        """입력 텍스트에서 컨셉 유형을 감지합니다."""
        # 간단한 키워드 기반 감지 (실제로는 더 복잡한 분류 로직 필요)
        keywords = {
            "nature": ["자연", "풍경", "산", "바다", "호수", "숲", "하늘", "일몰", "일출"],
            "urban": ["도시", "거리", "건물", "도로", "교통", "사람들", "번화가"],
            "character": ["인물", "사람", "캐릭터", "행동", "활동", "움직임"],
            "narrative": ["이야기", "스토리", "내러티브", "플롯", "사건", "전개"],
            "abstract": ["추상", "비현실적", "예술적", "실험적", "개념적"],
            "product": ["제품", "상품", "광고", "홍보", "마케팅", "브랜드"],
            "travel": ["여행", "관광", "탐험", "모험", "방문", "명소", "랜드마크"]
        }
        
        # 텍스트를 소문자로 변환
        text_lower = text.lower()
        
        # 각 유형별 키워드 매칭 점수 계산
        scores = {}
        for concept_type, type_keywords in keywords.items():
            score = sum(1 for keyword in type_keywords if keyword in text_lower)
            scores[concept_type] = score
        
        # 가장 높은 점수의 유형 반환
        if scores:
            max_type = max(scores.items(), key=lambda x: x[1])
            if max_type[1] > 0:
                return max_type[0]
        
        # 기본값은 narrative
        return "narrative"
    
    def _extract_concept_details(self, text: str, concept_type: str) -> Dict[str, str]:
        """입력 텍스트에서 컨셉 세부 정보를 추출합니다."""
        # 기본 세부 정보
        details = {}
        
        # 컨셉 유형별 추가 세부 정보
        if concept_type == "nature":
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
        
        elif concept_type == "character":
            # 캐릭터 추출
            character_patterns = ["사람", "남자", "여자", "아이", "노인", "학생", "전문가", "운동선수", "예술가"]
            for pattern in character_patterns:
                if pattern in text:
                    details["character"] = pattern
                    break
            
            # 행동 추출
            action_patterns = ["걷는", "뛰는", "앉아있는", "서있는", "말하는", "웃는", "일하는", "놀고 있는"]
            for pattern in action_patterns:
                if pattern in text:
                    details["action"] = pattern
                    break
            
            # 위치 추출
            location_patterns = ["실내", "실외", "도시", "자연", "사무실", "집", "공원", "거리"]
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
            
            # 카메라 움직임 추출
            camera_patterns = ["패닝", "틸트", "줌", "트래킹", "고정", "핸드헬드"]
            for pattern in camera_patterns:
                if pattern in text:
                    details["camera_movement"] = pattern
                    break
            
            # 스타일 추출
            style_patterns = ["영화적", "다큐멘터리", "드라마틱", "자연스러운", "스타일리시"]
            for pattern in style_patterns:
                if pattern in text:
                    details["style"] = pattern
                    break
        
        # 다른 컨셉 유형에 대한 세부 정보 추출 로직 추가 가능
        
        # 기본 설명 추가
        details["description"] = text
        
        return details
    
    def _generate_scenes(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """장면 설명을 생성합니다."""
        # 기본 장면 설명
        input_text = analysis_result.get("input_text", "")
        
        # 장면 수 결정 (기본값은 3)
        scene_count = min(analysis_result.get("scene_count", 3), 5)
        
        # 컨셉 유형 감지
        concept_type = self._detect_concept_type(input_text)
        
        # 장면 설명 생성
        scenes = []
        
        if concept_type == "nature":
            scenes = [
                "장면 1: 넓은 풍경 샷으로 시작, 자연의 아름다움을 보여줌",
                "장면 2: 세부적인 자연 요소에 집중, 클로즈업 샷으로 디테일 강조",
                "장면 3: 시간의 흐름을 보여주는 타임랩스, 자연의 변화 표현"
            ]
        elif concept_type == "urban":
            scenes = [
                "장면 1: 도시 스카이라인을 보여주는 와이드 샷, 도시의 규모와 활기를 표현",
                "장면 2: 거리의 사람들과 활동에 집중, 도시 생활의 역동성 포착",
                "장면 3: 도시의 특징적인 랜드마크나 건축물 클로즈업, 도시의 정체성 강조"
            ]
        elif concept_type == "character":
            scenes = [
                "장면 1: 캐릭터 소개, 환경과 상황 설정",
                "장면 2: 캐릭터의 주요 활동이나 행동 표현",
                "장면 3: 캐릭터의 감정이나 반응에 집중한 클로즈업"
            ]
        elif concept_type == "narrative":
            scenes = [
                "장면 1: 이야기의 배경과 주요 인물 소개",
                "장면 2: 주요 사건이나 갈등 전개",
                "장면 3: 이야기의 절정이나 해결 과정"
            ]
        elif concept_type == "product":
            scenes = [
                "장면 1: 제품 전체 모습을 보여주는 와이드 샷",
                "장면 2: 제품의 주요 기능이나 특징을 강조하는 클로즈업",
                "장면 3: 제품 사용 장면이나 효과를 보여주는 실용적 샷"
            ]
        else:
            scenes = [
                "장면 1: 주제 소개와 전체적인 분위기 설정",
                "장면 2: 주요 요소나 활동에 집중",
                "장면 3: 마무리와 결론을 제시하는 장면"
            ]
        
        # 장면 수에 맞게 조정
        scenes = scenes[:scene_count]
        
        # 장면 설명 조합
        return "\n".join(scenes)
    
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
            
            return ", ".join(movement_texts)
        
        # 컨셉 유형에 따른 기본 카메라 움직임 선택
        concept_type = self._detect_concept_type(analysis_result.get("input_text", ""))
        
        if concept_type == "nature":
            return "부드러운 패닝 샷으로 풍경을 보여주고, 중간에 드론 항공 샷을 통해 넓은 시야를 제공, 마지막에는 세부 요소에 대한 클로즈업 샷"
        elif concept_type == "urban":
            return "도시 스카이라인을 보여주는 크레인 샷으로 시작, 트래킹 샷으로 거리의 활동을 따라가고, 스테디캠으로 부드럽게 움직이며 도시 생활 포착"
        elif concept_type == "character":
            return "캐릭터를 소개하는 미디엄 샷으로 시작, 캐릭터의 행동을 따라가는 트래킹 샷, 감정을 강조하는 클로즈업 샷"
        elif concept_type == "narrative":
            return "장면 설정을 위한 와이드 샷, 이야기 전개에 따른 다양한 카메라 움직임, 중요한 순간에는 슬로우 모션과 클로즈업 활용"
        elif concept_type == "product":
            return "제품 전체 모습을 보여주는 와이드 샷, 제품의 주요 기능이나 특징을 강조하는 클로즈업, 제품 사용 장면이나 효과를 보여주는 실용적 샷"
        else:
            return "주제 소개를 위한 와이드 샷, 주요 요소나 활동에 집중하는 클로즈업, 마무리를 위한 와이드 샷"
    
    def _generate_transitions(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """전환을 생성합니다."""
        # 전환 정보 추출
        transitions = analysis_result.get("transitions", [])
        
        # 전환이 명시적으로 지정된 경우