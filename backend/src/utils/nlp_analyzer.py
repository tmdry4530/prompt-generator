"""
NLP 기반 텍스트 분석 모듈
한국어와 영어를 위한 고급 텍스트 분석 기능을 제공합니다.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
import logging
from dataclasses import dataclass
from langdetect import detect, LangDetectException

# 언어별 NLP 라이브러리 임포트
try:
    import nltk
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False
    logging.warning("NLTK 라이브러리가 설치되지 않았습니다. 기본 분석 기능만 사용됩니다.")

# NLTK 데이터 다운로드 (필요시)
if NLP_AVAILABLE:
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except:
        pass


@dataclass
class NLPAnalysisResult:
    """NLP 분석 결과를 담는 데이터 클래스"""
    language: str
    tokens: List[str]
    pos_tags: List[Tuple[str, str]]
    entities: List[Dict[str, str]]
    key_phrases: List[str]
    sentiment: str
    intent: str
    complexity_score: float


class NLPAnalyzer:
    """고급 NLP 기반 텍스트 분석기"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize_nlp_models()
        
    def _initialize_nlp_models(self):
        """NLP 모델 초기화 (기본 NLTK만 사용)"""
        self.nltk_available = NLP_AVAILABLE
        
        if NLP_AVAILABLE:
            try:
                # NLTK 토크나이저 테스트
                nltk.word_tokenize("test")
                self.logger.info("NLTK 기본 분석기가 초기화되었습니다.")
            except:
                self.logger.info("NLTK 데이터가 완전히 다운로드되지 않았습니다.")
                self.nltk_available = False
    
    def analyze(self, text: str) -> NLPAnalysisResult:
        """텍스트를 종합적으로 분석"""
        # 언어 감지
        language = self._detect_language(text)
        
        # 언어별 분석 수행
        if language == 'ko':
            return self._analyze_korean(text)
        elif language == 'en':
            return self._analyze_english(text)
        else:
            # 기타 언어는 기본 분석
            return self._analyze_basic(text, language)
    
    def _detect_language(self, text: str) -> str:
        """텍스트의 언어를 감지"""
        try:
            lang = detect(text)
            return lang
        except LangDetectException:
            # 언어 감지 실패시 기본값으로 영어 반환
            return 'en'
    
    def _analyze_korean(self, text: str) -> NLPAnalysisResult:
        """한국어 텍스트 분석"""
        if not NLP_AVAILABLE or not self.nltk_available:
            return self._analyze_basic(text, 'ko')
        
        try:
            # 형태소 분석
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            
            # 명사 추출 (주요 키워드)
            nouns = [word for word, pos in pos_tags if pos.startswith('N')]
            
            # 엔티티 추출 (간단한 규칙 기반)
            entities = self._extract_korean_entities(text, pos_tags)
            
            # 핵심 구문 추출
            key_phrases = self._extract_korean_key_phrases(pos_tags, nouns)
            
            # 감성 분석 (간단한 규칙 기반)
            sentiment = self._analyze_korean_sentiment(text)
            
            # 의도 분류
            intent = self._classify_korean_intent(text, pos_tags)
            
            # 복잡도 점수
            complexity_score = self._calculate_complexity(text, tokens)
            
            return NLPAnalysisResult(
                language='ko',
                tokens=tokens,
                pos_tags=pos_tags,
                entities=entities,
                key_phrases=key_phrases,
                sentiment=sentiment,
                intent=intent,
                complexity_score=complexity_score
            )
        except Exception as e:
            self.logger.error(f"한국어 분석 오류: {e}")
            return self._analyze_basic(text, 'ko')
    
    def _analyze_english(self, text: str) -> NLPAnalysisResult:
        """영어 텍스트 분석"""
        if not NLP_AVAILABLE or not self.nltk_available:
            return self._analyze_basic(text, 'en')
        
        try:
            # NLTK 분석
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            
            # 엔티티 추출
            entities = self._extract_english_entities(text, pos_tags)
            
            # 핵심 구문 추출 (명사구)
            key_phrases = self._extract_english_key_phrases(pos_tags, tokens)
            
            # 감성 분석 (간단한 규칙 기반)
            sentiment = self._analyze_english_sentiment(text)
            
            # 의도 분류
            intent = self._classify_english_intent(text)
            
            # 복잡도 점수
            complexity_score = self._calculate_complexity(text, tokens)
            
            return NLPAnalysisResult(
                language='en',
                tokens=tokens,
                pos_tags=pos_tags,
                entities=entities,
                key_phrases=key_phrases,
                sentiment=sentiment,
                intent=intent,
                complexity_score=complexity_score
            )
        except Exception as e:
            self.logger.error(f"영어 분석 오류: {e}")
            return self._analyze_basic(text, 'en')
    
    def _analyze_basic(self, text: str, language: str) -> NLPAnalysisResult:
        """기본적인 텍스트 분석 (NLP 라이브러리 없이)"""
        # 단순 토큰화
        tokens = text.split()
        
        # 기본 품사 태깅 (단순화)
        pos_tags = [(token, 'UNKNOWN') for token in tokens]
        
        # 기본 엔티티 추출 (정규식 기반)
        entities = self._extract_basic_entities(text)
        
        # 핵심 구문 (긴 단어들)
        key_phrases = [word for word in tokens if len(word) > 5]
        
        # 기본 감성 분석
        sentiment = 'neutral'
        
        # 기본 의도 분류
        intent = self._classify_basic_intent(text)
        
        # 복잡도 점수
        complexity_score = len(text) / 100.0  # 매우 단순한 측정
        
        return NLPAnalysisResult(
            language=language,
            tokens=tokens,
            pos_tags=pos_tags,
            entities=entities,
            key_phrases=key_phrases,
            sentiment=sentiment,
            intent=intent,
            complexity_score=complexity_score
        )
    
    def _extract_korean_entities(self, text: str, pos_tags: List[Tuple[str, str]]) -> List[Dict[str, str]]:
        """한국어 엔티티 추출"""
        entities = []
        
        # 이메일 패턴
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            entities.append({
                'text': match.group(),
                'label': 'EMAIL',
                'start': match.start(),
                'end': match.end()
            })
        
        # 전화번호 패턴
        phone_pattern = r'(\d{2,3}-\d{3,4}-\d{4})|(\d{10,11})'
        for match in re.finditer(phone_pattern, text):
            entities.append({
                'text': match.group(),
                'label': 'PHONE',
                'start': match.start(),
                'end': match.end()
            })
        
        # 조직명/회사명 추출 (NNP 태그 활용)
        for word, tag in pos_tags:
            if tag == 'NNP' and len(word) > 1:  # 고유명사
                entities.append({
                    'text': word,
                    'label': 'ORG',
                    'start': text.find(word),
                    'end': text.find(word) + len(word)
                })
        
        return entities
    
    def _extract_korean_key_phrases(self, pos_tags: List[Tuple[str, str]], nouns: List[str]) -> List[str]:
        """한국어 핵심 구문 추출"""
        key_phrases = []
        
        # 명사구 추출
        current_phrase = []
        for word, tag in pos_tags:
            if tag.startswith('N'):  # 명사류
                current_phrase.append(word)
            else:
                if len(current_phrase) > 1:
                    key_phrases.append(' '.join(current_phrase))
                current_phrase = []
        
        # 마지막 구문 처리
        if len(current_phrase) > 1:
            key_phrases.append(' '.join(current_phrase))
        
        # 중요 명사 추가
        key_phrases.extend([noun for noun in nouns if len(noun) > 1])
        
        return list(set(key_phrases))  # 중복 제거
    
    def _analyze_korean_sentiment(self, text: str) -> str:
        """한국어 감성 분석 (간단한 규칙 기반)"""
        positive_words = ['좋다', '훌륭', '최고', '멋지다', '행복', '기쁘다', '사랑', '감사']
        negative_words = ['나쁘다', '싫다', '최악', '화나다', '슬프다', '실망', '문제', '오류']
        
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _classify_korean_intent(self, text: str, pos_tags: List[Tuple[str, str]]) -> str:
        """한국어 의도 분류"""
        # 질문 의도
        if any(word in text for word in ['?', '뭐', '무엇', '어떻게', '왜', '언제', '어디']):
            return 'question'
        
        # 요청/명령 의도
        if any(tag == 'VV' for _, tag in pos_tags):  # 동사가 있으면
            if any(word in text for word in ['해줘', '하세요', '부탁', '요청']):
                return 'request'
        
        # 설명/정보 제공
        if any(word in text for word in ['이다', '입니다', '있다']):
            return 'inform'
        
        return 'general'
    
    def _analyze_english_sentiment(self, text: str) -> str:
        """영어 감성 분석 (간단한 규칙 기반)"""
        positive_words = ['good', 'great', 'excellent', 'love', 'happy', 'wonderful', 'best']
        negative_words = ['bad', 'hate', 'terrible', 'worst', 'sad', 'angry', 'problem']
        
        tokens_lower = text.lower().split()
        
        positive_count = sum(1 for word in positive_words if word in tokens_lower)
        negative_count = sum(1 for word in negative_words if word in tokens_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _classify_english_intent(self, text: str) -> str:
        """영어 의도 분류"""
        # 질문 의도
        question_words = ['what', 'when', 'where', 'why', 'how', 'who', 'which']
        if text.strip().endswith('?') or any(word in question_words for word in text.split()):
            return 'question'
        
        # 요청/명령 의도
        imperative_verbs = ['please', 'could', 'would', 'can', 'help', 'need']
        if any(word in imperative_verbs for word in text.split()):
            return 'request'
        
        # 설명/정보 제공
        if any(word in text for word in ['is', 'are', 'was', 'were', 'has', 'have', 'had']):
            return 'inform'
        
        return 'general'
    
    def _extract_basic_entities(self, text: str) -> List[Dict[str, str]]:
        """기본적인 엔티티 추출 (정규식 기반)"""
        entities = []
        
        # URL 패턴
        url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        for match in re.finditer(url_pattern, text):
            entities.append({
                'text': match.group(),
                'label': 'URL',
                'start': match.start(),
                'end': match.end()
            })
        
        # 숫자 패턴
        number_pattern = r'\b\d+(?:\.\d+)?\b'
        for match in re.finditer(number_pattern, text):
            entities.append({
                'text': match.group(),
                'label': 'NUMBER',
                'start': match.start(),
                'end': match.end()
            })
        
        return entities
    
    def _classify_basic_intent(self, text: str) -> str:
        """기본적인 의도 분류"""
        text_lower = text.lower()
        
        if '?' in text:
            return 'question'
        elif any(word in text_lower for word in ['please', 'help', 'need', '부탁', '요청']):
            return 'request'
        else:
            return 'general'
    
    def _calculate_complexity(self, text: str, tokens: List[str]) -> float:
        """텍스트 복잡도 계산"""
        # 다양한 요소를 고려한 복잡도 점수
        sentence_count = len(re.split(r'[.!?]+', text))
        avg_word_length = sum(len(token) for token in tokens) / len(tokens) if tokens else 0
        unique_words = len(set(tokens))
        
        # 복잡도 점수 계산 (0-1 범위)
        complexity = min(1.0, (
            (sentence_count / 10) * 0.3 +  # 문장 수
            (avg_word_length / 10) * 0.3 +  # 평균 단어 길이
            (unique_words / len(tokens)) * 0.4 if tokens else 0  # 어휘 다양성
        ))
        
        return complexity
    
    def _extract_english_entities(self, text: str, pos_tags: List[Tuple[str, str]]) -> List[Dict[str, str]]:
        """영어 엔티티 추출 (기본 규칙 기반)"""
        entities = []
        
        # 기본 엔티티 추출 재사용
        entities.extend(self._extract_basic_entities(text))
        
        # 고유명사 추출
        for word, tag in pos_tags:
            if tag in ['NNP', 'NNPS'] and len(word) > 1:  # 고유명사
                entities.append({
                    'text': word,
                    'label': 'PERSON_OR_ORG',
                    'start': text.find(word),
                    'end': text.find(word) + len(word)
                })
        
        return entities
    
    def _extract_english_key_phrases(self, pos_tags: List[Tuple[str, str]], tokens: List[str]) -> List[str]:
        """영어 핵심 구문 추출"""
        key_phrases = []
        
        # 명사구 추출
        current_phrase = []
        for word, tag in pos_tags:
            if tag.startswith('N'):  # 명사류
                current_phrase.append(word)
            elif tag in ['JJ', 'JJR', 'JJS']:  # 형용사
                current_phrase.append(word)
            else:
                if len(current_phrase) > 1:
                    key_phrases.append(' '.join(current_phrase))
                current_phrase = []
        
        # 마지막 구문 처리
        if len(current_phrase) > 1:
            key_phrases.append(' '.join(current_phrase))
        
        # 중요한 단어들 추가 (길이가 긴 단어)
        key_phrases.extend([word for word in tokens if len(word) > 5])
        
        return list(set(key_phrases))  # 중복 제거 