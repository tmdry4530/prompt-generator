#!/usr/bin/env python3
"""
Optimizer 시스템 테스트 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_optimizer():
    """Optimizer 시스템을 테스트합니다."""
    try:
        print("🔧 Optimizer 시스템 테스트 시작...")
        
        # 1. 기본 import 테스트
        from src.services.optimizer import PromptOptimizer
        print("✅ PromptOptimizer import 성공")
        
        # 2. 인스턴스 생성 테스트
        optimizer = PromptOptimizer()
        print("✅ PromptOptimizer 인스턴스 생성 성공")
        
        # 3. 모델 로드 확인
        print(f"📊 로드된 모델 수: {len(optimizer.models)}")
        print("📝 사용 가능한 모델:")
        for model_id in sorted(optimizer.models.keys()):
            model = optimizer.models[model_id]
            print(f"  - {model_id}: {model.model_name} (제공업체: {model.provider})")
        
        # 4. 모델별 기능 테스트
        if optimizer.models:
            test_model_id = list(optimizer.models.keys())[0]
            print(f"\n🧪 '{test_model_id}' 모델로 최적화 테스트...")
            
            test_input = "밝고 화창한 날에 해변에서 뛰노는 강아지의 사진을 생성해주세요"
            result = optimizer.optimize_prompt(test_input, test_model_id)
            
            if result.get("success"):
                print("✅ 프롬프트 최적화 성공!")
                print(f"📝 원본 입력: {result['original_input']}")
                print(f"⚡ 최적화된 프롬프트: {result['optimized_prompt'][:200]}...")
                
                if result.get("generation_params"):
                    print(f"⚙️ 생성 매개변수: {list(result['generation_params'].keys())}")
            else:
                print(f"❌ 프롬프트 최적화 실패: {result.get('error')}")
        
        print("\n🎉 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_optimizer()

"""
PromptOptimizer 클래스 통합 테스트
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List
from src.services.optimizer import PromptOptimizer


