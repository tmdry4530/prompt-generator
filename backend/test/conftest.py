"""
pytest 공통 설정 및 픽스처
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, List

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def mock_input_analyzer():
    """InputAnalyzer 모의 객체를 반환합니다."""
    from src.utils.input_analyzer import InputAnalyzer
    
    analyzer = Mock(spec=InputAnalyzer)
    analyzer.analyze.return_value = {
        "input_text": "테스트 입력",
        "selected_model": "test-model",
        "model_category": "text",
        "keywords": ["테스트", "입력"],
        "task_type": [("general", 1.0)],
        "style": [("neutral", 1.0)],
        "complexity": "medium",
        "entities": ["테스트"],
        "structure_hints": {"format": None, "sections": [], "length": None},
        "constraints": {"include": [], "exclude": [], "tone": None, "audience": None, "time_constraint": None}
    }
    return analyzer


@pytest.fixture
def mock_base_model():
    """BaseModel 모의 객체를 반환합니다."""
    from src.models.base_model import BaseModel
    
    model = Mock(spec=BaseModel)
    model.model_id = "test-model"
    model.model_name = "Test Model"
    model.provider = "Test Provider"
    model.capabilities = ["test_capability"]
    model.supports_multimodal = False
    model.max_tokens = 1000
    model.best_practices = ["테스트 모범 사례"]
    
    model.optimize_prompt.return_value = "최적화된 테스트 프롬프트"
    model.get_model_info.return_value = {
        "model_id": "test-model",
        "model_name": "Test Model",
        "provider": "Test Provider",
        "capabilities": ["test_capability"],
        "supports_multimodal": False
    }
    model.get_prompt_structure.return_value = {
        "components": ["test_component"],
        "recommended_order": ["test_component"],
        "optional_components": []
    }
    
    return model


@pytest.fixture
def sample_analysis_result() -> Dict[str, Any]:
    """샘플 입력 분석 결과를 반환합니다."""
    return {
        "input_text": "밝고 화창한 날에 해변에서 뛰노는 강아지의 사진을 생성해주세요",
        "selected_model": "imagen-3",
        "model_category": "image",
        "keywords": ["강아지", "해변", "사진", "생성"],
        "task_type": [("image_generation", 0.8)],
        "style": [("photorealistic", 0.9)],
        "complexity": "medium",
        "entities": ["강아지", "해변"],
        "structure_hints": {
            "format": "image",
            "sections": [],
            "length": None
        },
        "constraints": {
            "include": ["강아지", "해변"],
            "exclude": [],
            "tone": "friendly",
            "audience": "general",
            "time_constraint": None
        }
    }


@pytest.fixture
def sample_intent_result() -> Dict[str, Any]:
    """샘플 의도 감지 결과를 반환합니다."""
    return {
        "primary_intent": ("generate_content", 0.8),
        "is_creative": True,
        "is_technical": False,
        "urgency_level": "medium"
    }


@pytest.fixture
def text_model_test_cases() -> List[Dict[str, Any]]:
    """텍스트 모델 테스트 케이스를 반환합니다."""
    return [
        {
            "name": "기본 텍스트 생성",
            "input": "안녕하세요라는 인사말에 대한 설명을 작성해주세요",
            "expected_keywords": ["안녕하세요", "인사말", "설명"]
        },
        {
            "name": "기술 문서 작성",
            "input": "Python의 클래스 상속에 대해 상세한 기술 문서를 작성해주세요",
            "expected_keywords": ["Python", "클래스", "상속", "기술", "문서"]
        },
        {
            "name": "창작 글쓰기",
            "input": "우주를 배경으로 한 SF 소설의 첫 장을 창작해주세요",
            "expected_keywords": ["우주", "SF", "소설", "창작"]
        }
    ]


@pytest.fixture
def image_model_test_cases() -> List[Dict[str, Any]]:
    """이미지 모델 테스트 케이스를 반환합니다."""
    return [
        {
            "name": "간단한 초상화",
            "input": "웃는 여성의 초상화",
            "expected_subject_type": "portrait",
            "expected_keywords": ["여성", "초상화", "웃는"]
        },
        {
            "name": "복잡한 풍경",
            "input": "일몰 시간에 산 정상에서 바라본 아름다운 계곡, 사진 사실적, 고해상도",
            "expected_subject_type": "landscape",
            "expected_keywords": ["일몰", "산", "계곡", "사진", "고해상도"]
        },
        {
            "name": "제품 사진",
            "input": "고급 스마트폰 제품 사진, 스튜디오 조명, 미니멀한 배경",
            "expected_subject_type": "product",
            "expected_keywords": ["스마트폰", "제품", "스튜디오", "조명"]
        }
    ]


@pytest.fixture
def music_model_test_cases() -> List[Dict[str, Any]]:
    """음악 모델 테스트 케이스를 반환합니다."""
    return [
        {
            "name": "팝 음악",
            "input": "밝고 경쾌한 팝 음악, 사랑에 관한 가사",
            "expected_genre": "pop",
            "expected_keywords": ["팝", "밝고", "경쾌한", "사랑"]
        },
        {
            "name": "록 음악",
            "input": "에너지 넘치는 록 음악, 일렉트릭 기타 중심",
            "expected_genre": "rock",
            "expected_keywords": ["록", "에너지", "일렉트릭", "기타"]
        },
        {
            "name": "클래식 음악",
            "input": "우아한 클래식 음악, 오케스트라 편성",
            "expected_genre": "classical",
            "expected_keywords": ["클래식", "우아한", "오케스트라"]
        }
    ]


@pytest.fixture
def edge_case_inputs() -> List[Dict[str, Any]]:
    """엣지 케이스 입력들을 반환합니다."""
    return [
        {
            "name": "빈 입력",
            "input": "",
            "expected_error": True
        },
        {
            "name": "매우 긴 입력",
            "input": "테스트 " * 1000,
            "expected_error": False
        },
        {
            "name": "특수 문자",
            "input": "!@#$%^&*()_+-=[]{}|;':\",./<>?",
            "expected_error": False
        },
        {
            "name": "다국어 입력",
            "input": "Hello 안녕하세요 こんにちは 你好 Bonjour",
            "expected_error": False
        },
        {
            "name": "숫자만 입력",
            "input": "12345",
            "expected_error": False
        }
    ]


@pytest.fixture
def performance_test_data() -> Dict[str, Any]:
    """성능 테스트 데이터를 반환합니다."""
    return {
        "small_input": "간단한 테스트",
        "medium_input": "중간 크기의 테스트 입력" * 10,
        "large_input": "큰 크기의 테스트 입력" * 100,
        "iterations": 100,
        "max_response_time": 1.0  # 1초
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """각 테스트 실행 전 환경을 설정합니다."""
    # 테스트 환경 변수 설정
    os.environ["TESTING"] = "true"
    
    yield
    
    # 테스트 후 정리
    if "TESTING" in os.environ:
        del os.environ["TESTING"]


# 마커 등록
def pytest_configure(config):
    """pytest 설정을 구성합니다."""
    config.addinivalue_line("markers", "unit: 단위 테스트")
    config.addinivalue_line("markers", "integration: 통합 테스트")
    config.addinivalue_line("markers", "slow: 느린 테스트")
    config.addinivalue_line("markers", "model: 모델 관련 테스트")
    config.addinivalue_line("markers", "analyzer: 분석기 관련 테스트")
    config.addinivalue_line("markers", "optimizer: 최적화 관련 테스트") 