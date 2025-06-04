#!/usr/bin/env python3
"""
Simple test script to verify basic functionality
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_input_analyzer():
    """Test InputAnalyzer basic functionality"""
    try:
        from src.utils.input_analyzer import InputAnalyzer
        print("[SUCCESS] InputAnalyzer imported successfully")
        
        analyzer = InputAnalyzer()
        print("[SUCCESS] InputAnalyzer instance created")
        
        # Test basic analysis
        result = analyzer.analyze("Hello world", "gpt-4o")
        print("[SUCCESS] Basic analysis completed")
        print(f"Result keys: {list(result.keys())}")
        
        # Check required keys
        required_keys = ["input_text", "selected_model", "keywords", "task_type"]
        missing_keys = [key for key in required_keys if key not in result]
        
        if missing_keys:
            print(f"[ERROR] Missing required keys: {missing_keys}")
            return False
        else:
            print("[SUCCESS] All required keys present")
            return True
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_optimizer():
    """Test PromptOptimizer basic functionality"""
    try:
        from src.services.optimizer import PromptOptimizer
        print("[SUCCESS] PromptOptimizer imported successfully")
        
        optimizer = PromptOptimizer()
        print("[SUCCESS] PromptOptimizer instance created")
        
        # Get available models
        models = optimizer.get_available_models()
        print(f"[SUCCESS] Available models: {len(models)}")
        
        if len(models) > 0:
            print(f"First model: {models[0]['model_id']}")
            return True
        else:
            print("[ERROR] No models available")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Simple Backend Test ===")
    
    success_count = 0
    total_tests = 2
    
    print("\n1. Testing InputAnalyzer...")
    if test_input_analyzer():
        success_count += 1
    
    print("\n2. Testing PromptOptimizer...")
    if test_optimizer():
        success_count += 1
    
    print(f"\n=== Results ===")
    print(f"Passed: {success_count}/{total_tests}")
    print(f"Success rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("[SUCCESS] All tests passed!")
        sys.exit(0)
    else:
        print("[ERROR] Some tests failed")
        sys.exit(1) 