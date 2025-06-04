"""
음악 생성 모델을 위한 프롬프트 템플릿 모듈
"""

from typing import Dict, List, Any

class MusicPromptTemplate:
    """음악 생성 모델을 위한 프롬프트 템플릿 클래스"""
    
    @staticmethod
    def get_basic_template() -> Dict[str, Any]:
        """기본 음악 프롬프트 템플릿 반환"""
        return {
            "components": [
                "genre_style",
                "mood_emotion",
                "instruments",
                "tempo_rhythm",
                "structure",
                "lyrics_theme",
                "reference_tracks",
                "duration_quality"
            ],
            "recommended_order": [
                "genre_style",
                "mood_emotion",
                "instruments",
                "tempo_rhythm",
                "structure",
                "lyrics_theme",
                "reference_tracks",
                "duration_quality"
            ],
            "optional_components": [
                "lyrics_theme",
                "structure",
                "reference_tracks",
                "duration_quality"
            ]
        }
    
    @staticmethod
    def get_genre_style_templates() -> Dict[str, str]:
        """장르와 스타일 템플릿 반환"""
        return {
            "pop": "현대적인 팝 음악, 캐치한 후렴구, 깔끔한 프로덕션, 대중적인 구조",
            "rock": "강렬한 록 사운드, 일렉트릭 기타 리프, 파워풀한 드럼, 에너지 넘치는 보컬",
            "electronic": "전자 음악, 신디사이저 기반, 미니멀한 비트, 미래적인 사운드스케이프",
            "classical": "클래식 음악, 오케스트라 구성, 복잡한 화성 구조, 감정적인 표현",
            "jazz": "재즈, 즉흥 연주, 복잡한 화성 진행, 스윙 리듬, 자유로운 표현",
            "hiphop": "힙합, 강한 비트, 베이스 중심, 리드미컬한 보컬 플로우",
            "ambient": "앰비언트 음악, 부드러운 음향, 느린 진행, 명상적인 분위기, 배경음 특성",
            "folk": "포크 음악, 어쿠스틱 기반, 스토리텔링 중심, 전통적 요소, 자연스러운 사운드",
            "world": "월드 뮤직, 다양한 문화적 요소, 독특한 민족 악기, 전통적 리듬 패턴"
        }
    
    @staticmethod
    def get_mood_emotion_templates() -> Dict[str, str]:
        """분위기와 감정 템플릿 반환"""
        return {
            "happy": "밝고 경쾌한 분위기, 희망적인 느낌, 활기찬 에너지, 긍정적인 감정",
            "sad": "슬프고 멜랑콜리한 분위기, 감성적인 표현, 내면적인 성찰, 서정적 선율",
            "energetic": "역동적이고 에너지 넘치는 분위기, 흥분감, 움직임을 유발하는 리듬",
            "relaxing": "편안하고 차분한 분위기, 스트레스 해소, 평화로운 흐름, 부드러운 전개",
            "dramatic": "극적인 분위기, 감정의 굴곡, 긴장과 해소, 영화 음악적 접근",
            "mysterious": "신비로운 분위기, 호기심을 자극하는 사운드, 예측할 수 없는 진행",
            "romantic": "로맨틱한 분위기, 감미로운 선율, 따뜻한 화성, 감성적인 표현",
            "epic": "웅장하고 서사적인 분위기, 큰 스케일, 감동적인 클라이맥스, 영웅적 느낌",
            "nostalgic": "향수를 불러일으키는 분위기, 과거를 회상하는 느낌, 따뜻한 감성"
        }
    
    @staticmethod
    def get_instrument_templates() -> Dict[str, str]:
        """악기 구성 템플릿 반환"""
        return {
            "orchestral": "풀 오케스트라, 현악기, 관악기, 타악기가 조화롭게 어우러진 웅장한 앙상블",
            "band": "전형적인 밴드 구성, 드럼, 베이스, 일렉트릭 기타, 키보드, 보컬 중심",
            "electronic": "전자 악기, 신디사이저, 드럼 머신, 샘플러, 디지털 효과",
            "acoustic": "어쿠스틱 기타, 피아노, 어쿠스틱 베이스, 가벼운 타악기 중심",
            "strings": "현악기 중심, 바이올린, 비올라, 첼로, 더블 베이스의 풍부한 앙상블",
            "brass": "금관악기 중심, 트럼펫, 트롬본, 호른, 튜바의 화려하고 강렬한 사운드",
            "piano_solo": "솔로 피아노, 섬세한 터치와 표현, 다이내믹한 범위, 독주 악기로서의 완성도",
            "vocal_centric": "보컬 중심, 목소리가 주요 표현 수단, 백킹 악기는 보조적 역할",
            "percussion": "타악기 중심, 다양한 리듬 악기, 풍부한 타악 앙상블, 리듬적 다양성"
        }
    
    @staticmethod
    def get_tempo_rhythm_templates() -> Dict[str, str]:
        """템포와 리듬 템플릿 반환"""
        return {
            "slow": "느린 템포(60-80 BPM), 여유로운 진행, 긴 음표 중심, 편안한 흐름",
            "moderate": "중간 템포(80-110 BPM), 안정적인 리듬, 균형잡힌 흐름, 자연스러운 진행",
            "fast": "빠른 템포(120-160 BPM), 활기찬 리듬, 짧은 음표, 역동적인 진행",
            "very_fast": "매우 빠른 템포(160+ BPM), 격렬한 리듬, 높은 에너지, 강렬한 진행",
            "waltz": "3/4 박자, 왈츠 리듬, 우아한 흐름, 춤을 연상시키는 움직임",
            "syncopated": "당김음이 많은 리듬, 예상치 못한 악센트, 리듬적 긴장감",
            "complex": "복잡한 리듬 패턴, 불규칙한 박자, 변화무쌍한 리듬 구조",
            "steady": "안정적이고 꾸준한 리듬, 일정한 비트, 규칙적인 패턴"
        }
    
    @staticmethod
    def get_structure_templates() -> Dict[str, str]:
        """곡 구조 템플릿 반환"""
        return {
            "verse_chorus": "전통적인 verse-chorus 구조, 반복되는 후렴구, 발전하는 구성",
            "intro_verse_chorus_bridge_outro": "완전한 팝 구조, 도입부, 절, 후렴, 브릿지, 마무리 포함",
            "aaba": "AABA 형식, 재즈와 대중음악에서 흔한 32마디 구조",
            "through_composed": "스루컴포즈드 구조, 반복 없이 계속 발전하는 구성",
            "theme_variations": "주제와 변주 형식, 기본 테마를 다양하게 변형하며 발전",
            "ambient_flow": "뚜렷한 구조 없이 자연스럽게 흐르는 앰비언트 스타일",
            "sonata_form": "소나타 형식, 제시부-발전부-재현부의 클래식 구조",
            "intro_drop_breakdown_drop_outro": "EDM 구조, 인트로, 드롭, 브레이크다운, 두 번째 드롭, 아웃트로"
        }
    
    @staticmethod
    def get_lyrics_theme_templates() -> Dict[str, str]:
        """가사 주제 템플릿 반환"""
        return {
            "love": "사랑을 주제로 한 가사, 로맨틱한 감정, 관계에 대한 이야기",
            "nature": "자연을 주제로 한 가사, 풍경, 계절, 자연 현상에 대한 묘사",
            "personal_growth": "개인적 성장과 자아 발견, 인생의 여정, 극복에 대한 이야기",
            "social_issues": "사회적 이슈, 현실 문제, 사회 비판, 변화에 대한 메시지",
            "storytelling": "이야기를 들려주는 가사, 캐릭터와 내러티브 중심",
            "fantasy": "판타지 세계, 상상력, 초현실적 이미지, 꿈같은 세계관",
            "spiritual": "영적인 주제, 깨달음, 초월적 경험, 내면의 평화",
            "instrumental": "가사 없음, 순수한 음악적 표현에 집중"
        }
    
    @staticmethod
    def get_reference_track_templates() -> Dict[str, str]:
        """참조 트랙 템플릿 반환"""
        return {
            "pop": "\"Shape of You\" - Ed Sheeran과 같은 캐치한 현대 팝 스타일",
            "rock": "\"Stairway to Heaven\" - Led Zeppelin의 상징적인 록 트랙 느낌",
            "electronic": "\"Strobe\" - Deadmau5와 같은 분위기의 일렉트로닉 트랙",
            "classical": "베토벤의 \"월광 소나타\"와 같은 클래식 피아노 곡 스타일",
            "jazz": "\"Take Five\" - Dave Brubeck의 재즈 스탠다드 접근 방식",
            "ambient": "Brian Eno의 \"Music for Airports\"와 같은 앰비언트 분위기",
            "folk": "Bob Dylan의 \"Blowin' in the Wind\"와 같은 포크 스타일",
            "hip_hop": "Kendrick Lamar의 \"HUMBLE.\"과 같은 현대 힙합 비트"
        }
    
    @staticmethod
    def get_duration_quality_templates() -> Dict[str, str]:
        """길이와 품질 템플릿 반환"""
        return {
            "short": "짧은 길이(1-2분), 간결한 구성, 핵심 아이디어에 집중",
            "standard": "표준 길이(3-4분), 균형 잡힌 구성, 라디오 친화적 형식",
            "extended": "긴 길이(5-7분), 발전된 구조, 깊이 있는 음악적 탐구",
            "ambient_long": "매우 긴 길이(10분 이상), 점진적인 변화, 몰입감 있는 경험",
            "high_fidelity": "높은 음질, 명확한 믹싱, 전문적인 마스터링, 세밀한 디테일",
            "lo_fi": "로파이 사운드, 의도적인 노이즈, 빈티지한 느낌, 따뜻한 아날로그 감성"
        }
    
    @staticmethod
    def get_full_prompt_template(
        genre_style: str,
        mood_emotion: str = None,
        instruments: str = None,
        tempo_rhythm: str = None,
        structure: str = None,
        lyrics_theme: str = None,
        reference_tracks: str = None,
        duration_quality: str = None
    ) -> str:
        """완전한 음악 프롬프트 템플릿 생성"""
        prompt_parts = [f"장르/스타일: {genre_style}"]
        
        if mood_emotion:
            prompt_parts.append(f"분위기/감정: {mood_emotion}")
        
        if instruments:
            prompt_parts.append(f"악기 구성: {instruments}")
        
        if tempo_rhythm:
            prompt_parts.append(f"템포/리듬: {tempo_rhythm}")
        
        if structure:
            prompt_parts.append(f"곡 구조: {structure}")
        
        if lyrics_theme:
            prompt_parts.append(f"가사 주제: {lyrics_theme}")
        
        if reference_tracks:
            prompt_parts.append(f"참조 트랙: {reference_tracks}")
        
        if duration_quality:
            prompt_parts.append(f"길이/품질: {duration_quality}")
        
        # 최종 프롬프트 생성
        full_prompt = "\n".join(prompt_parts)
        
        return full_prompt 