"""
InputAnalyzer 클래스 단위 테스트
"""

import pytest
from typing import Dict, Any, List
from src.utils.input_analyzer import InputAnalyzer


class TestInputAnalyzer:
    """InputAnalyzer 클래스 테스트"""
    
    @pytest.fixture
    def analyzer(self):
        """InputAnalyzer 인스턴스를 반환합니다."""
        return InputAnalyzer()
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_analyzer_initialization(self, analyzer):
        """InputAnalyzer 초기화 테스트"""
        assert analyzer is not None
        assert hasattr(analyzer, 'task_keywords')
        assert hasattr(analyzer, 'style_keywords')
        assert hasattr(analyzer, 'complexity_indicators')
        
        # 키워드 사전들이 비어있지 않은지 확인
        assert len(analyzer.task_keywords) > 0
        assert len(analyzer.style_keywords) > 0
        assert len(analyzer.complexity_indicators) > 0
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_basic_analyze_functionality(self, analyzer):
        """기본 분석 기능 테스트"""
        input_text = "안녕하세요. 간단한 블로그 포스트를 작성해주세요."
        model_id = "gpt-4o"
        
        result = analyzer.analyze(input_text, model_id)
        
        # 필수 키들이 존재하는지 확인
        required_keys = [
            "input_text", "selected_model", "model_category", "keywords",
            "task_type", "style", "complexity", "entities",
            "structure_hints", "constraints"
        ]
        
        for key in required_keys:
            assert key in result, f"Required key '{key}' is missing from result"
        
        # 반환값 타입 검증
        assert isinstance(result["input_text"], str)
        assert isinstance(result["selected_model"], str)
        assert isinstance(result["keywords"], list)
        assert isinstance(result["task_type"], list)
        assert isinstance(result["style"], list)
        assert isinstance(result["complexity"], str)
        assert isinstance(result["entities"], list)
        assert isinstance(result["structure_hints"], dict)
        assert isinstance(result["constraints"], dict)
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_keyword_extraction(self, analyzer):
        """키워드 추출 기능 테스트"""
        test_cases = [
            {
                "input": "Python 프로그래밍 언어를 사용한 웹 개발 프로젝트",
                "expected_keywords": ["python", "프로그래밍", "언어", "웹", "개발", "프로젝트"]
            },
            {
                "input": "아름다운 일몰 풍경 사진을 촬영하고 싶습니다",
                "expected_keywords": ["아름다운", "일몰", "풍경", "사진", "촬영"]
            },
            {
                "input": "명상과 휴식을 위한 클래식 음악 추천해주세요",
                "expected_keywords": ["명상", "휴식", "클래식", "음악", "추천"]
            }
        ]
        
        for case in test_cases:
            keywords = analyzer._extract_keywords(case["input"])
            
            # 키워드가 추출되었는지 확인
            assert len(keywords) > 0
            
            # 예상 키워드가 일부 포함되어 있는지 확인
            keywords_lower = [k.lower() for k in keywords]
            found_keywords = [k for k in case["expected_keywords"] if k in keywords_lower]
            assert len(found_keywords) > 0, f"No expected keywords found in {keywords}"
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_task_type_identification(self, analyzer):
        """작업 유형 식별 테스트"""
        test_cases = [
            {
                "input": "창의적인 소설을 작성해주세요",
                "expected_task": "creative_writing"
            },
            {
                "input": "기술 문서를 작성해 달라",
                "expected_task": "technical_writing"
            },
            {
                "input": "마케팅 슬로건을 만들어주세요",
                "expected_task": "marketing"
            },
            {
                "input": "이미지를 생성해주세요",
                "expected_task": "visual_creation"
            },
            {
                "input": "프로그래밍 코드를 작성해주세요",
                "expected_task": "code_generation"
            }
        ]
        
        for case in test_cases:
            task_types = analyzer._identify_task_type(case["input"])
            
            # 작업 유형이 식별되었는지 확인
            assert len(task_types) > 0
            
            # 예상 작업 유형이 최상위에 있는지 확인
            top_task = task_types[0][0] if task_types else None
            assert top_task == case["expected_task"], f"Expected {case['expected_task']}, got {top_task}"
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_style_identification(self, analyzer):
        """스타일 식별 테스트"""
        test_cases = [
            {
                "input": "공식적인 비즈니스 이메일을 작성해주세요",
                "expected_style": "formal"
            },
            {
                "input": "친근하고 캐주얼한 톤으로 작성해주세요",
                "expected_style": "casual"
            },
            {
                "input": "창의적이고 독창적인 아이디어를 제시해주세요",
                "expected_style": "creative"
            },
            {
                "input": "기술적이고 전문적인 설명을 부탁드립니다",
                "expected_style": "technical"
            }
        ]
        
        for case in test_cases:
            styles = analyzer._identify_style(case["input"])
            
            # 스타일이 식별되었는지 확인
            assert len(styles) > 0
            
            # 예상 스타일이 최상위에 있는지 확인
            top_style = styles[0][0] if styles else None
            assert top_style == case["expected_style"], f"Expected {case['expected_style']}, got {top_style}"
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_complexity_assessment(self, analyzer):
        """복잡성 평가 테스트"""
        test_cases = [
            {
                "input": "안녕",
                "expected_complexity": "low"
            },
            {
                "input": "간단한 설명을 작성해주세요. 기본적인 내용으로 부탁드립니다.",
                "expected_complexity": "medium"
            },
            {
                "input": "상세하고 포괄적인 분석을 포함한 전문적인 보고서를 작성해주세요. 복잡한 데이터 분석과 심층적인 인사이트를 포함하여 전문가 수준의 고급 내용으로 작성해야 합니다.",
                "expected_complexity": "high"
            }
        ]
        
        for case in test_cases:
            complexity = analyzer._assess_complexity(case["input"])
            assert complexity == case["expected_complexity"], f"Expected {case['expected_complexity']}, got {complexity}"
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_entity_extraction(self, analyzer):
        """엔티티 추출 테스트"""
        test_cases = [
            {
                "input": "Apple과 Google의 경쟁에 대해 설명해주세요",
                "expected_entities": ["Apple", "Google"]
            },
            {
                "input": "서울에서 부산까지 여행 계획을 세워주세요",
                "expected_entities": []  # 한글 엔티티는 기본 구현에서 추출되지 않음
            },
            {
                "input": "Python과 JavaScript 비교 분석",
                "expected_entities": ["Python", "JavaScript"]
            }
        ]
        
        for case in test_cases:
            entities = analyzer._extract_entities(case["input"])
            
            # 엔티티가 리스트인지 확인
            assert isinstance(entities, list)
            
            # 예상 엔티티가 포함되어 있는지 확인 (영어만)
            if case["expected_entities"]:
                for expected_entity in case["expected_entities"]:
                    assert expected_entity in entities or any(expected_entity.lower() in entity.lower() for entity in entities)
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_structure_hints_extraction(self, analyzer):
        """구조 힌트 추출 테스트"""
        test_cases = [
            {
                "input": "목록 형태로 정리해주세요",
                "expected_format": "list"
            },
            {
                "input": "표로 만들어주세요",
                "expected_format": "table"
            },
            {
                "input": "코드로 작성해주세요",
                "expected_format": "code"
            },
            {
                "input": "JSON 형식으로 출력해주세요",
                "expected_format": "json"
            }
        ]
        
        for case in test_cases:
            structure_hints = analyzer._extract_structure_hints(case["input"])
            
            # 구조 힌트가 딕셔너리인지 확인
            assert isinstance(structure_hints, dict)
            
            # 예상 형식이 감지되었는지 확인
            assert structure_hints.get("format") == case["expected_format"]
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_constraints_extraction(self, analyzer):
        """제약 조건 추출 테스트"""
        test_cases = [
            {
                "input": "전문적인 톤으로 작성해주세요",
                "expected_tone": "professional"
            },
            {
                "input": "친근한 어조로 부탁드립니다",
                "expected_tone": "friendly"
            },
            {
                "input": "초보자를 위한 설명으로 작성해주세요",
                "expected_audience": "beginner"
            },
            {
                "input": "전문가 대상으로 작성해주세요",
                "expected_audience": "expert"
            }
        ]
        
        for case in test_cases:
            constraints = analyzer._extract_constraints(case["input"])
            
            # 제약 조건이 딕셔너리인지 확인
            assert isinstance(constraints, dict)
            
            # 예상 톤이나 대상이 감지되었는지 확인
            if "expected_tone" in case:
                assert constraints.get("tone") == case["expected_tone"]
            if "expected_audience" in case:
                assert constraints.get("audience") == case["expected_audience"]
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_model_category_detection(self, analyzer):
        """모델 카테고리 감지 테스트"""
        test_cases = [
            {
                "model_id": "gpt-4o",
                "expected_category": "text"
            },
            {
                "model_id": "dall-e-3",
                "expected_category": "image"
            },
            {
                "model_id": "stable-diffusion-xl",
                "expected_category": "image"
            },
            {
                "model_id": "runway-gen-3",
                "expected_category": "video"
            },
            {
                "model_id": "unknown-model",
                "expected_category": "text"  # 기본값
            }
        ]
        
        for case in test_cases:
            category = analyzer._get_model_category(case["model_id"])
            assert category == case["expected_category"], f"Expected {case['expected_category']}, got {category}"
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    @pytest.mark.parametrize("edge_case", [
        {"name": "빈 문자열", "input": "", "model_id": "gpt-4o"},
        {"name": "공백만", "input": "   ", "model_id": "gpt-4o"},
        {"name": "특수 문자", "input": "!@#$%^&*()", "model_id": "gpt-4o"},
        {"name": "매우 긴 텍스트", "input": "테스트 " * 1000, "model_id": "gpt-4o"},
        {"name": "다국어", "input": "Hello 안녕하세요 こんにちは", "model_id": "gpt-4o"}
    ])
    def test_edge_cases(self, analyzer, edge_case):
        """엣지 케이스 테스트"""
        try:
            result = analyzer.analyze(edge_case["input"], edge_case["model_id"])
            
            # 기본 구조가 유지되는지 확인
            assert isinstance(result, dict)
            assert "input_text" in result
            assert "selected_model" in result
            assert result["input_text"] == edge_case["input"]
            assert result["selected_model"] == edge_case["model_id"]
            
        except Exception as e:
            # 예외가 발생하면 로그에 기록
            pytest.fail(f"Edge case '{edge_case['name']}' failed with error: {str(e)}")
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    @pytest.mark.benchmark
    def test_performance(self, analyzer, benchmark):
        """성능 테스트"""
        input_text = "중간 크기의 텍스트 입력으로 성능을 측정합니다. " * 50
        model_id = "gpt-4o"
        
        # 성능 벤치마크 실행
        result = benchmark(analyzer.analyze, input_text, model_id)
        
        # 결과가 올바른지 확인
        assert isinstance(result, dict)
        assert "input_text" in result
    
    @pytest.mark.unit
    @pytest.mark.analyzer
    def test_analyze_integration(self, analyzer, sample_analysis_result):
        """통합 분석 기능 테스트"""
        input_text = "밝고 화창한 날에 해변에서 뛰노는 강아지의 사진을 생성해주세요"
        model_id = "imagen-3"
        
        result = analyzer.analyze(input_text, model_id)
        
        # 입력 텍스트와 모델 ID가 올바르게 설정되었는지 확인
        assert result["input_text"] == input_text
        assert result["selected_model"] == model_id
        
        # 모델 카테고리가 올바르게 감지되었는지 확인
        assert result["model_category"] == "image"
        
        # 키워드가 추출되었는지 확인
        keywords = [k.lower() for k in result["keywords"]]
        expected_keywords = ["강아지", "해변", "사진", "생성"]
        found_keywords = [k for k in expected_keywords if any(k in keyword for keyword in keywords)]
        assert len(found_keywords) > 0
        
        # 작업 유형이 올바르게 식별되었는지 확인
        task_types = [task[0] for task in result["task_type"]]
        assert "visual_creation" in task_types or "general" in task_types
        
        # 복잡성이 평가되었는지 확인
        assert result["complexity"] in ["low", "medium", "high"] 