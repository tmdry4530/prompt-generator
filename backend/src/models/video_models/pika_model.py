"""
Pika 모델 최적화 모듈: Pika 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class PikaModel(BaseModel):
    """
    Pika 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """Pika 모델 클래스 초기화"""
        super().__init__(
            model_id="pika",
            model_name="Pika",
            provider="Pika Labs"
        )
        self.capabilities = [
            "video_generation",
            "scene_transition",
            "camera_movement",
            "character_animation",
            "visual_effects",
            "style_transfer",
            "music_sync"
        ]
        self.max_tokens = 800  # 프롬프트 최대 길이
        self.supports_multimodal = True
        self.best_practices = [
            "명확하고 구체적인 장면 설명 제공",
            "시각적 스타일과 참조 이미지 활용",
            "카메라 움직임과 전환 명시",
            "음악과 비디오 동기화 지정",
            "캐릭터 동작과 표현 설명",
            "시각적 효과와 분위기 설정"
        ]
        
        # Pika에 최적화된 장면 템플릿
        self.scene_templates = {
            "nature": "{location}의 자연 풍경, {time_of_day}, {weather}, {camera_movement}, {style}",
            "urban": "{location}의 도시 풍경, {time_of_day}, {activity}, {camera_movement}, {style}",
            "character": "{character}가 {action}하는 장면, {location}, {time_of_day}, {camera_movement}, {style}",
            "music_video": "{music_style} 음악에 맞춘 {theme} 영상, {visual_elements}, {camera_movement}, {style}",
            "abstract": "{theme}을(를) 표현한 추상적 영상, {visual_elements}, {movement}, {style}",
            "product": "{product_name} 제품 영상, {product_details}, {background}, {camera_movement}, {style}",
            "animation": "{animation_style} 스타일의 애니메이션, {character}, {action}, {setting}, {style}"
        }
        
        # 스타일 템플릿
        self.style_templates = {
            "cinematic": "영화적인 스타일, 시네마틱한 구도, 영화 같은 색감과 조명",
            "anime": "애니메이션 스타일, 선명한 윤곽선, 생동감 있는 색상, 2D 애니메이션 느낌",
            "3d_animation": "3D 애니메이션 스타일, 입체적인 모델링, 부드러운 텍스처, 컴퓨터 그래픽스",
            "vintage": "빈티지 스타일, 필름 그레인, 레트로한 색감, 아날로그 느낌",
            "futuristic": "미래적인 스타일, 첨단 기술적 요소, 세련된 디자인, 네온 색상, 홀로그램 효과",
            "dreamy": "몽환적인 스타일, 부드러운 포커스, 환상적인 분위기, 꿈같은 색감",
            "stylized": "양식화된 스타일, 독특한 미학, 과장된 특징, 예술적 해석",
            "photorealistic": "사진처럼 사실적인 스타일, 정확한 디테일, 자연스러운 조명, 현실적인 텍스처",
            "pixel_art": "픽셀 아트 스타일, 레트로 게임 그래픽, 제한된 색상 팔레트, 픽셀화된 이미지",
            "watercolor": "수채화 스타일, 부드러운 색상 혼합, 투명한 질감, 물감 효과"
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
        
        # 음악 동기화 템플릿
        self.music_sync_templates = {
            "beat": "음악의 비트에 맞춘 영상 전환과 움직임",
            "rhythm": "리듬에 맞춘 시각적 요소의 변화와 움직임",
            "melody": "멜로디 라인을 따라가는 부드러운 시각적 흐름",
            "drop": "음악의 드롭(고조) 부분에서 극적인 시각적 변화",
            "tempo": "음악의 템포에 맞춘 영상의 속도와 페이스",
            "mood": "음악의 분위기와 조화를 이루는 시각적 톤과 색감",
            "lyrics": "가사의 내용과 연결되는 시각적 내러티브",
            "instrument": "특정 악기 소리에 반응하는 시각적 요소"
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        Pika 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        return {
            "components": [
                "visual_concept",
                "style_reference",
                "camera_movements",
                "music_sync",
                "visual_effects",
                "scene_transitions",
                "technical_specifications"
            ],
            "recommended_order": [
                "visual_concept",
                "style_reference",
                "camera_movements",
                "music_sync",
                "visual_effects",
                "scene_transitions",
                "technical_specifications"
            ],
            "optional_components": [
                "style_reference",
                "music_sync",
                "visual_effects",
                "scene_transitions",
                "technical_specifications"
            ]
        }
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 Pika에 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        # 1. 시각적 컨셉 생성
        concept = self._generate_concept(analysis_result, intent_result)
        
        # 2. 스타일 참조 생성
        style = self._generate_style(analysis_result, intent_result)
        
        # 3. 카메라 움직임 생성
        camera = self._generate_camera_movements(analysis_result, intent_result)
        
        # 4. 음악 동기화 생성
        music_sync = self._generate_music_sync(analysis_result, intent_result)
        
        # 5. 시각적 효과 생성
        effects = self._generate_visual_effects(analysis_result, intent_result)
        
        # 6. 장면 전환 생성
        transitions = self._generate_transitions(analysis_result, intent_result)
        
        # 7. 기술적 명세 생성
        technical = self._generate_technical(analysis_result, intent_result)
        
        # 8. 최종 프롬프트 조합
        # Pika는 간결하고 명확한 프롬프트를 선호함
        prompt_parts = []
        
        # 시각적 컨셉 (필수)
        if concept:
            prompt_parts.append(concept)
        
        # 스타일 참조
        if style:
            prompt_parts.append(style)
        
        # 카메라 움직임
        if camera:
            prompt_parts.append(camera)
        
        # 음악 동기화
        if music_sync:
            prompt_parts.append(music_sync)
        
        # 시각적 효과
        if effects:
            prompt_parts.append(effects)
        
        # 장면 전환
        if transitions:
            prompt_parts.append(transitions)
        
        # 기술적 명세
        if technical:
            prompt_parts.append(technical)
        
        # 최종 프롬프트 생성
        optimized_prompt = ", ".join(filter(None, prompt_parts))
        
        # 공통 규칙 적용
        optimized_prompt = self.apply_common_rules(optimized_prompt)
        
        return optimized_prompt
    
    def _generate_concept(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """시각적 컨셉을 생성합니다."""
        # 기본 컨셉 설명
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
            "music_video": ["뮤직비디오", "음악", "노래", "댄스", "춤", "공연", "콘서트"],
            "abstract": ["추상", "비현실적", "예술적", "실험적", "개념적"],
            "product": ["제품", "상품", "광고", "홍보", "마케팅", "브랜드"],
            "animation": ["애니메이션", "만화", "캐릭터", "3D", "2D", "애니"]
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
        
        # 기본값은 character
        return "character"
    
    def _extract_scene_details(self, text: str, scene_type: str) -> Dict[str, str]:
        """입력 텍스트에서 장면 세부 정보를 추출합니다."""
        # 기본 세부 정보
        details = {}
        
        # 장면 유형별 추가 세부 정보
        if scene_type == "music_video":
            # 음악 스타일 추출
            music_style_patterns = ["팝", "록", "힙합", "재즈", "클래식", "EDM", "트로트", "발라드", "R&B"]
            for pattern in music_style_patterns:
                if pattern in text:
                    details["music_style"] = pattern
                    break
            
            # 테마 추출
            theme_patterns = ["사랑", "이별", "여행", "파티", "자연", "도시", "우정", "성장", "모험"]
            for pattern in theme_patterns:
                if pattern in text:
                    details["theme"] = pattern
                    break
            
            # 시각적 요소 추출
            visual_patterns = ["네온", "빛", "그림자", "물", "불", "구름", "별", "춤", "움직임"]
            for pattern in visual_patterns:
                if pattern in text:
                    details["visual_elements"] = pattern
                    break
            
            # 카메라 움직임 추출
            camera_patterns = ["패닝", "틸트", "줌", "트래킹", "고정", "항공", "드론"]
            for pattern in camera_patterns:
                if pattern in text:
                    details["camera_movement"] = pattern
                    break
            
            # 스타일 추출
            style_patterns = ["영화적", "애니메이션", "빈티지", "미래적", "몽환적", "사실적"]
            for pattern in style_patterns:
                if pattern in text:
                    details["style"] = pattern
                    break
        
        elif scene_type == "animation":
            # 애니메이션 스타일 추출
            animation_style_patterns = ["2D", "3D", "픽셀", "스톱모션", "수채화", "일본식", "디즈니", "미니멀"]
            for pattern in animation_style_patterns:
                if pattern in text:
                    details["animation_style"] = pattern
                    break
            
            # 캐릭터 추출
            character_patterns = ["사람", "동물", "로봇", "판타지", "몬스터", "영웅", "요정", "외계인"]
            for pattern in character_patterns:
                if pattern in text:
                    details["character"] = pattern
                    break
            
            # 행동 추출
            action_patterns = ["달리는", "뛰는", "날아가는", "싸우는", "춤추는", "여행하는", "모험하는"]
            for pattern in action_patterns:
                if pattern in text:
                    details["action"] = pattern
                    break
            
            # 배경 추출
            setting_patterns = ["우주", "판타지", "도시", "자연", "바다", "산", "미래", "과거"]
            for pattern in setting_patterns:
                if pattern in text:
                    details["setting"] = pattern
                    break
            
            # 스타일 추출
            style_patterns = ["밝은", "어두운", "화려한", "단순한", "복잡한", "귀여운", "심각한"]
            for pattern in style_patterns:
                if pattern in text:
                    details["style"] = pattern
                    break
        
        # 다른 장면 유형에 대한 세부 정보 추출 로직 추가 가능
        
        # 기본 설명 추가
        details["description"] = text
        
        return details
    
    def _generate_style(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """스타일 참조를 생성합니다."""
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
            # 장면 유형에 따른 기본 스타일 선택
            scene_type = self._detect_scene_type(analysis_result.get("input_text", ""))
            
            if scene_type == "nature":
                style_text = self.style_templates["cinematic"]
            elif scene_type == "urban":
                style_text = self.style_templates["cinematic"]
            elif scene_type == "character":
                style_text = self.style_templates["cinematic"]
            elif scene_type == "music_video":
                style_text = self.style_templates["stylized"]
            elif scene_type == "abstract":
                style_text = self.style_templates["dreamy"]
            elif scene_type == "animation":
                style_text = self.style_templates["3d_animation"]
            else:
                style_text = self.style_templates["cinematic"]
        
        # 참조 이미지 정보 추출
        reference_images = analysis_result.get("reference_images", [])
        if reference_images:
            style_text += ", 참조 이미지 스타일"
        
        return style_text
    
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
        
        # 장면 유형에 따른 기본 카메라 움직임 선택
        scene_type = self._detect_scene_type(analysis_result.get("input_text", ""))
        
        if scene_type == "nature":
            return "부드러운 패닝 샷, 자연 풍경을 넓게 보여주는 움직임"
        elif scene_type == "urban":
            return "역동적인 트래킹 샷, 도시의 활기를 따라가는 움직임"
        elif scene_type == "character":
            return "캐릭터를 따라가는 부드러운 트래킹 샷"
        elif scene_type == "music_video":
            return "음악의 리듬에 맞춘 역동적인 카메라 움직임, 비트에 맞는 전환"
        elif scene_type == "animation":
            return "부드럽고 유동적인 카메라 움직임, 캐릭터의 동작을 강조하는 앵글"
        
        # 기본 카메라 움직임
        return "영상의 내용과 분위기에 맞는 자연스러운 카메라 움직임"
    
    def _generate_music_sync(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """음악 동기화를 생성합니다."""
        # 음악 동기화 정보 추출
        music_sync = analysis_result.get("music_sync", [])
        
        # 음악 동기화가 명시적으로 지정된 경우
        if music_sync:
            sync_texts = []
            for sync in music_sync:
                if sync in self.music_sync_templates:
                    sync_texts.append(self.music_sync_templates[sync])
                else:
                    sync_texts.append(sync)
            
            return ", ".join(sync_texts)
        
        # 장면 유형에 따른 기본 음악 동기화 선택
        scene_type = self._detect_scene_type(analysis_result.get("input_text", ""))
        
        if scene_type == "nature":
            return "자연스러운 음악 동기화, 자연 풍경을 더욱 아름답게 표현"
        elif scene_type == "urban":
            return "도시의 활기와 밝은 분위기에 맞춘 음악 동기화"
        elif scene_type == "character":
            return "캐릭터의 감정과 행동에 맞춘 음악 동기화"
        elif scene_type == "music_video":
            return "뮤직비디오의 내용과 분위기에 맞춘 음악 동기화"
        elif scene_type == "animation":
            return "애니메이션의 분위기와 캐릭터의 동작에 맞춘 음악 동기화"