class TestPromptOptimizer:
    """PromptOptimizer 클래스 테스트"""
    
    @pytest.fixture
    def optimizer(self):
        """PromptOptimizer 인스턴스를 반환합니다."""
        return PromptOptimizer()
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_optimizer_initialization(self, optimizer):
        """Optimizer 초기화 테스트"""
        assert optimizer is not None
        assert hasattr(optimizer, 'input_analyzer')
        assert hasattr(optimizer, 'models')
        
        # 모델이 로드되었는지 확인
        assert len(optimizer.models) > 0
        
        # 각 모델이 올바른 구조를 가지는지 확인
        for model_id, model in optimizer.models.items():
            assert hasattr(model, 'model_id')
            assert hasattr(model, 'model_name')
            assert hasattr(model, 'provider')
            assert hasattr(model, 'capabilities')
            assert hasattr(model, 'optimize_prompt')
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_get_available_models(self, optimizer):
        """사용 가능한 모델 목록 조회 테스트"""
        models = optimizer.get_available_models()
        
        # 모델 목록이 비어있지 않은지 확인
        assert len(models) > 0
        
        # 각 모델 정보가 올바른 구조를 가지는지 확인
        for model_info in models:
            required_keys = ["model_id", "model_name", "provider", "capabilities", "supports_multimodal"]
            for key in required_keys:
                assert key in model_info, f"Required key '{key}' is missing from model info"
            
            assert isinstance(model_info["capabilities"], list)
            assert isinstance(model_info["supports_multimodal"], bool)
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    @pytest.mark.parametrize("model_id,input_text", [
        ("gpt-4o", "안녕하세요. 간단한 블로그 포스트를 작성해주세요."),
        ("imagen-3", "밝고 화창한 날에 해변에서 뛰노는 강아지의 사진"),
        ("suno", "밝고 경쾌한 팝 음악을 만들어주세요"),
        ("sora", "도시를 배경으로 한 짧은 비디오 클립")
    ])
    def test_optimize_prompt_success(self, optimizer, model_id, input_text):
        """프롬프트 최적화 성공 케이스 테스트"""
        result = optimizer.optimize_prompt(input_text, model_id)
        
        # 성공적인 결과인지 확인
        assert result["success"] is True
        assert "optimized_prompt" in result
        assert "model_info" in result
        assert "prompt_structure" in result
        
        # 입력과 모델 ID가 올바르게 설정되었는지 확인
        assert result["original_input"] == input_text
        assert result["model_id"] == model_id
        
        # 최적화된 프롬프트가 비어있지 않은지 확인
        assert len(result["optimized_prompt"]) > 0
        assert result["optimized_prompt"] != input_text  # 최적화가 실제로 일어났는지 확인
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_optimize_prompt_with_additional_params(self, optimizer):
        """추가 매개변수를 포함한 프롬프트 최적화 테스트"""
        input_text = "복잡한 기술 문서를 작성해주세요"
        model_id = "gpt-4o"
        additional_params = {
            "complexity": "high",
            "style": [("technical", 0.9)],
            "constraints": {"tone": "professional", "audience": "expert"}
        }
        
        result = optimizer.optimize_prompt(input_text, model_id, additional_params)
        
        assert result["success"] is True
        
        # 추가 매개변수가 분석 결과에 포함되었는지 확인
        analysis_result = result["analysis_result"]
        assert analysis_result["complexity"] == "high"
        assert analysis_result["style"] == [("technical", 0.9)]
        assert analysis_result["constraints"]["tone"] == "professional"
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_optimize_prompt_invalid_model(self, optimizer):
        """존재하지 않는 모델로 최적화 요청 테스트"""
        input_text = "테스트 입력"
        invalid_model_id = "non-existent-model"
        
        result = optimizer.optimize_prompt(input_text, invalid_model_id)
        
        # 실패 결과인지 확인
        assert result["success"] is False
        assert "error" in result
        assert "available_models" in result
        assert invalid_model_id not in result["available_models"]
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_get_model_specific_tips(self, optimizer):
        """모델별 최적화 팁 조회 테스트"""
        # 사용 가능한 모델 중 하나를 선택
        available_models = list(optimizer.models.keys())
        test_model_id = available_models[0]
        
        tips = optimizer.get_model_specific_tips(test_model_id)
        
        # 팁이 반환되었는지 확인
        assert isinstance(tips, list)
        assert len(tips) > 0
        
        # 팁이 문자열인지 확인
        for tip in tips:
            assert isinstance(tip, str)
            assert len(tip) > 0
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_get_model_prompt_structure(self, optimizer):
        """모델 프롬프트 구조 조회 테스트"""
        # 사용 가능한 모델 중 하나를 선택
        available_models = list(optimizer.models.keys())
        test_model_id = available_models[0]
        
        structure = optimizer.get_model_prompt_structure(test_model_id)
        
        # 구조 정보가 올바른지 확인
        assert isinstance(structure, dict)
        assert "components" in structure
        assert "recommended_order" in structure
        
        # 컴포넌트가 리스트인지 확인
        assert isinstance(structure["components"], list)
        assert isinstance(structure["recommended_order"], list)
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_get_model_info(self, optimizer):
        """모델 정보 조회 테스트"""
        # 사용 가능한 모델 중 하나를 선택
        available_models = list(optimizer.models.keys())
        test_model_id = available_models[0]
        
        model_info = optimizer.get_model_info(test_model_id)
        
        # 모델 정보가 올바른지 확인
        assert isinstance(model_info, dict)
        required_keys = ["model_id", "model_name", "provider", "capabilities", "supports_multimodal"]
        for key in required_keys:
            assert key in model_info, f"Required key '{key}' is missing from model info"
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_compare_models(self, optimizer):
        """모델 비교 기능 테스트"""
        # 사용 가능한 모델 중 일부를 선택
        available_models = list(optimizer.models.keys())
        test_model_ids = available_models[:min(3, len(available_models))]
        
        comparison = optimizer.compare_models(test_model_ids)
        
        # 비교 결과가 올바른지 확인
        assert isinstance(comparison, dict)
        assert "models" in comparison
        assert "capabilities" in comparison
        assert "providers" in comparison
        assert "multimodal_support" in comparison
        
        # 요청한 모델 수만큼 정보가 있는지 확인
        assert len(comparison["models"]) == len(test_model_ids)
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    @pytest.mark.parametrize("edge_case", [
        {"name": "빈 입력", "input": "", "model_id": "gpt-4o"},
        {"name": "매우 긴 입력", "input": "테스트 " * 1000, "model_id": "gpt-4o"},
        {"name": "특수 문자", "input": "!@#$%^&*()", "model_id": "gpt-4o"},
        {"name": "다국어", "input": "Hello 안녕하세요 こんにちは", "model_id": "gpt-4o"}
    ])
    def test_edge_cases(self, optimizer, edge_case):
        """엣지 케이스 테스트"""
        try:
            result = optimizer.optimize_prompt(edge_case["input"], edge_case["model_id"])
            
            # 결과가 반환되었는지 확인
            assert isinstance(result, dict)
            assert "success" in result
            
            # 빈 입력이 아닌 경우 성공해야 함
            if edge_case["input"].strip():
                assert result["success"] is True
                assert "optimized_prompt" in result
            
        except Exception as e:
            pytest.fail(f"Edge case '{edge_case['name']}' failed with error: {str(e)}")
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    @pytest.mark.slow
    def test_performance_multiple_requests(self, optimizer):
        """다중 요청 성능 테스트"""
        import time
        
        input_text = "성능 테스트를 위한 입력 텍스트"
        model_id = "gpt-4o"
        num_requests = 10
        
        start_time = time.time()
        
        results = []
        for _ in range(num_requests):
            result = optimizer.optimize_prompt(input_text, model_id)
            results.append(result)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / num_requests
        
        # 모든 요청이 성공했는지 확인
        assert all(result["success"] for result in results)
        
        # 평균 응답 시간이 합리적인지 확인 (2초 이하)
        assert avg_time < 2.0, f"Average response time too high: {avg_time:.2f}s"
        
        print(f"Average response time: {avg_time:.3f}s for {num_requests} requests")
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_model_specific_generation_parameters(self, optimizer):
        """모델별 생성 매개변수 테스트"""
        test_cases = [
            {
                "model_id": "imagen-3",
                "input": "고품질 초상화 사진",
                "expected_params": ["width", "height", "quality"]
            },
            {
                "model_id": "sora",
                "input": "짧은 동영상 클립",
                "expected_params": ["duration", "resolution", "fps"]
            },
            {
                "model_id": "suno",
                "input": "팝 음악",
                "expected_params": ["duration", "tempo", "quality"]
            }
        ]
        
        for case in test_cases:
            if case["model_id"] in optimizer.models:
                result = optimizer.optimize_prompt(case["input"], case["model_id"])
                
                if result["success"] and "generation_params" in result:
                    gen_params = result["generation_params"]
                    
                    # 예상 매개변수가 포함되어 있는지 확인
                    for param in case["expected_params"]:
                        assert param in gen_params, f"Expected parameter '{param}' not found in generation params"
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_cross_model_consistency(self, optimizer):
        """모델 간 일관성 테스트"""
        input_text = "창의적인 콘텐츠를 생성해주세요"
        
        results = {}
        for model_id in optimizer.models.keys():
            result = optimizer.optimize_prompt(input_text, model_id)
            results[model_id] = result
        
        # 모든 모델이 성공적으로 처리했는지 확인
        for model_id, result in results.items():
            assert result["success"] is True, f"Model {model_id} failed to process input"
            assert "optimized_prompt" in result
            assert result["original_input"] == input_text
            assert result["model_id"] == model_id
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    def test_error_handling_and_recovery(self, optimizer):
        """오류 처리 및 복구 테스트"""
        # 모의 객체를 사용하여 분석기에서 오류 발생 시뮬레이션
        with patch.object(optimizer.input_analyzer, 'analyze') as mock_analyze:
            mock_analyze.side_effect = Exception("Simulated analysis error")
            
            result = optimizer.optimize_prompt("테스트 입력", "gpt-4o")
            
            # 오류가 적절히 처리되었는지 확인
            assert result["success"] is False
            assert "error" in result
            assert "Simulated analysis error" in result["error"]
    
    @pytest.mark.integration
    @pytest.mark.optimizer
    @pytest.mark.benchmark
    def test_optimization_benchmark(self, optimizer, benchmark):
        """최적화 성능 벤치마크"""
        input_text = "중간 크기의 텍스트 입력으로 성능을 측정합니다. " * 20
        model_id = "gpt-4o"
        
        # 성능 벤치마크 실행
        result = benchmark(optimizer.optimize_prompt, input_text, model_id)
        
        # 결과가 올바른지 확인
        assert result["success"] is True
        assert "optimized_prompt" in result


