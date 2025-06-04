"""
이미지 생성 모델을 위한 프롬프트 템플릿 모듈
"""

from typing import Dict, List, Any

class ImagePromptTemplate:
    """이미지 생성 모델을 위한 프롬프트 템플릿 클래스"""
    
    @staticmethod
    def get_basic_template() -> Dict[str, Any]:
        """기본 이미지 프롬프트 템플릿 반환"""
        return {
            "components": [
                "subject_description",
                "style_description",
                "composition",
                "lighting",
                "color_palette",
                "technical_parameters",
                "negative_prompts"
            ],
            "recommended_order": [
                "subject_description",
                "style_description",
                "composition",
                "lighting",
                "color_palette",
                "technical_parameters",
                "negative_prompts"
            ],
            "optional_components": [
                "lighting",
                "color_palette",
                "technical_parameters",
                "negative_prompts"
            ]
        }
    
    @staticmethod
    def get_subject_templates() -> Dict[str, str]:
        """피사체 설명 템플릿 반환"""
        return {
            "person": "중년의 남성, 턱수염, 캐주얼한 의상, 사려 깊은 표정",
            "landscape": "광활한 산맥, 석양에 비치는 눈 덮인 봉우리, 아래 계곡의 안개",
            "object": "오래된 빈티지 카메라, 가죽 표면, 반사되는 금속 렌즈",
            "animal": "아름다운 붉은색 여우, 숲속에 앉아 있는 모습, 호기심 어린 눈빛",
            "abstract": "꿈같은 파도와 기하학적 형태가 서로 어우러지는 추상적 형태",
            "architecture": "미래적인 고층 건물, 유리와 강철 구조, 하늘에 반사되는 표면",
            "food": "완벽하게 차려진 프랑스 요리, 선명한 색상의 음식, 증기가 살짝 올라옴"
        }
    
    @staticmethod
    def get_style_templates() -> Dict[str, str]:
        """스타일 설명 템플릿 반환"""
        return {
            "photorealistic": "초고해상도 사진, 사실적인 디테일, DSLR로 촬영한 듯한 품질",
            "oil_painting": "유화 스타일, 두꺼운 물감 질감, 뚜렷한 붓놀림",
            "watercolor": "수채화, 부드러운 색상 혼합, 투명한 물감의 느낌",
            "3d_render": "3D 렌더링, 높은 디테일, 완벽한 그림자와 반사",
            "concept_art": "영화 컨셉 아트, 인상적인 구도, 역동적인 요소",
            "anime": "일본 애니메이션 스타일, 선명한 윤곽선, 특징적인 캐릭터 디자인",
            "digital_art": "디지털 아트, 선명한 색상, 세밀한 디테일, 완벽한 그라데이션",
            "sketch": "손으로 그린 스케치, 연필 질감, 자연스러운 선의 흐름",
            "pixel_art": "픽셀 아트, 복고풍 게임 스타일, 제한된 색상 팔레트"
        }
    
    @staticmethod
    def get_composition_templates() -> Dict[str, str]:
        """구도 템플릿 반환"""
        return {
            "wide_shot": "와이드 샷, 전체 장면 포착, 환경을 강조",
            "close_up": "클로즈업, 세부 디테일에 초점, 인물의 표정 강조",
            "aerial_view": "공중 전망, 높은 각도에서 내려다보는 시점",
            "low_angle": "로우 앵글, 아래에서 위로 올려다보는 시점, 웅장함 강조",
            "dutch_angle": "더치 앵글(기울어진 화면), 긴장감과 불안정함 표현",
            "symmetrical": "대칭 구도, 중앙을 기준으로 완벽한 좌우 대칭",
            "rule_of_thirds": "삼분할 구도, 주요 피사체가 화면의 교차점에 위치",
            "golden_ratio": "황금비율 구도, 자연스럽고 조화로운 비율"
        }
    
    @staticmethod
    def get_lighting_templates() -> Dict[str, str]:
        """조명 템플릿 반환"""
        return {
            "natural_daylight": "자연광, 밝고 균일한 조명, 부드러운 그림자",
            "golden_hour": "황금빛 조명, 일출이나 일몰의 따뜻한 빛",
            "dramatic": "극적인 조명, 강한 대비, 하이라이트와 그림자가 뚜렷함",
            "soft": "부드러운 조명, 균일하고 확산된 빛, 부드러운 그림자",
            "backlit": "역광, 피사체의 뒤에서 비치는 빛, 실루엣 효과",
            "studio": "스튜디오 조명, 정교하게 설정된 인공 조명, 완벽한 노출",
            "neon": "네온 조명, 선명한 색상의 인공 빛, 사이버펑크 분위기",
            "candlelight": "촛불 조명, 따뜻하고 흔들리는 빛, 아늑한 분위기"
        }
    
    @staticmethod
    def get_color_palette_templates() -> Dict[str, str]:
        """색상 팔레트 템플릿 반환"""
        return {
            "vibrant": "선명하고 강렬한 색상, 높은 채도, 뚜렷한 대비",
            "pastel": "파스텔 색상, 부드럽고 연한 색조, 밝은 톤",
            "monochromatic": "단색 팔레트, 한 가지 색상의 다양한 음영과 채도",
            "analogous": "유사 색상 팔레트, 색상환에서 서로 인접한 색상들",
            "complementary": "보색 팔레트, 색상환에서 서로 마주보는 색상들의 조합",
            "warm": "따뜻한 색상 팔레트, 빨강, 주황, 노랑 계열 중심",
            "cool": "차가운 색상 팔레트, 파랑, 보라, 초록 계열 중심",
            "vintage": "빈티지 색상, 약간 바랜 듯한 복고풍 색상"
        }
    
    @staticmethod
    def get_technical_parameter_templates() -> Dict[str, str]:
        """기술적 매개변수 템플릿 반환"""
        return {
            "ultra_detailed": "초고해상도, 8K, 세밀한 디테일, 선명한 질감",
            "depth_of_field": "얕은 피사계 심도, 배경 흐림 효과, 피사체 강조",
            "motion_blur": "모션 블러, 움직임이 있는 요소에 속도감 표현",
            "film_grain": "필름 그레인, 아날로그 카메라 느낌의 입자 효과",
            "sharp_focus": "선명한 초점, 디테일이 살아있는 또렷한 이미지",
            "high_contrast": "높은 대비, 명암 차이가 뚜렷한 이미지",
            "hdr": "HDR(High Dynamic Range), 폭넓은 색상과 밝기 범위"
        }
    
    @staticmethod
    def get_negative_prompt_templates() -> List[str]:
        """네거티브 프롬프트 템플릿 반환"""
        return [
            "저해상도, 흐릿함, 왜곡된 비율, 이상한 얼굴 특징",
            "잘린 이미지, 부자연스러운 포즈, 기형적인 손가락, 과도한 노이즈",
            "부자연스러운 색상, 낮은 품질, 텍스트나 워터마크",
            "지나치게 포화된 색상, 그래픽 오류, 부자연스러운 질감"
        ]
    
    @staticmethod
    def get_full_prompt_template(
        subject: str,
        style: str = None,
        composition: str = None,
        lighting: str = None,
        color_palette: str = None,
        technical_parameters: str = None,
        negative_prompts: List[str] = None
    ) -> Dict[str, str]:
        """완전한 이미지 프롬프트 템플릿 생성"""
        prompt_parts = [subject]
        
        if style:
            prompt_parts.append(style)
        
        if composition:
            prompt_parts.append(composition)
        
        if lighting:
            prompt_parts.append(lighting)
        
        if color_palette:
            prompt_parts.append(color_palette)
        
        if technical_parameters:
            prompt_parts.append(technical_parameters)
        
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