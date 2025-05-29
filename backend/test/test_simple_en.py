#!/usr/bin/env python3
"""
Simple image model test in English
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Starting simple image model test...")

try:
    from src.services.optimizer import PromptOptimizer
    print("PromptOptimizer import successful")
    
    optimizer = PromptOptimizer()
    print("PromptOptimizer instance created successfully")
    
    # Test Imagen3 model
    test_input = "A cute dog running on a sunny beach"
    model_id = "imagen-3"
    
    print(f"Testing {model_id} model...")
    print(f"Input: {test_input}")
    
    result = optimizer.optimize_prompt(test_input, model_id)
    
    if result.get("success"):
        print("Optimization successful!")
        print(f"Optimized prompt:")
        print(result['optimized_prompt'])
        
        if result.get("generation_params"):
            print(f"Generation parameters:")
            for key, value in result['generation_params'].items():
                print(f"   {key}: {value}")
    else:
        print(f"Optimization failed: {result.get('error')}")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()

print("Test completed!") 