class TestPromptOptimizerMocked:
    """모의 객체를 사용한 PromptOptimizer 테스트"""
    
    @pytest.fixture
    def mock_optimizer(self, mock_input_analyzer, mock_base_model):
        """모의 객체를 사용한 PromptOptimizer를 반환합니다."""
        with patch('src.services.optimizer.InputAnalyzer', return_value=mock_input_analyzer):
            optimizer = PromptOptimizer()
            # 모의 모델 추가
            optimizer.models = {"test-model": mock_base_model}
            return optimizer
    
    @pytest.mark.unit
    @pytest.mark.optimizer
    def test_optimize_prompt_with_mocks(self, mock_optimizer, mock_input_analyzer, mock_base_model):
        """모의 객체를 사용한 프롬프트 최적화 테스트"""
        input_text = "테스트 입력"
        model_id = "test-model"
        
        result = mock_optimizer.optimize_prompt(input_text, model_id)
        
        # 모의 객체 메서드가 호출되었는지 확인
        mock_input_analyzer.analyze.assert_called_once_with(input_text, model_id)
        mock_base_model.optimize_prompt.assert_called_once()
        
        # 결과가 올바른지 확인
        assert result["success"] is True
        assert result["optimized_prompt"] == "최적화된 테스트 프롬프트"
    
    @pytest.mark.unit
    @pytest.mark.optimizer
    def test_get_available_models_with_mocks(self, mock_optimizer):
        """모의 객체를 사용한 모델 목록 조회 테스트"""
        models = mock_optimizer.get_available_models()
        
        assert len(models) == 1
        assert models[0]["model_id"] == "test-model"
        assert models[0]["model_name"] == "Test Model"
    
    @pytest.mark.unit
    @pytest.mark.optimizer
    def test_error_handling_with_mocks(self, mock_optimizer, mock_input_analyzer):
        """모의 객체를 사용한 오류 처리 테스트"""
        # 분석기에서 오류 발생 시뮬레이션
        mock_input_analyzer.analyze.side_effect = Exception("Mock error")
        
        result = mock_optimizer.optimize_prompt("테스트", "test-model")
        
        assert result["success"] is False
        assert "Mock error" in result["error"] 