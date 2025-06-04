"""
Model Optimization Prompt Generator - Quick Test
Fast functionality test script
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from model_optimizer import ModelOptimizationPromptGenerator
from template_library import PromptTemplateLibrary
import json

def test_model_optimizer():
    """Test prompt optimization engine"""
    print("🧪 [Test] Model Optimizer test starting...")
    
    generator = ModelOptimizationPromptGenerator()
    
    # Check supported models
    models = generator.get_supported_models()
    print(f"✅ Supported models: {models}")
    
    # Test each model
    test_task = "Write Python code to read and analyze data from a CSV file"
    
    for model in models:
        print(f"\n🔧 [{model}] Testing...")
        
        result = generator.generate_optimized_prompt(test_task, model)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            continue
            
        print(f"✅ Success!")
        print(f"   - Original: {result['original_task'][:50]}...")
        print(f"   - Structure: {result['prompt_structure']}")
        print(f"   - Max tokens: {result['max_tokens']:,}")
        print(f"   - Optimization tips: {len(result['optimization_tips'])}")

def test_template_library():
    """Test template library"""
    print("\n🧪 [Test] Template Library test starting...")
    
    library = PromptTemplateLibrary()
    
    # Check categories
    categories = library.get_all_categories()
    print(f"✅ Template categories: {categories}")
    
    # Test each category for different models
    test_variables = {
        'code_generation': {
            'language': 'Python',
            'task': 'CSV file processing function'
        },
        'analysis': {
            'subject': 'Sales data',
            'content': 'Excel file containing monthly sales'
        },
        'writing': {
            'type': 'Technical blog',
            'topic': 'Machine learning introduction',
            'purpose': 'Beginner education',
            'audience': 'Developers',
            'length': '2000 words',
            'tone': 'Friendly and simple'
        },
        'summarization': {
            'content': 'Long research paper content. Covers the latest trends in machine learning and technical advancements.',
            'format': 'Bullet points',
            'length': '300 words'
        }
    }
    
    models = ['gpt-4', 'claude-3']
    
    for category in categories[:4]:  # Test only first 4 categories
        if category not in test_variables:
            continue
            
        print(f"\n📝 [{category}] Category test...")
        
        for model in models:
            template_data = library.get_template(category, model)
            if not template_data:
                print(f"   ❌ {model}: No template")
                continue
            
            variables = test_variables[category]
            result = library.apply_template(category, model, variables)
            
            if result.startswith('Category') or result.startswith('Required variables'):
                print(f"   ❌ {model}: {result}")
            else:
                print(f"   ✅ {model}: Template applied successfully ({len(result)} chars)")

def test_examples():
    """Test example tasks"""
    print("\n🧪 [Test] Example Tasks test starting...")
    
    library = PromptTemplateLibrary()
    models = ['gpt-4', 'claude-3', 'llama-2', 'gemini-pro']
    
    for model in models:
        examples = library.get_example_tasks(model)
        print(f"✅ {model}: {len(examples)} examples")
        
        if examples:
            print(f"   - First example: {examples[0]}")

def test_integration():
    """Integration test"""
    print("\n🧪 [Test] Integration test starting...")
    
    generator = ModelOptimizationPromptGenerator()
    library = PromptTemplateLibrary()
    
    # Test actual workflow
    model = 'gpt-4'
    examples = library.get_example_tasks(model)
    
    if examples:
        task = examples[0]  # Use first example
        print(f"📝 Test task: {task}")
        
        # Basic optimization
        result = generator.generate_optimized_prompt(task, model)
        
        if 'error' not in result:
            print("✅ Integration test successful!")
            print(f"   - Optimized prompt length: {len(result['optimized_prompt'])} chars")
            print(f"   - Generated at: {result['generated_at']}")
        else:
            print(f"❌ Integration test failed: {result['error']}")

def main():
    """Main test execution"""
    print("=" * 60)
    print("🚀 Model Optimization Prompt Generator - Quick Test")
    print("=" * 60)
    
    try:
        test_model_optimizer()
        test_template_library()
        test_examples()
        test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed!")
        print("✅ Ready to start the server.")
        print("💡 Run method: .\\start_server.ps1")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during tests: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 