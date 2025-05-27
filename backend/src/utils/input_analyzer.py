"""
입력 분석 모듈: 사용자 입력을 분석하여 주요 키워드, 의도, 요청 유형을 식별합니다.
"""

import re
from typing import Dict, List, Any, Tuple

class InputAnalyzer:
    """사용자 입력을 분석하여 프롬프트 최적화에 필요한 정보를 추출하는 클래스"""
    
    def __init__(self):
        # 작업 유형 키워드 (확장 가능)
        self.task_keywords = {
            "creative_writing": ["글", "시", "소설", "이야기", "스토리", "작성", "창작", "스크립트", "대본"],
            "technical_writing": ["기술", "문서", "보고서", "논문", "설명", "매뉴얼", "가이드"],
            "marketing": ["마케팅", "광고", "카피", "홍보", "슬로건", "캠페인"],
            "visual_creation": ["이미지", "그림", "사진", "디자인", "로고", "일러스트", "시각화"],
            "video_creation": ["비디오", "영상", "동영상", "애니메이션", "모션"],
            "code_generation": ["코드", "프로그래밍", "함수", "알고리즘", "개발"],
            "data_analysis": ["데이터", "분석", "통계", "차트", "그래프", "시각화"],
            "translation": ["번역", "통역", "언어 변환"],
            "summarization": ["요약", "축약", "핵심", "중요 포인트"],
            "question_answering": ["질문", "답변", "해결", "문제"]
        }
        
        # 스타일 키워드 (확장 가능)
        self.style_keywords = {
            "formal": ["공식적", "격식", "전문적", "학술적", "비즈니스"],
            "casual": ["캐주얼", "비격식", "친근한", "일상적"],
            "creative": ["창의적", "독창적", "혁신적", "예술적"],
            "technical": ["기술적", "전문적", "상세한", "정확한"],
            "persuasive": ["설득력", "영향력", "호소력"],
            "informative": ["정보", "교육적", "설명적"],
            "humorous": ["유머", "재미", "위트", "코믹"],
            "minimalist": ["간결", "최소한", "심플", "깔끔"]
        }
        
        # 복잡성 평가 지표
        self.complexity_indicators = {
            "high": ["상세", "복잡", "심층", "포괄적", "전문적", "고급"],
            "medium": ["중간", "균형", "적절한"],
            "low": ["간단", "기본", "쉬운", "초보적"]
        }

    def analyze(self, input_text: str, selected_model: str) -> Dict[str, Any]:
        """
        사용자 입력을 분석하여 프롬프트 최적화에 필요한 정보를 추출합니다.
        
        Args:
            input_text: 사용자가 입력한 기본 요청 텍스트
            selected_model: 사용자가 선택한 AI 모델 ID
            
        Returns:
            분석 결과를 담은 딕셔너리
        """
        # 기본 분석 결과 구조
        analysis_result = {
            "input_text": input_text,
            "selected_model": selected_model,
            "model_category": self._get_model_category(selected_model),
            "keywords": self._extract_keywords(input_text),
            "task_type": self._identify_task_type(input_text),
            "style": self._identify_style(input_text),
            "complexity": self._assess_complexity(input_text),
            "entities": self._extract_entities(input_text),
            "structure_hints": self._extract_structure_hints(input_text),
            "constraints": self._extract_constraints(input_text)
        }
        
        return analysis_result
    
    def _get_model_category(self, model_id: str) -> str:
        """모델 ID를 기반으로 모델 카테고리(텍스트, 이미지, 비디오)를 반환합니다."""
        text_models = ["gpt-4o", "claude-sonnet-4", "gemini-ultra", "llama-3"]
        image_models = ["dall-e-3", "midjourney-v6", "stable-diffusion-xl"]
        video_models = ["runway-gen-3"]
        
        model_id_lower = model_id.lower()
        
        for model in text_models:
            if model in model_id_lower:
                return "text"
                
        for model in image_models:
            if model in model_id_lower:
                return "image"
                
        for model in video_models:
            if model in model_id_lower:
                return "video"
                
        # 기본값은 텍스트 모델로 가정
        return "text"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """텍스트에서 중요 키워드를 추출합니다."""
        # 간단한 키워드 추출 로직 (실제로는 더 복잡한 NLP 기법 사용 가능)
        words = re.findall(r'\b\w+\b', text.lower())
        # 불용어 제거 (실제 구현에서는 더 포괄적인 불용어 목록 사용)
        stopwords = ["그", "이", "저", "것", "수", "를", "에", "의", "가", "은", "는", "이다", "있다", "하다"]
        keywords = [word for word in words if word not in stopwords and len(word) > 1]
        
        # 빈도수 기반 상위 키워드 추출
        keyword_freq = {}
        for word in keywords:
            if word in keyword_freq:
                keyword_freq[word] += 1
            else:
                keyword_freq[word] = 1
                
        # 빈도수 기준 상위 10개 키워드 반환
        sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_keywords[:10]]
    
    def _identify_task_type(self, text: str) -> List[Tuple[str, float]]:
        """텍스트에서 작업 유형을 식별합니다."""
        text_lower = text.lower()
        task_scores = {}
        
        # 각 작업 유형별 키워드 매칭 점수 계산
        for task, keywords in self.task_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            if score > 0:
                task_scores[task] = score / len(keywords)  # 정규화된 점수
        
        # 점수 기준 내림차순 정렬
        sorted_tasks = sorted(task_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 점수가 있는 작업이 없으면 기본값 반환
        if not sorted_tasks:
            return [("general", 1.0)]
            
        return sorted_tasks
    
    def _identify_style(self, text: str) -> List[Tuple[str, float]]:
        """텍스트에서 스타일을 식별합니다."""
        text_lower = text.lower()
        style_scores = {}
        
        # 각 스타일별 키워드 매칭 점수 계산
        for style, keywords in self.style_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            if score > 0:
                style_scores[style] = score / len(keywords)  # 정규화된 점수
        
        # 점수 기준 내림차순 정렬
        sorted_styles = sorted(style_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 점수가 있는 스타일이 없으면 기본값 반환
        if not sorted_styles:
            return [("neutral", 1.0)]
            
        return sorted_styles
    
    def _assess_complexity(self, text: str) -> str:
        """텍스트의 복잡성 수준을 평가합니다."""
        text_lower = text.lower()
        complexity_scores = {}
        
        # 복잡성 지표별 키워드 매칭 점수 계산
        for level, indicators in self.complexity_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in text_lower:
                    score += 1
            complexity_scores[level] = score
        
        # 가장 높은 점수의 복잡성 수준 반환
        if not complexity_scores or max(complexity_scores.values()) == 0:
            # 기본 복잡성 평가 로직 (텍스트 길이, 문장 구조 등 기반)
            word_count = len(text.split())
            if word_count > 50:
                return "high"
            elif word_count > 20:
                return "medium"
            else:
                return "low"
        
        return max(complexity_scores.items(), key=lambda x: x[1])[0]
    
    def _extract_entities(self, text: str) -> List[str]:
        """텍스트에서 중요 엔티티(인물, 장소, 조직 등)를 추출합니다."""
        # 간단한 엔티티 추출 로직 (실제로는 NER 모델 사용 가능)
        # 여기서는 대문자로 시작하는 단어를 엔티티로 간주 (영어 기준)
        entities = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        # 한글 고유명사 추출 (실제로는 한국어 NER 모델 사용 필요)
        # 여기서는 간단한 예시만 구현
        korean_entities = []
        
        return list(set(entities + korean_entities))
    
    def _extract_structure_hints(self, text: str) -> Dict[str, Any]:
        """텍스트에서 출력 구조에 관한 힌트를 추출합니다."""
        structure_hints = {
            "format": None,
            "sections": [],
            "length": None
        }
        
        # 형식 힌트 추출
        format_patterns = {
            "list": r'목록|리스트|항목|bullet|list',
            "table": r'표|테이블|table',
            "essay": r'에세이|논설|essay',
            "code": r'코드|프로그램|함수|code|function',
            "json": r'json|제이슨|JSON',
            "markdown": r'마크다운|markdown|MD'
        }
        
        for format_type, pattern in format_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                structure_hints["format"] = format_type
                break
        
        # 섹션 힌트 추출
        section_matches = re.findall(r'섹션|부분|챕터|section|part|chapter', text, re.IGNORECASE)
        if section_matches:
            # 섹션 수 추정 (간단한 로직)
            numbers = re.findall(r'\d+', text)
            if numbers:
                structure_hints["sections"] = [f"Section {i+1}" for i in range(min(int(numbers[0]), 10))]
        
        # 길이 힌트 추출
        length_patterns = {
            "short": r'짧은|간단한|short|brief',
            "medium": r'중간|medium',
            "long": r'긴|상세한|포괄적인|long|detailed|comprehensive'
        }
        
        for length_type, pattern in length_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                structure_hints["length"] = length_type
                break
                
        # 구체적인 단어/문장 수 힌트 추출
        word_count_match = re.search(r'(\d+)\s*(단어|words)', text, re.IGNORECASE)
        if word_count_match:
            structure_hints["word_count"] = int(word_count_match.group(1))
            
        sentence_count_match = re.search(r'(\d+)\s*(문장|sentences)', text, re.IGNORECASE)
        if sentence_count_match:
            structure_hints["sentence_count"] = int(sentence_count_match.group(1))
        
        return structure_hints
    
    def _extract_constraints(self, text: str) -> Dict[str, Any]:
        """텍스트에서 제약 조건을 추출합니다."""
        constraints = {
            "include": [],
            "exclude": [],
            "tone": None,
            "audience": None,
            "time_constraint": None
        }
        
        # 포함해야 할 요소 추출
        include_matches = re.findall(r'포함해야?\s*(?:함|합니다|할?|하세요)[\s\.:]*([^.!?]*)', text)
        include_matches += re.findall(r'반드시\s*([^.!?]*)', text)
        include_matches += re.findall(r'include\s*([^.!?]*)', text, re.IGNORECASE)
        
        for match in include_matches:
            if match.strip():
                constraints["include"].append(match.strip())
        
        # 제외해야 할 요소 추출
        exclude_matches = re.findall(r'제외해야?\s*(?:함|합니다|할?|하세요)[\s\.:]*([^.!?]*)', text)
        exclude_matches += re.findall(r'포함하지?\s*(?:말아야|마세요|않음|않습니다)[\s\.:]*([^.!?]*)', text)
        exclude_matches += re.findall(r'exclude\s*([^.!?]*)', text, re.IGNORECASE)
        exclude_matches += re.findall(r'avoid\s*([^.!?]*)', text, re.IGNORECASE)
        
        for match in exclude_matches:
            if match.strip():
                constraints["exclude"].append(match.strip())
        
        # 톤/어조 추출
        tone_patterns = {
            "professional": r'전문적|프로페셔널|professional',
            "friendly": r'친근한|우호적|friendly',
            "formal": r'격식|공식적|formal',
            "informal": r'비격식|informal|casual',
            "enthusiastic": r'열정적|enthusiastic',
            "serious": r'진지한|serious',
            "humorous": r'유머러스|재미있는|humorous|funny'
        }
        
        for tone, pattern in tone_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                constraints["tone"] = tone
                break
        
        # 대상 독자 추출
        audience_patterns = {
            "general": r'일반|대중|general|public',
            "expert": r'전문가|expert|specialist',
            "beginner": r'초보자|입문자|beginner|novice',
            "children": r'어린이|아동|children|kids',
            "teenager": r'청소년|teenager|adolescent',
            "adult": r'성인|adult'
        }
        
        for audience, pattern in audience_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                constraints["audience"] = audience
                break
        
        # 시간 제약 추출
        time_match = re.search(r'(\d+)\s*(분|시간|hours?|minutes?)', text, re.IGNORECASE)
        if time_match:
            value = int(time_match.group(1))
            unit = time_match.group(2)
            
            if '시간' in unit or 'hour' in unit.lower():
                constraints["time_constraint"] = f"{value} hours"
            else:
                constraints["time_constraint"] = f"{value} minutes"
        
        return constraints
