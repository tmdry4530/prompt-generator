"""
Prompt Template Library
사용 사례별 최적화된 프롬프트 템플릿 라이브러리
"""

from typing import Dict, List, Any
from enum import Enum


class TemplateCategory(Enum):
    """템플릿 카테고리 정의"""
    CODE_GENERATION = "code_generation"
    ANALYSIS = "analysis"
    WRITING = "writing"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    CREATIVE = "creative"
    EDUCATION = "education"
    BUSINESS = "business"


class PromptTemplateLibrary:
    """사용 사례별 최적화된 프롬프트 템플릿을 제공하는 라이브러리"""
    
    def __init__(self):
        self.templates = {
            TemplateCategory.CODE_GENERATION.value: {
                'gpt-4': {
                    'template': """다음 {language} 코드를 작성해주세요: {task}

**요구사항**:
1. 에러 핸들링 포함
2. 명확한 주석 추가
3. 모범 사례 적용
4. 테스트 가능한 코드

**출력 형식**:
- 완전한 코드
- 사용법 예시
- 주요 함수/클래스 설명""",
                    'variables': ['language', 'task']
                },
                'claude-3': {
                    'template': """<coding_request>
<language>{language}</language>
<task>{task}</task>
<requirements>
- 에러 핸들링 포함
- 코드 품질 최적화
- 상세한 주석
- 확장 가능한 구조
</requirements>
<output_structure>
code|explanation|usage_example|best_practices
</output_structure>
</coding_request>

위 요청에 따라 체계적으로 코드를 작성해주세요.""",
                    'variables': ['language', 'task']
                },
                'llama-2': {
                    'template': """{language} 코드 생성: {task}

요구사항:
- 간결하고 효율적인 코드
- 핵심 기능 중심
- 명확한 주석

출력: 실행 가능한 코드와 간단한 설명""",
                    'variables': ['language', 'task']
                },
                'gemini-pro': {
                    'template': """**코드 생성 요청**
언어: {language}
작업: {task}

**구현 접근법**:
1. 요구사항 분석
2. 구조 설계
3. 단계별 구현
4. 테스트 및 최적화

**출력 구성**:
- 메인 코드
- 유틸리티 함수
- 사용 예시
- 성능 고려사항""",
                    'variables': ['language', 'task']
                }
            },
            
            TemplateCategory.ANALYSIS.value: {
                'gpt-4': {
                    'template': """다음 {subject}에 대해 심층 분석해주세요: {content}

**분석 프레임워크**:
1. **개요**: 주요 내용 요약
2. **핵심 발견사항**: 중요한 인사이트들
3. **시사점**: 의미와 영향
4. **권장사항**: 실행 가능한 제안

**분석 관점**:
- 데이터 기반 접근
- 다각적 시각
- 실용적 결론""",
                    'variables': ['subject', 'content']
                },
                'claude-3': {
                    'template': """<analysis_request>
<subject>{subject}</subject>
<content>{content}</content>
<methodology>
- 체계적 분석 접근
- 객관적 평가
- 논리적 추론
- 증거 기반 결론
</methodology>
<output_structure>
executive_summary|key_findings|implications|recommendations|supporting_evidence
</output_structure>
</analysis_request>

상기 내용에 대해 전문적이고 철저한 분석을 수행해주세요.""",
                    'variables': ['subject', 'content']
                },
                'llama-2': {
                    'template': """{subject} 분석: {content}

분석 요소:
- 핵심 포인트 식별
- 중요 패턴 파악
- 실용적 결론

출력: 구조화된 분석 결과와 핵심 인사이트""",
                    'variables': ['subject', 'content']
                },
                'gemini-pro': {
                    'template': """**분석 대상**: {subject}
**분석 내용**: {content}

**분석 방법론**:
1. 다차원적 데이터 검토
2. 패턴 및 트렌드 식별
3. 인과관계 분석
4. 예측 및 전망

**결과 구성**:
- 요약 및 핵심 메시지
- 상세 분석 결과
- 시각적 표현 제안
- 후속 조치 방안""",
                    'variables': ['subject', 'content']
                }
            },
            
            TemplateCategory.WRITING.value: {
                'gpt-4': {
                    'template': """{type} 작성을 도와주세요: {topic}

**작성 요구사항**:
- 목적: {purpose}
- 대상 독자: {audience}
- 분량: {length}
- 톤앤매너: {tone}

**구성 요소**:
1. 매력적인 서론
2. 논리적인 본론
3. 강력한 결론
4. 필요시 참고자료

**품질 기준**:
- 명확성과 일관성
- 독창성과 창의성
- 실용성과 유용성""",
                    'variables': ['type', 'topic', 'purpose', 'audience', 'length', 'tone']
                },
                'claude-3': {
                    'template': """<writing_request>
<document_type>{type}</document_type>
<topic>{topic}</topic>
<purpose>{purpose}</purpose>
<target_audience>{audience}</target_audience>
<length>{length}</length>
<tone>{tone}</tone>
<requirements>
- 체계적인 구성
- 논리적 흐름
- 독자 중심 접근
- 명확한 메시지
</requirements>
</writing_request>

위 조건에 맞는 고품질 문서를 작성해주세요.""",
                    'variables': ['type', 'topic', 'purpose', 'audience', 'length', 'tone']
                },
                'llama-2': {
                    'template': """{type} 작성: {topic}

목적: {purpose}
독자: {audience}
길이: {length}
톤: {tone}

요구사항:
- 명확한 메시지
- 체계적 구성
- 읽기 쉬운 문체

출력: 완성된 문서""",
                    'variables': ['type', 'topic', 'purpose', 'audience', 'length', 'tone']
                },
                'gemini-pro': {
                    'template': """**문서 작성 요청**
유형: {type}
주제: {topic}
목적: {purpose}
대상: {audience}
분량: {length}
스타일: {tone}

**작성 전략**:
1. 독자 니즈 분석
2. 핵심 메시지 구성
3. 효과적인 구조 설계
4. 매력적인 표현 활용

**결과물 특징**:
- 독자 친화적
- 목적 달성 중심
- 실행 가능한 내용
- 기억에 남는 메시지""",
                    'variables': ['type', 'topic', 'purpose', 'audience', 'length', 'tone']
                }
            },
            
            TemplateCategory.SUMMARIZATION.value: {
                'gpt-4': {
                    'template': """다음 내용을 {format} 형식으로 요약해주세요: {content}

**요약 기준**:
- 핵심 내용 보존
- {length} 분량
- 원문의 논조 유지
- 중요도 순 정렬

**포함 요소**:
1. 핵심 메시지
2. 주요 데이터/사실
3. 결론 및 시사점
4. 추가 고려사항 (필요시)

**출력 품질**:
- 명확성과 간결성
- 완전성과 정확성""",
                    'variables': ['format', 'content', 'length']
                },
                'claude-3': {
                    'template': """<summarization_request>
<content>{content}</content>
<format>{format}</format>
<target_length>{length}</target_length>
<criteria>
- 핵심 정보 보존
- 논리적 구조 유지
- 객관적 관점
- 실용적 가치
</criteria>
</summarization_request>

위 내용을 요청된 형식으로 체계적으로 요약해주세요.""",
                    'variables': ['content', 'format', 'length']
                },
                'llama-2': {
                    'template': """내용 요약: {content}

형식: {format}
길이: {length}

요구사항:
- 핵심 내용 위주
- 간결하고 명확
- 중요도 순 배열

출력: 구조화된 요약""",
                    'variables': ['content', 'format', 'length']
                },
                'gemini-pro': {
                    'template': """**요약 작업**
원본 내용: {content}
요약 형식: {format}
목표 길이: {length}

**요약 방법론**:
1. 핵심 테마 추출
2. 중요도 기반 선별
3. 논리적 재구성
4. 명확성 최적화

**결과 특성**:
- 완전성과 간결성 균형
- 원문 의도 보존
- 실용적 활용 가능
- 독립적 이해 가능""",
                    'variables': ['content', 'format', 'length']
                }
            }
        }
        
        # 예시 작업들 정의
        self.example_tasks = {
            'gpt-4': [
                "CSV 파일을 처리하는 Python 함수 작성",
                "초보자를 위한 양자컴퓨팅 설명",
                "스타트업을 위한 마케팅 전략 수립",
                "React 컴포넌트 최적화 방법",
                "API 보안 가이드라인 작성"
            ],
            'claude-3': [
                "연구논문 분석 및 핵심 내용 요약",
                "머신러닝 종합 튜토리얼 작성",
                "코드 보안 취약점 검토",
                "비즈니스 프로세스 분석 및 개선안",
                "기술 문서 품질 평가"
            ],
            'llama-2': [
                "Node.js REST API 간단 구현",
                "기사 내용을 3개 요점으로 요약",
                "Python 코드를 JavaScript로 변환",
                "효율적인 알고리즘 추천",
                "빠른 프로토타입 개발"
            ],
            'gemini-pro': [
                "멀티모달 데이터 분석",
                "이미지와 텍스트 통합 처리",
                "실시간 정보 검색 및 요약",
                "복합 문서 자동 생성",
                "인터랙티브 튜토리얼 제작"
            ]
        }
    
    def get_template(self, category: str, model: str) -> Dict[str, Any]:
        """특정 카테고리와 모델에 대한 템플릿 반환"""
        return self.templates.get(category, {}).get(model, {})
    
    def get_all_categories(self) -> List[str]:
        """모든 템플릿 카테고리 반환"""
        return list(self.templates.keys())
    
    def get_example_tasks(self, model: str) -> List[str]:
        """특정 모델에 대한 예시 작업들 반환"""
        return self.example_tasks.get(model, [])
    
    def apply_template(self, category: str, model: str, variables: Dict[str, str]) -> str:
        """템플릿에 변수를 적용하여 완성된 프롬프트 생성"""
        template_data = self.get_template(category, model)
        if not template_data:
            return f"카테고리 '{category}' 또는 모델 '{model}'에 대한 템플릿을 찾을 수 없습니다."
        
        template = template_data.get('template', '')
        try:
            return template.format(**variables)
        except KeyError as e:
            missing_var = str(e).strip("'")
            return f"필수 변수 '{missing_var}'가 누락되었습니다. 필요한 변수: {template_data.get('variables', [])}"
    
    def get_template_variables(self, category: str, model: str) -> List[str]:
        """특정 템플릿의 필수 변수 목록 반환"""
        template_data = self.get_template(category, model)
        return template_data.get('variables', []) 