"""
Suno 모델 최적화 모듈: Suno 모델에 최적화된 프롬프트를 생성합니다.
"""

from typing import Dict, Any, List
import re
from ..base_model import BaseModel

class SunoModel(BaseModel):
    """
    Suno 모델에 최적화된 프롬프트를 생성하는 클래스
    """
    
    def __init__(self):
        """Suno 모델 클래스 초기화"""
        super().__init__(
            model_id="suno",
            model_name="Suno",
            provider="Suno"
        )
        self.capabilities = [
            "music_generation",
            "lyrics_generation",
            "genre_style_control",
            "mood_control",
            "instrumentation_control",
            "structure_control",
            "vocal_style_control"
        ]
        self.max_tokens = 600  # 프롬프트 최대 길이
        self.supports_multimodal = False
        self.best_practices = [
            "음악 장르와 스타일 명확히 지정",
            "가사 주제와 내용 구체적 설명",
            "원하는 악기 구성 명시",
            "분위기와 감정 표현 포함",
            "곡의 구조와 전개 설명",
            "보컬 스타일과 특성 지정",
            "참조 아티스트나 곡 언급"
        ]
        
        # Suno에 최적화된 음악 템플릿
        self.music_templates = {
            "pop": "{mood} 분위기의 팝 음악, {vocal_style} 보컬 스타일, {theme}에 관한 가사, {instruments} 악기 구성",
            "rock": "{mood} 분위기의 록 음악, {vocal_style} 보컬 스타일, {theme}에 관한 가사, {instruments} 악기 구성",
            "hiphop": "{mood} 분위기의 힙합 음악, {vocal_style} 보컬 스타일, {theme}에 관한 가사, {instruments} 악기 구성",
            "electronic": "{mood} 분위기의 일렉트로닉 음악, {vocal_style} 보컬 스타일, {theme}에 관한 가사, {instruments} 악기 구성",
            "jazz": "{mood} 분위기의 재즈 음악, {vocal_style} 보컬 스타일, {theme}에 관한 가사, {instruments} 악기 구성",
            "classical": "{mood} 분위기의 클래식 음악, {instruments} 악기 구성, {structure} 구조",
            "folk": "{mood} 분위기의 포크 음악, {vocal_style} 보컬 스타일, {theme}에 관한 가사, {instruments} 악기 구성",
            "rnb": "{mood} 분위기의 R&B 음악, {vocal_style} 보컬 스타일, {theme}에 관한 가사, {instruments} 악기 구성",
            "soundtrack": "{mood} 분위기의 사운드트랙, {theme}을 표현하는, {instruments} 악기 구성, {structure} 구조"
        }
        
        # 분위기 템플릿
        self.mood_templates = {
            "happy": "밝고 경쾌한, 긍정적인, 활기찬",
            "sad": "슬프고 우울한, 멜랑콜리한, 감성적인",
            "energetic": "에너지 넘치는, 역동적인, 활기찬",
            "calm": "차분하고 평온한, 편안한, 부드러운",
            "dramatic": "극적인, 긴장감 있는, 웅장한",
            "romantic": "로맨틱한, 감미로운, 따뜻한",
            "mysterious": "신비로운, 미스터리한, 몽환적인",
            "nostalgic": "향수를 불러일으키는, 복고적인, 추억의",
            "epic": "웅장하고 장대한, 영웅적인, 압도적인",
            "playful": "장난스러운, 유쾌한, 재미있는"
        }
        
        # 보컬 스타일 템플릿 (docs/development 문서 기반 확장)
        self.vocal_style_templates = {
            "powerful": "파워풀한 보컬, 강렬한 목소리, 넓은 음역대, 벨팅 기법",
            "soft": "부드러운 보컬, 감미로운 목소리, 속삭이는 듯한, 인티메이트한 느낌",
            "raspy": "허스키한 보컬, 거친 질감의 목소리, 감정적인 표현",
            "smooth": "매끄러운 보컬, 부드럽게 흐르는 목소리, 실키한 톤",
            "soulful": "소울풀한 보컬, 감정이 풍부한 표현, 멜리스마 기법",
            "operatic": "오페라틱한 보컬, 클래식한 발성, 정확한 딕션",
            "rap": "랩 보컬, 리듬감 있는 딜리버리, 플로우 중심, 명확한 발음",
            "breathy": "숨이 섞인 보컬, 공기가 느껴지는 목소리, 감성적인 표현",
            "autotuned": "오토튠 효과가 적용된 보컬, 전자적인 느낌, 미래적인 사운드",
            "choir": "합창단 스타일, 여러 목소리의 하모니, 풍성한 화음",
            "folk": "포크 보컬, 자연스럽고 진정성 있는 목소리, 스토리텔링 중심",
            "blues": "블루스 보컬, 감정의 깊이가 느껴지는, 애절한 표현",
            "country": "컨트리 보컬, 내러티브가 중요한, 따뜻하고 친근한 목소리",
            "metal": "메탈 보컬, 극적이고 강력한, 스크리밍과 그로울링 포함",
            "gospel": "가스펠 보컬, 영적이고 감동적인, 풍부한 감정 표현"
        }
        
        # 악기 구성 템플릿
        self.instrument_templates = {
            "band": "밴드 구성(기타, 베이스, 드럼, 키보드)",
            "orchestra": "오케스트라 구성(현악기, 관악기, 타악기)",
            "electronic": "전자 악기 구성(신디사이저, 드럼머신, 샘플러)",
            "acoustic": "어쿠스틱 악기 구성(어쿠스틱 기타, 피아노, 가벼운 타악기)",
            "hiphop": "힙합 구성(비트, 베이스, 샘플)",
            "jazz": "재즈 구성(피아노, 더블 베이스, 드럼, 색소폰)",
            "rock": "록 밴드 구성(일렉 기타, 베이스, 드럼, 보컬)",
            "pop": "팝 구성(신디사이저, 드럼, 기타, 베이스)",
            "minimal": "미니멀 구성(피아노 또는 기타 중심, 최소한의 반주)",
            "experimental": "실험적 구성(비전통적 악기, 특이한 사운드 디자인)"
        }
        
        # 곡 구조 템플릿
        self.structure_templates = {
            "verse_chorus": "일반적인 구조(인트로, 버스, 코러스, 버스, 코러스, 브릿지, 코러스, 아웃트로)",
            "ambient": "앰비언트 구조(점진적 발전, 레이어 추가, 클라이맥스 없음)",
            "buildup_drop": "빌드업과 드롭 구조(인트로, 빌드업, 드롭, 브레이크, 빌드업, 드롭, 아웃트로)",
            "aaba": "AABA 구조(A 섹션 두 번, B 섹션, A 섹션)",
            "through_composed": "스루 컴포즈드 구조(반복 없이 계속 발전)",
            "loop_based": "루프 기반 구조(반복적인 패턴, 점진적 변화)",
            "call_response": "콜 앤 리스폰스 구조(질문과 응답 형식)",
            "sonata": "소나타 구조(제시부, 발전부, 재현부)",
            "theme_variations": "주제와 변주 구조(기본 주제 제시 후 다양한 변주)",
            "freestyle": "자유로운 구조(전통적 구조에 얽매이지 않음)"
        }
    
    def get_prompt_structure(self) -> Dict[str, Any]:
        """
        Suno 모델에 최적화된 프롬프트 구조를 반환합니다.
        
        Returns:
            프롬프트 구조 정보를 담은 딕셔너리
        """
        return {
            "components": [
                "genre_style",
                "mood_emotion",
                "lyrics_theme",
                "instrumentation",
                "vocal_style",
                "song_structure",
                "reference_artists",
                "technical_specifications"
            ],
            "recommended_order": [
                "genre_style",
                "mood_emotion",
                "lyrics_theme",
                "instrumentation",
                "vocal_style",
                "song_structure",
                "reference_artists",
                "technical_specifications"
            ],
            "optional_components": [
                "song_structure",
                "reference_artists",
                "technical_specifications"
            ]
        }
    
    def optimize_prompt(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """
        분석 결과와 의도 결과를 기반으로 Suno에 최적화된 프롬프트를 생성합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            최적화된 프롬프트 문자열
        """
        # 1. 장르와 스타일 생성
        genre = self._generate_genre(analysis_result, intent_result)
        
        # 2. 분위기와 감정 생성
        mood = self._generate_mood(analysis_result, intent_result)
        
        # 3. 가사 주제 생성
        lyrics = self._generate_lyrics_theme(analysis_result, intent_result)
        
        # 4. 악기 구성 생성
        instruments = self._generate_instrumentation(analysis_result, intent_result)
        
        # 5. 보컬 스타일 생성
        vocal = self._generate_vocal_style(analysis_result, intent_result)
        
        # 6. 곡 구조 생성
        structure = self._generate_structure(analysis_result, intent_result)
        
        # 7. 참조 아티스트 생성
        references = self._generate_references(analysis_result, intent_result)
        
        # 8. 기술적 명세 생성
        technical = self._generate_technical(analysis_result, intent_result)
        
        # 9. 최종 프롬프트 조합
        # Suno는 명확하고 구체적인 프롬프트를 선호함
        prompt_parts = []
        
        # 장르와 스타일 (필수)
        if genre:
            prompt_parts.append(genre)
        
        # 분위기와 감정
        if mood:
            prompt_parts.append(mood)
        
        # 가사 주제
        if lyrics:
            prompt_parts.append(lyrics)
        
        # 악기 구성
        if instruments:
            prompt_parts.append(instruments)
        
        # 보컬 스타일
        if vocal:
            prompt_parts.append(vocal)
        
        # 곡 구조
        if structure:
            prompt_parts.append(structure)
        
        # 참조 아티스트
        if references:
            prompt_parts.append(references)
        
        # 기술적 명세
        if technical:
            prompt_parts.append(technical)
        
        # 최종 프롬프트 생성
        optimized_prompt = ", ".join(filter(None, prompt_parts))
        
        # 공통 규칙 적용
        optimized_prompt = self.apply_common_rules(optimized_prompt)
        
        return optimized_prompt
    
    def get_generation_parameters(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suno 모델의 음악 생성 매개변수를 반환합니다.
        
        Args:
            analysis_result: 입력 분석 결과
            intent_result: 의도 감지 결과
            
        Returns:
            생성 매개변수를 담은 딕셔너리
        """
        # 장르 유형 감지
        genre_type = self._detect_genre_type(analysis_result.get("input_text", ""))
        
        # 기본 생성 매개변수
        generation_params = {
            "duration": 180,  # 기본 3분
            "tempo": "medium",
            "key": "C major",
            "time_signature": "4/4",
            "quality": "high",
            "format": "mp3"
        }
        
        # 장르별 매개변수 조정
        if genre_type == "hiphop":
            generation_params.update({
                "tempo": "medium-fast",
                "emphasis": "rhythm"
            })
        elif genre_type == "electronic":
            generation_params.update({
                "tempo": "fast",
                "emphasis": "beat",
                "effects": ["reverb", "delay"]
            })
        elif genre_type == "classical":
            generation_params.update({
                "duration": 240,  # 4분
                "tempo": "varied",
                "emphasis": "melody",
                "dynamics": "varied"
            })
        elif genre_type == "jazz":
            generation_params.update({
                "tempo": "varied",
                "emphasis": "improvisation",
                "swing": True
            })
        
        # 복잡성에 따른 조정
        complexity = analysis_result.get("complexity", "medium")
        if complexity == "high":
            generation_params["duration"] = 300  # 5분
            generation_params["arrangement"] = "complex"
        elif complexity == "low":
            generation_params["duration"] = 120  # 2분
            generation_params["arrangement"] = "simple"
        
        return generation_params
    
    def _generate_genre(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """장르와 스타일을 생성합니다."""
        # 기본 장르 설명
        input_text = analysis_result.get("input_text", "")
        
        # 장르 유형 감지
        genre_type = self._detect_genre_type(input_text)
        
        # 장르 세부 정보 추출
        genre_details = self._extract_genre_details(input_text, genre_type)
        
        # 장르 템플릿 선택 및 적용
        if genre_type in self.music_templates:
            template = self.music_templates[genre_type]
            
            # 템플릿 변수 채우기
            for key, value in genre_details.items():
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
    
    def _detect_genre_type(self, text: str) -> str:
        """입력 텍스트에서 장르 유형을 감지합니다."""
        # 간단한 키워드 기반 감지 (실제로는 더 복잡한 분류 로직 필요)
        keywords = {
            "pop": ["팝", "대중음악", "팝송", "팝스타", "팝 음악"],
            "rock": ["록", "락", "록음악", "기타", "밴드", "헤비메탈", "메탈"],
            "hiphop": ["힙합", "랩", "래퍼", "비트", "플로우", "라임"],
            "electronic": ["일렉트로닉", "EDM", "테크노", "하우스", "트랜스", "신디사이저"],
            "jazz": ["재즈", "스윙", "즉흥연주", "색소폰", "트럼펫"],
            "classical": ["클래식", "오케스트라", "교향곡", "협주곡", "소나타"],
            "folk": ["포크", "어쿠스틱", "전통음악", "민속음악"],
            "rnb": ["R&B", "알앤비", "소울", "리듬앤블루스"],
            "soundtrack": ["사운드트랙", "영화음악", "배경음악", "OST", "테마곡"]
        }
        
        # 텍스트를 소문자로 변환
        text_lower = text.lower()
        
        # 각 유형별 키워드 매칭 점수 계산
        scores = {}
        for genre_type, type_keywords in keywords.items():
            score = sum(1 for keyword in type_keywords if keyword in text_lower)
            scores[genre_type] = score
        
        # 가장 높은 점수의 유형 반환
        if scores:
            max_type = max(scores.items(), key=lambda x: x[1])
            if max_type[1] > 0:
                return max_type[0]
        
        # 기본값은 pop
        return "pop"
    
    def _extract_genre_details(self, text: str, genre_type: str) -> Dict[str, str]:
        """입력 텍스트에서 장르 세부 정보를 추출합니다."""
        # 기본 세부 정보
        details = {}
        
        # 분위기 추출
        mood_patterns = ["밝은", "슬픈", "에너지", "차분한", "극적인", "로맨틱한", "신비로운", "향수", "웅장한", "장난스러운"]
        for pattern in mood_patterns:
            if pattern in text:
                details["mood"] = pattern
                break
        
        # 보컬 스타일 추출
        vocal_patterns = ["파워풀", "부드러운", "허스키", "매끄러운", "소울풀", "오페라", "랩", "숨이 섞인", "오토튠", "합창"]
        for pattern in vocal_patterns:
            if pattern in text:
                details["vocal_style"] = pattern
                break
        
        # 주제 추출
        theme_patterns = ["사랑", "이별", "희망", "꿈", "여행", "자연", "도시", "인생", "우정", "성장"]
        for pattern in theme_patterns:
            if pattern in text:
                details["theme"] = pattern
                break
        
        # 악기 구성 추출
        instrument_patterns = ["밴드", "오케스트라", "전자", "어쿠스틱", "힙합", "재즈", "록", "팝", "미니멀", "실험적"]
        for pattern in instrument_patterns:
            if pattern in text:
                details["instruments"] = pattern
                break
        
        # 구조 추출
        structure_patterns = ["버스-코러스", "앰비언트", "빌드업-드롭", "AABA", "스루 컴포즈드", "루프", "콜 앤 리스폰스"]
        for pattern in structure_patterns:
            if pattern in text:
                details["structure"] = pattern
                break
        
        # 기본 설명 추가
        details["description"] = text
        
        return details
    
    def _generate_mood(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """분위기와 감정을 생성합니다."""
        # 분위기 정보 추출
        moods = analysis_result.get("mood", [])
        
        # 분위기가 명시적으로 지정된 경우
        if moods:
            mood_texts = []
            for mood in moods:
                if mood in self.mood_templates:
                    mood_texts.append(self.mood_templates[mood])
                else:
                    mood_texts.append(mood)
            
            return ", ".join(mood_texts)
        
        # 장르 유형에 따른 기본 분위기 선택
        genre_type = self._detect_genre_type(analysis_result.get("input_text", ""))
        
        if genre_type == "pop":
            return "밝고 경쾌한 분위기"
        elif genre_type == "rock":
            return "에너지 넘치고 강렬한 분위기"
        elif genre_type == "hiphop":
            return "자신감 있고 도시적인 분위기"
        elif genre_type == "electronic":
            return "미래적이고 몽환적인 분위기"
        elif genre_type == "jazz":
            return "세련되고 부드러운 분위기"
        elif genre_type == "classical":
            return "우아하고 감성적인 분위기"
        elif genre_type == "folk":
            return "따뜻하고 친근한 분위기"
        elif genre_type == "rnb":
            return "감성적이고 부드러운 분위기"
        elif genre_type == "soundtrack":
            return "극적이고 감동적인 분위기"
        
        # 기본 분위기
        return "감정이 풍부한 분위기"
    
    def _generate_lyrics_theme(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """가사 주제를 생성합니다."""
        # 가사 주제 정보 추출
        lyrics_theme = analysis_result.get("lyrics_theme", "")
        
        # 가사 주제가 명시적으로 지정된 경우
        if lyrics_theme:
            return f"{lyrics_theme}에 관한 가사"
        
        # 장르 유형에 따른 기본 가사 주제 선택
        genre_type = self._detect_genre_type(analysis_result.get("input_text", ""))
        
        if genre_type == "pop":
            return "사랑과 관계에 관한 가사"
        elif genre_type == "rock":
            return "자유와 반항에 관한 가사"
        elif genre_type == "hiphop":
            return "자신의 경험과 성공에 관한 가사"
        elif genre_type == "electronic":
            return "축제와 자유에 관한 가사, 또는 가사 없음"
        elif genre_type == "jazz":
            return "감성과 인생에 관한 가사"
        elif genre_type == "folk":
            return "자연과 인생의 여정에 관한 가사"
        elif genre_type == "rnb":
            return "사랑과 관계의 깊은 감정에 관한 가사"
        elif genre_type == "soundtrack":
            return "영화나 이야기의 주제에 맞는 가사, 또는 가사 없음"
        
        # 기본 가사 주제
        return "보편적인 감정과 경험에 관한 가사"
    
    def _generate_instrumentation(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """악기 구성을 생성합니다."""
        # 악기 구성 정보 추출
        instruments = analysis_result.get("instruments", [])
        
        # 악기 구성이 명시적으로 지정된 경우
        if instruments:
            instrument_texts = []
            for instrument in instruments:
                if instrument in self.instrument_templates:
                    instrument_texts.append(self.instrument_templates[instrument])
                else:
                    instrument_texts.append(instrument)
            
            return ", ".join(instrument_texts)
        
        # 장르 유형에 따른 기본 악기 구성 선택
        genre_type = self._detect_genre_type(analysis_result.get("input_text", ""))
        
        if genre_type == "pop":
            return self.instrument_templates["pop"]
        elif genre_type == "rock":
            return self.instrument_templates["rock"]
        elif genre_type == "hiphop":
            return self.instrument_templates["hiphop"]
        elif genre_type == "electronic":
            return self.instrument_templates["electronic"]
        elif genre_type == "jazz":
            return self.instrument_templates["jazz"]
        elif genre_type == "classical":
            return self.instrument_templates["orchestra"]
        elif genre_type == "folk":
            return self.instrument_templates["acoustic"]
        elif genre_type == "rnb":
            return "R&B 구성(피아노, 베이스, 드럼, 신디사이저, 때로는 현악기)"
        elif genre_type == "soundtrack":
            return self.instrument_templates["orchestra"]
        
        # 기본 악기 구성
        return "다양한 악기 구성"
    
    def _generate_vocal_style(self, analysis_result: Dict[str, Any], intent_result: Dict[str, Any]) -> str:
        """보컬 스타일을 생성합니다."""
        # 보컬 스타일 정보 추출
        vocal_styles = analysis_result.get("vocal_styles", [])
        
        # 보컬 스타일이 명시적으로 지정된 경우
        if vocal_styles:
            vocal_texts = []
            for style in vocal_styles:
                if style in self.vocal_templates:
                    vocal_texts.append(self.vocal_templates[style])
                else:
                    vocal_texts.append(style)
            
            return ", ".join(vocal_texts)
        
        # 장르 유형에 따른 기본 보컬 스타일 선택
        genre_type = self._detect_genre_type(analysis_result.get("input_text", ""))
        
        if genre_type == "pop":
            return self.vocal_templates["pop"]