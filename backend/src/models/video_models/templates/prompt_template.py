"""
비디오 생성 모델을 위한 프롬프트 템플릿 모듈
"""

from typing import Dict, List, Any

class VideoPromptTemplate:
    """비디오 생성 모델을 위한 프롬프트 템플릿 클래스"""
    
    @staticmethod
    def get_basic_template() -> Dict[str, Any]:
        """기본 비디오 프롬프트 템플릿 반환"""
        return {
            "components": [
                "scene_description",
                "motion_description",
                "style_description",
                "camera_movement",
                "lighting_atmosphere",
                "audio_description",
                "duration_fps",
                "negative_prompts"
            ],
            "recommended_order": [
                "scene_description",
                "motion_description",
                "style_description", 
                "camera_movement",
                "lighting_atmosphere",
                "audio_description",
                "duration_fps",
                "negative_prompts"
            ],
            "optional_components": [
                "camera_movement",
                "lighting_atmosphere",
                "audio_description",
                "duration_fps",
                "negative_prompts"
            ]
        }
    
    @staticmethod
    def get_scene_templates() -> Dict[str, str]:
        """장면 설명 템플릿 반환"""
        return {
            "nature": "울창한 숲속 호수, 물에 비치는 나무들, 잔잔한 물결, 새들이 나뭇가지 사이를 날아다님",
            "urban": "북적이는 도시의 교차로, 사람들이 이동하는 모습, 불빛이 가득한 고층 빌딩들, 택시와 버스 지나가는 모습",
            "futuristic": "미래 도시의 공중 도로, 날아다니는 차량들, 홀로그램 광고판, 네온 불빛의 거리",
            "fantasy": "마법의 성, 하늘을 나는 용, 빛나는 마법 입자들, 신비로운 안개가 둘러싸인 풍경",
            "space": "우주 공간의 행성들, 반짝이는 별, 떠다니는 소행성들, 멀리서 빛나는 은하",
            "underwater": "화려한 산호초와 열대어들, 물속 빛줄기, 부드럽게 흔들리는 해초, 거품들이 올라오는 모습",
            "historical": "중세 시대 마을 거리, 석조 건물들, 횃불을 든 사람들, 말이 끄는 마차"
        }
    
    @staticmethod
    def get_motion_templates() -> Dict[str, str]:
        """모션 설명 템플릿 반환"""
        return {
            "slow": "느리고 우아한 움직임, 시간이 늘어나는 듯한 느낌, 부드러운 변화",
            "fast": "빠른 속도감, 역동적인 움직임, 급격한 변화, 에너지 넘치는 동작",
            "flowing": "물 흐르듯 자연스러운 움직임, 연속적이고 부드러운 흐름",
            "robotic": "기계적이고 정확한 움직임, 예측 가능한 패턴, 일정한 속도",
            "chaotic": "예측할 수 없는 혼돈스러운 움직임, 불규칙한 변화, 다양한 속도",
            "rhythmic": "음악에 맞춘 듯한 리듬감 있는 움직임, 일정한 패턴의 반복",
            "subtle": "미묘하고 섬세한 움직임, 눈치채기 어려운 작은 변화, 정적인 느낌 속 섬세한 동작"
        }
    
    @staticmethod
    def get_style_templates() -> Dict[str, str]:
        """스타일 설명 템플릿 반환"""
        return {
            "cinematic": "영화적 품질, 전문 영화 촬영 기법, 넓은 화면비, 시네마틱 컬러 그레이딩",
            "documentary": "다큐멘터리 스타일, 사실적 표현, 인터뷰 형식, 현장감 있는 촬영",
            "animation": "3D 애니메이션, 생생한 캐릭터와 환경, 부드러운 동작, 스튜디오 퀄리티",
            "stop_motion": "스톱모션 애니메이션 효과, 약간의 떨림, 독특한 질감과 움직임",
            "vhs": "VHS 테이프 느낌, 노이즈와 지터, 낮은 해상도, 복고풍 색상",
            "noir": "필름 누아르 스타일, 강한 대비, 그림자와 실루엣, 흑백 또는 탈색된 색상",
            "dreamy": "꿈같은 분위기, 부드러운 초점, 빛 번짐 효과, 밝은 하이라이트"
        }
    
    @staticmethod
    def get_camera_movement_templates() -> Dict[str, str]:
        """카메라 움직임 템플릿 반환"""
        return {
            "stationary": "고정된 카메라, 움직임 없음, 안정적인 프레임",
            "panning": "수평 패닝, 왼쪽에서 오른쪽(또는 반대)으로 카메라가 회전",
            "tilting": "수직 틸팅, 위에서 아래(또는 반대)로 카메라가 회전",
            "tracking": "트래킹 샷, 피사체를 따라 부드럽게 이동하는 카메라",
            "aerial": "드론 촬영 같은 공중 시점, 높은 곳에서 내려다보는 앵글",
            "dolly": "달리 샷, 카메라가 피사체를 향해 앞으로 또는 뒤로 이동",
            "zoom": "줌 인/줌 아웃, 피사체를 향해 확대하거나 축소하는 효과",
            "handheld": "핸드헬드 효과, 약간의 흔들림, 다큐멘터리 같은 현실감"
        }
    
    @staticmethod
    def get_lighting_atmosphere_templates() -> Dict[str, str]:
        """조명과 분위기 템플릿 반환"""
        return {
            "bright": "밝고 활기찬 조명, 선명한 색상, 긍정적인 분위기",
            "dark": "어둡고 그림자가 많은 조명, 미스터리한 분위기, 낮은 노출",
            "dramatic": "극적인 조명, 강한 대비, 감정적인 분위기",
            "foggy": "안개 낀 분위기, 부드러운 빛 산란, 신비로운 환경",
            "sunset": "석양의 따뜻한 황금빛 조명, 긴 그림자, 로맨틱한 분위기",
            "rainy": "비 내리는 분위기, 젖은 표면의 반사, 물방울 효과, 차분한 느낌",
            "neon": "네온 조명 효과, 선명한 인공 빛, 도시적 분위기, 현대적 느낌"
        }
    
    @staticmethod
    def get_audio_description_templates() -> Dict[str, str]:
        """오디오 설명 템플릿 반환"""
        return {
            "ambient": "자연스러운 환경음, 배경의 작은 소리들, 현장감 있는 사운드스케이프",
            "soundtrack": "영화 같은 배경 음악, 분위기에 맞는 오케스트라 또는 전자음악",
            "dialogue": "등장인물 간의 대화, 또렷한 음성, 감정을 담은 대사",
            "sfx": "특수 효과음, 액션에 맞는 사운드 이펙트, 현실감 있는 소리",
            "voice_over": "나레이션, 배경에 깔리는 설명하는 목소리, 이야기를 이끄는 해설",
            "silence": "의도적인 침묵, 최소한의 소리, 시각적 요소에 집중",
            "rhythmic": "리듬감 있는 음악, 영상의 템포에 맞춘 비트, 역동적인 사운드트랙"
        }
    
    @staticmethod
    def get_duration_fps_templates() -> Dict[str, str]:
        """영상 길이와 FPS 템플릿 반환"""
        return {
            "short": "짧은 클립, 5-10초, 30fps, 간결한 내용",
            "medium": "중간 길이, 15-30초, 30fps, 발전된 내용",
            "cinematic": "영화적 느낌, 24fps, 부드러운 모션 블러",
            "slow_motion": "슬로우 모션 효과, 60fps 촬영 30fps 재생, 부드러운 디테일",
            "timelapse": "타임랩스, 길어 보이는 시간을 압축, 빠른 구름이나 인파의 움직임",
            "smooth": "매우 부드러운 움직임, 60fps, 고품질 모션"
        }
    
    @staticmethod
    def get_negative_prompt_templates() -> List[str]:
        """네거티브 프롬프트 템플릿 반환"""
        return [
            "흐릿함, 저해상도, 왜곡, 깜빡임, 불안정한 영상",
            "잘린 프레임, 부자연스러운 움직임, 불연속적인 전환",
            "텍스트, 워터마크, 로고, UI 요소",
            "과도한 노이즈, 색상 오류, 압축 아티팩트"
        ]
    
    @staticmethod
    def get_full_prompt_template(
        scene: str,
        motion: str = None,
        style: str = None,
        camera_movement: str = None,
        lighting_atmosphere: str = None,
        audio_description: str = None,
        duration_fps: str = None,
        negative_prompts: List[str] = None
    ) -> Dict[str, str]:
        """완전한 비디오 프롬프트 템플릿 생성"""
        prompt_parts = [scene]
        
        if motion:
            prompt_parts.append(motion)
        
        if style:
            prompt_parts.append(style)
        
        if camera_movement:
            prompt_parts.append(f"카메라: {camera_movement}")
        
        if lighting_atmosphere:
            prompt_parts.append(f"조명: {lighting_atmosphere}")
        
        if audio_description:
            prompt_parts.append(f"오디오: {audio_description}")
        
        if duration_fps:
            prompt_parts.append(f"기술 설정: {duration_fps}")
        
        # 최종 프롬프트 생성
        positive_prompt = ", ".join(prompt_parts)
        
        # 네거티브 프롬프트 처리
        negative_prompt = ""
        if negative_prompts and isinstance(negative_prompts, list):
            negative_prompt = ", ".join(negative_prompts)
        
        return {
            "prompt": positive_prompt,
            "negative_prompt": negative_prompt
        } 