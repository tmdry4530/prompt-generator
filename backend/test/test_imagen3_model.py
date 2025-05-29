"""
Imagen3Model 클래스 단위 테스트
"""

import pytest
from typing import Dict, Any
from src.models.image_models.imagen3_model import Imagen3Model


class TestImagen3Model:
    """Imagen3Model 클래스 테스트"""
    
    @pytest.fixture
    def imagen3_model(self):
        """Imagen3Model 인스턴스를 반환합니다."""
        return Imagen3Model()
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_model_initialization(self, imagen3_model):
        """모델 초기화 테스트"""
        assert imagen3_model.model_id == "imagen-3"
        assert imagen3_model.model_name == "Imagen 3"
        assert imagen3_model.provider == "Google"
        assert imagen3_model.max_tokens == 1000
        assert imagen3_model.supports_multimodal is False
        
        # 기능 목록 확인
        expected_capabilities = [
            "image_generation",
            "photorealistic_rendering",
            "artistic_rendering",
            "concept_visualization",
            "style_transfer"
        ]
        assert all(cap in imagen3_model.capabilities for cap in expected_capabilities)
        
        # 템플릿 사전들이 존재하는지 확인
        assert len(imagen3_model.subject_templates) > 0
        assert len(imagen3_model.style_templates) > 0
        assert len(imagen3_model.composition_templates) > 0
        assert len(imagen3_model.lighting_templates) > 0
        assert len(imagen3_model.negative_prompt_templates) > 0
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_get_prompt_structure(self, imagen3_model):
        """프롬프트 구조 반환 테스트"""
        structure = imagen3_model.get_prompt_structure()
        
        # 구조가 올바른지 확인
        assert isinstance(structure, dict)
        assert "components" in structure
        assert "recommended_order" in structure
        assert "optional_components" in structure
        
        # 예상 컴포넌트들이 포함되어 있는지 확인
        expected_components = [
            "subject_description",
            "style_specification",
            "composition_details",
            "lighting_details"
        ]
        
        for component in expected_components:
            assert component in structure["components"]
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_subject_type_detection(self, imagen3_model):
        """주제 유형 감지 테스트"""
        test_cases = [
            {
                "input": "웃는 여성의 초상화",
                "expected": "portrait"
            },
            {
                "input": "일몰 시간의 산 풍경",
                "expected": "landscape"
            },
            {
                "input": "고급 스마트폰 제품 사진",
                "expected": "product"
            },
            {
                "input": "미래적인 도시 컨셉 아트",
                "expected": "concept_art"
            },
            {
                "input": "추상적인 기하학적 패턴",
                "expected": "abstract"
            },
            {
                "input": "고딕 양식의 대성당 건물",
                "expected": "architecture"
            },
            {
                "input": "맛있는 파스타 요리 사진",
                "expected": "food"
            }
        ]
        
        for case in test_cases:
            detected_type = imagen3_model._detect_subject_type(case["input"])
            assert detected_type == case["expected"], f"Expected {case['expected']}, got {detected_type} for input: {case['input']}"
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_subject_details_extraction(self, imagen3_model):
        """주제 세부 정보 추출 테스트"""
        test_cases = [
            {
                "input": "아침에 웃는 여성의 초상화, 자연광 조명",
                "subject_type": "portrait",
                "expected_details": {
                    "description": "아침에 웃는 여성의 초상화, 자연광 조명",
                    "expression": "웃는",
                    "lighting": "자연광"
                }
            },
            {
                "input": "일몰 시간에 흐린 날씨의 산 풍경, 항공 촬영",
                "subject_type": "landscape",
                "expected_details": {
                    "description": "일몰 시간에 흐린 날씨의 산 풍경, 항공 촬영",
                    "time_of_day": "일몰",
                    "weather": "흐린",
                    "perspective": "항공"
                }
            }
        ]
        
        for case in test_cases:
            details = imagen3_model._extract_subject_details(
                case["input"], 
                case["subject_type"]
            )
            
            # 기본 설명이 포함되어 있는지 확인
            assert details["description"] == case["input"]
            
            # 예상 세부 정보가 추출되었는지 확인
            for key, expected_value in case["expected_details"].items():
                if key != "description":  # description은 이미 확인했음
                    assert key in details
                    assert details[key] == expected_value
    
    @pytest.mark.unit
    @pytest.mark.model
    @pytest.mark.parametrize("input_text,expected_style", [
        ("사진 사실적인 이미지", "photorealistic"),
        ("영화 같은 장면", "cinematic"),
        ("애니메이션 스타일", "anime"),
        ("디지털 아트", "digital_art"),
        ("유화 스타일", "oil_painting"),
        ("수채화 느낌", "watercolor"),
        ("3D 렌더링", "3d_render"),
        ("픽셀 아트", "pixel_art"),
        ("미니멀한 디자인", "minimalist"),
        ("판타지 스타일", "fantasy")
    ])
    def test_style_generation(self, imagen3_model, input_text, expected_style, sample_analysis_result, sample_intent_result):
        """스타일 생성 테스트"""
        # 분석 결과에 스타일 정보 설정
        sample_analysis_result["style"] = [(expected_style, 0.9)]
        
        style_text = imagen3_model._generate_style(sample_analysis_result, sample_intent_result)
        
        # 예상 스타일이 포함되어 있는지 확인
        assert len(style_text) > 0
        assert expected_style in imagen3_model.style_templates
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_composition_generation(self, imagen3_model, sample_analysis_result, sample_intent_result):
        """구도 생성 테스트"""
        test_cases = [
            {
                "composition": "wide_shot",
                "expected_template": "wide_shot"
            },
            {
                "composition": "close_up",
                "expected_template": "close_up"
            },
            {
                "composition": "rule_of_thirds",
                "expected_template": "rule_of_thirds"
            }
        ]
        
        for case in test_cases:
            # 분석 결과에 구도 정보 설정
            analysis_result = sample_analysis_result.copy()
            analysis_result["composition"] = case["composition"]
            
            composition_text = imagen3_model._generate_composition(analysis_result, sample_intent_result)
            
            # 구도 템플릿이 올바르게 선택되었는지 확인
            expected_text = imagen3_model.composition_templates[case["expected_template"]]
            assert composition_text == expected_text
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_lighting_generation(self, imagen3_model, sample_analysis_result, sample_intent_result):
        """조명 생성 테스트"""
        test_cases = [
            {
                "lighting": "natural",
                "expected_template": "natural"
            },
            {
                "lighting": "golden_hour",
                "expected_template": "golden_hour"
            },
            {
                "lighting": "dramatic",
                "expected_template": "dramatic"
            }
        ]
        
        for case in test_cases:
            # 분석 결과에 조명 정보 설정
            analysis_result = sample_analysis_result.copy()
            analysis_result["lighting"] = case["lighting"]
            
            lighting_text = imagen3_model._generate_lighting(analysis_result, sample_intent_result)
            
            # 조명 템플릿이 올바르게 선택되었는지 확인
            expected_text = imagen3_model.lighting_templates[case["expected_template"]]
            assert lighting_text == expected_text
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_color_palette_generation(self, imagen3_model, sample_analysis_result, sample_intent_result):
        """색상 팔레트 생성 테스트"""
        test_cases = [
            {
                "colors": ["빨간색", "파란색", "노란색"],
                "expected_contains": ["빨간색", "파란색", "노란색"]
            },
            {
                "mood": "warm",
                "expected_contains": ["따뜻한", "주황색", "노란색"]
            },
            {
                "mood": "cool",
                "expected_contains": ["차가운", "파란색", "보라색"]
            }
        ]
        
        for case in test_cases:
            # 분석 결과 설정
            analysis_result = sample_analysis_result.copy()
            if "colors" in case:
                analysis_result["colors"] = case["colors"]
            if "mood" in case:
                analysis_result["mood"] = case["mood"]
            
            palette_text = imagen3_model._generate_color_palette(analysis_result, sample_intent_result)
            
            # 예상 내용이 포함되어 있는지 확인
            if case["expected_contains"]:
                assert any(expected in palette_text for expected in case["expected_contains"])
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_negative_prompt_generation(self, imagen3_model, sample_analysis_result, sample_intent_result):
        """부정적 프롬프트 생성 테스트"""
        negative_prompt = imagen3_model._generate_negative_prompt(sample_analysis_result, sample_intent_result)
        
        # 부정적 프롬프트가 생성되었는지 확인
        assert len(negative_prompt) > 0
        
        # 기본 부정적 요소들이 포함되어 있는지 확인
        expected_negative_elements = ["저품질", "흐릿함", "왜곡된"]
        assert any(element in negative_prompt for element in expected_negative_elements)
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_technical_specs_generation(self, imagen3_model, sample_analysis_result, sample_intent_result):
        """기술적 명세 생성 테스트"""
        test_cases = [
            {
                "complexity": "high",
                "expected_contains": ["8K", "초고해상도", "세밀한"]
            },
            {
                "complexity": "medium",
                "expected_contains": ["고해상도", "상세한"]
            },
            {
                "complexity": "low",
                "expected_contains": ["표준 해상도", "깔끔한"]
            }
        ]
        
        for case in test_cases:
            # 분석 결과에 복잡성 설정
            analysis_result = sample_analysis_result.copy()
            analysis_result["complexity"] = case["complexity"]
            
            technical_text = imagen3_model._generate_technical(analysis_result, sample_intent_result)
            
            # 예상 기술적 명세가 포함되어 있는지 확인
            assert any(expected in technical_text for expected in case["expected_contains"])
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_optimize_prompt_integration(self, imagen3_model, sample_analysis_result, sample_intent_result):
        """프롬프트 최적화 통합 테스트"""
        optimized_prompt = imagen3_model.optimize_prompt(sample_analysis_result, sample_intent_result)
        
        # 최적화된 프롬프트가 생성되었는지 확인
        assert len(optimized_prompt) > 0
        assert isinstance(optimized_prompt, str)
        
        # 원본 입력보다 더 자세한지 확인
        original_input = sample_analysis_result["input_text"]
        assert len(optimized_prompt) > len(original_input)
        
        # 부정적 프롬프트가 포함되어 있는지 확인
        assert "Negative prompt:" in optimized_prompt or "negative" in optimized_prompt.lower()
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_generation_parameters(self, imagen3_model, sample_analysis_result, sample_intent_result):
        """생성 매개변수 테스트"""
        generation_params = imagen3_model.get_generation_parameters(sample_analysis_result, sample_intent_result)
        
        # 필수 매개변수가 포함되어 있는지 확인
        required_params = ["width", "height", "num_inference_steps", "guidance_scale", "quality", "format"]
        for param in required_params:
            assert param in generation_params, f"Required parameter '{param}' is missing"
        
        # 매개변수 값이 합리적인지 확인
        assert generation_params["width"] > 0
        assert generation_params["height"] > 0
        assert generation_params["num_inference_steps"] > 0
        assert generation_params["guidance_scale"] > 0
        assert generation_params["quality"] in ["fast", "standard", "premium", "ultra"]
        assert generation_params["format"] in ["png", "jpg", "webp"]
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_generation_parameters_subject_type_adjustment(self, imagen3_model):
        """주제 유형에 따른 생성 매개변수 조정 테스트"""
        test_cases = [
            {
                "input": "웃는 여성의 초상화",
                "expected_aspect": "3:4"
            },
            {
                "input": "아름다운 산 풍경",
                "expected_aspect": "4:3"
            },
            {
                "input": "스마트폰 제품 사진",
                "expected_aspect": "1:1"
            }
        ]
        
        for case in test_cases:
            analysis_result = {
                "input_text": case["input"],
                "complexity": "medium"
            }
            intent_result = {"primary_intent": ("generate_content", 0.8)}
            
            generation_params = imagen3_model.get_generation_parameters(analysis_result, intent_result)
            
            if "expected_aspect" in case:
                assert "aspect_ratio" in generation_params
                assert generation_params["aspect_ratio"] == case["expected_aspect"]
    
    @pytest.mark.unit
    @pytest.mark.model
    @pytest.mark.parametrize("complexity,expected_quality", [
        ("high", "premium"),
        ("medium", "standard"),
        ("low", "fast")
    ])
    def test_generation_parameters_complexity_adjustment(self, imagen3_model, complexity, expected_quality):
        """복잡성에 따른 생성 매개변수 조정 테스트"""
        analysis_result = {
            "input_text": "테스트 이미지",
            "complexity": complexity
        }
        intent_result = {"primary_intent": ("generate_content", 0.8)}
        
        generation_params = imagen3_model.get_generation_parameters(analysis_result, intent_result)
        
        # 복잡성에 따른 품질 조정 확인
        if complexity == "high":
            assert generation_params["width"] >= 1280
            assert generation_params["height"] >= 1280
            assert generation_params["num_inference_steps"] >= 75
        elif complexity == "low":
            assert generation_params["num_inference_steps"] <= 30
    
    @pytest.mark.unit
    @pytest.mark.model
    def test_error_handling(self, imagen3_model):
        """오류 처리 테스트"""
        # 빈 분석 결과로 테스트
        empty_analysis = {}
        empty_intent = {}
        
        try:
            # 빈 입력에도 기본 프롬프트가 생성되어야 함
            result = imagen3_model.optimize_prompt(empty_analysis, empty_intent)
            assert isinstance(result, str)
        except Exception as e:
            pytest.fail(f"Model should handle empty input gracefully, but got error: {str(e)}")
    
    @pytest.mark.unit
    @pytest.mark.model
    @pytest.mark.benchmark
    def test_optimization_performance(self, imagen3_model, benchmark, sample_analysis_result, sample_intent_result):
        """최적화 성능 테스트"""
        # 성능 벤치마크 실행
        result = benchmark(imagen3_model.optimize_prompt, sample_analysis_result, sample_intent_result)
        
        # 결과가 올바른지 확인
        assert isinstance(result, str)
        assert len(result) > 0 