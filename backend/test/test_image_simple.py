#!/usr/bin/env python3
"""
간단한 이미지 모델 테스트
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🎨 간단한 이미지 모델 테스트 시작...")

try:
    from src.services.optimizer import PromptOptimizer
    print("✅ PromptOptimizer import 성공")
    
    optimizer = PromptOptimizer()
    print("✅ PromptOptimizer 인스턴스 생성 성공")
    
    # Imagen3 모델 테스트
    test_input = "밝고 화창한 날에 해변에서 뛰노는 강아지의 사진"
    model_id = "imagen-3"
    
    print(f"🧪 {model_id} 모델로 테스트...")
    print(f"📝 입력: {test_input}")
    
    result = optimizer.optimize_prompt(test_input, model_id)
    
    if result.get("success"):
        print("✅ 최적화 성공!")
        print(f"⚡ 최적화된 프롬프트:")
        print(result['optimized_prompt'])
        
        if result.get("generation_params"):
            print(f"⚙️ 생성 매개변수:")
            for key, value in result['generation_params'].items():
                print(f"   {key}: {value}")
    else:
        print(f"❌ 최적화 실패: {result.get('error')}")

except Exception as e:
    print(f"❌ 오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()

print("🎉 테스트 완료!") 