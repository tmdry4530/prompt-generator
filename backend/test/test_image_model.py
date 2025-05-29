#!/usr/bin/env python3
"""
이미지 모델 최적화 테스트 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_image_models():
    """이미지 모델들의 최적화 기능을 테스트합니다."""
    try:
        print("🎨 이미지 모델 최적화 테스트 시작...")
        
        from src.services.optimizer import PromptOptimizer
        optimizer = PromptOptimizer()
        
        # 이미지 모델들만 필터링
        image_models = {
            model_id: model for model_id, model in optimizer.models.items()
            if "image" in model.capabilities or any(cap in ["image_generation", "photorealistic_rendering"] for cap in model.capabilities)
        }
        
        print(f"🖼️ 찾은 이미지 모델 수: {len(image_models)}")
        
        # 다양한 테스트 케이스
        test_cases = [
            {
                "name": "간단한 초상화",
                "input": "웃는 여성의 초상화",
                "description": "기본적인 초상화 요청"
            },
            {
                "name": "복잡한 풍경",
                "input": "일몰 시간에 산 정상에서 바라본 아름다운 계곡, 사진 사실적, 고해상도",
                "description": "상세한 풍경 묘사"
            },
            {
                "name": "제품 사진",
                "input": "고급 스마트폰 제품 사진, 스튜디오 조명, 미니멀한 배경",
                "description": "제품 시각화"
            },
            {
                "name": "텍스트 포함 이미지",
                "input": "'Hello World'라는 텍스트가 중앙에 있는 포스터, 현대적 디자인",
                "description": "텍스트 렌더링 테스트"
            }
        ]
        
        for model_id, model in image_models.items():
            print(f"\n🧪 {model.model_name} ({model_id}) 테스트:")
            print(f"   제공업체: {model.provider}")
            print(f"   지원 기능: {', '.join(model.capabilities)}")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n   테스트 {i}: {test_case['name']}")
                print(f"   입력: {test_case['input']}")
                
                try:
                    result = optimizer.optimize_prompt(test_case['input'], model_id)
                    
                    if result.get("success"):
                        print("   ✅ 최적화 성공!")
                        print(f"   📝 최적화된 프롬프트 (처음 150자):")
                        optimized = result['optimized_prompt']
                        print(f"      {optimized[:150]}{'...' if len(optimized) > 150 else ''}")
                        
                        # 생성 매개변수 표시
                        if result.get("generation_params"):
                            params = result['generation_params']
                            key_params = {k: v for k, v in params.items() if k in ['width', 'height', 'quality', 'guidance_scale']}
                            print(f"   ⚙️ 주요 매개변수: {key_params}")
                        
                    else:
                        print(f"   ❌ 최적화 실패: {result.get('error')}")
                        
                except Exception as e:
                    print(f"   ❌ 오류 발생: {str(e)}")
                    
            # 구분선
            print("   " + "-" * 50)
        
        print("\n🎉 이미지 모델 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_models() 