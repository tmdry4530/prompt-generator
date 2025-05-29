#!/bin/bash

# AI Prompt Optimization Tool - Extended Integration Test Script
# Designed to run in PowerShell environment

set -e  # Exit script on error

# Functions for colored output
print_header() {
    echo "======================================"
    echo "$1"
    echo "======================================"
}

print_success() {
    echo "✅ $1"
}

print_error() {
    echo "❌ $1"
}

print_info() {
    echo "ℹ️  $1"
}

# Test result storage variables
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
START_TIME=$(date +%s)

# Test result recording function
record_test_result() {
    local test_name="$1"
    local result="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$result" = "PASS" ]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        print_success "$test_name"
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        print_error "$test_name - $result"
    fi
}

# Check Python environment
check_python_environment() {
    print_header "Checking Python Environment"
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        record_test_result "Python installation check" "Python not installed"
        return 1
    fi
    
    record_test_result "Python installation check" "PASS"
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
    print_info "Python version: $PYTHON_VERSION"
    
    # Activate virtual environment (Windows PowerShell compatible)
    if [ -d ".venv" ]; then
        if [ -f ".venv/Scripts/activate" ]; then
            # Windows environment
            source .venv/Scripts/activate
        elif [ -f ".venv/bin/activate" ]; then
            # Unix environment
            source .venv/bin/activate
        fi
        record_test_result "Virtual environment activation" "PASS"
    else
        print_info "No virtual environment found - using system Python"
    fi
}

# Check dependencies
check_dependencies() {
    print_header "Checking Dependencies"
    
    # Check requirements.txt
    if [ ! -f "requirements.txt" ]; then
        record_test_result "requirements.txt existence check" "File not found"
        return 1
    fi
    
    record_test_result "requirements.txt existence check" "PASS"
    
    # Check major package installations
    local packages=("pytest" "fastapi" "uvicorn")
    
    for package in "${packages[@]}"; do
        if $PYTHON_CMD -c "import $package" 2>/dev/null; then
            record_test_result "$package package check" "PASS"
        else
            record_test_result "$package package check" "Not installed"
            print_info "Installing $package..."
            $PYTHON_CMD -m pip install $package
        fi
    done
}

# Run unit tests
run_unit_tests() {
    print_header "Running Unit Tests"
    
    # InputAnalyzer test
    if $PYTHON_CMD -m pytest test/test_input_analyzer.py -v --tb=short; then
        record_test_result "InputAnalyzer unit test" "PASS"
    else
        record_test_result "InputAnalyzer unit test" "Failed"
    fi
    
    # Imagen3Model test
    if $PYTHON_CMD -m pytest test/test_imagen3_model.py -v --tb=short; then
        record_test_result "Imagen3Model unit test" "PASS"
    else
        record_test_result "Imagen3Model unit test" "Failed"
    fi
    
    # All unit tests (marker-based)
    if $PYTHON_CMD -m pytest -m "unit" -v --tb=short; then
        record_test_result "All unit tests" "PASS"
    else
        record_test_result "All unit tests" "Failed"
    fi
}

# Run integration tests
run_integration_tests() {
    print_header "Running Integration Tests"
    
    # PromptOptimizer integration test
    if $PYTHON_CMD -m pytest test/test_optimizer.py -v --tb=short; then
        record_test_result "PromptOptimizer integration test" "PASS"
    else
        record_test_result "PromptOptimizer integration test" "Failed"
    fi
    
    # All integration tests (marker-based)
    if $PYTHON_CMD -m pytest -m "integration" -v --tb=short; then
        record_test_result "All integration tests" "PASS"
    else
        record_test_result "All integration tests" "Failed"
    fi
}

# Test API functionality
test_api_functionality() {
    print_header "Testing API Functionality"
    
    # Start server (background)
    print_info "Starting server..."
    $PYTHON_CMD -c "
import sys
sys.path.append('.')
from src.services.optimizer import PromptOptimizer

# Test optimizer initialization
try:
    optimizer = PromptOptimizer()
    models = optimizer.get_available_models()
    print(f'Successfully loaded {len(models)} models')
    exit(0)
except Exception as e:
    print(f'Error: {e}')
    exit(1)
" && record_test_result "Server initialization" "PASS" || record_test_result "Server initialization" "Failed"
    
    # Test optimization for various models
    test_model_optimization "gpt-4o" "Hello. Please write a simple blog post."
    test_model_optimization "imagen-3" "A photo of a dog playing on the beach on a bright sunny day"
    test_model_optimization "suno" "Please create bright and cheerful pop music"
    test_model_optimization "sora" "A short video clip with a city background"
}

# Test individual model optimization
test_model_optimization() {
    local model_id="$1"
    local input_text="$2"
    
    $PYTHON_CMD -c "
import sys
sys.path.append('.')
from src.services.optimizer import PromptOptimizer

try:
    optimizer = PromptOptimizer()
    result = optimizer.optimize_prompt('$input_text', '$model_id')
    
    if result['success']:
        print(f'✅ $model_id optimization successful')
        print(f'   Input: $input_text')
        print(f'   Optimized: {result[\"optimized_prompt\"][:100]}...')
        exit(0)
    else:
        print(f'❌ $model_id optimization failed: {result.get(\"error\", \"Unknown error\")}')
        exit(1)
except Exception as e:
    print(f'❌ Error during $model_id test: {e}')
    exit(1)
" && record_test_result "$model_id model optimization" "PASS" || record_test_result "$model_id model optimization" "Failed"
}

# Test edge cases
test_edge_cases() {
    print_header "Testing Edge Cases"
    
    # Empty input test
    test_edge_case "Empty input" "" "gpt-4o"
    
    # Very long input test
    local long_input=$(printf "Test input %.0s" {1..100})
    test_edge_case "Long input" "$long_input" "gpt-4o"
    
    # Special character input test
    test_edge_case "Special characters" "!@#$%^&*()" "gpt-4o"
    
    # Multi-language input test
    test_edge_case "Multi-language input" "Hello 안녕하세요 こんにちは 你好" "gpt-4o"
    
    # Non-existent model test
    test_edge_case "Invalid model" "Test input" "non-existent-model"
}

# Test individual edge case
test_edge_case() {
    local test_name="$1"
    local input_text="$2"
    local model_id="$3"
    
    $PYTHON_CMD -c "
import sys
sys.path.append('.')
from src.services.optimizer import PromptOptimizer

try:
    optimizer = PromptOptimizer()
    result = optimizer.optimize_prompt('$input_text', '$model_id')
    
    # For edge cases, success or proper error handling is important
    if isinstance(result, dict) and 'success' in result:
        print(f'✅ $test_name handled (success: {result[\"success\"]})')
        exit(0)
    else:
        print(f'❌ $test_name handling failed: unexpected response format')
        exit(1)
except Exception as e:
    print(f'❌ Exception during $test_name test: {e}')
    exit(1)
" && record_test_result "$test_name edge case" "PASS" || record_test_result "$test_name edge case" "Failed"
}

# Run performance tests
run_performance_tests() {
    print_header "Running Performance Tests"
    
    # Response time test
    $PYTHON_CMD -c "
import sys
import time
sys.path.append('.')
from src.services.optimizer import PromptOptimizer

try:
    optimizer = PromptOptimizer()
    
    # Measure average response time for 10 optimization requests
    total_time = 0
    num_requests = 10
    
    for i in range(num_requests):
        start_time = time.time()
        result = optimizer.optimize_prompt('Performance test input', 'gpt-4o')
        end_time = time.time()
        
        if result['success']:
            total_time += (end_time - start_time)
        else:
            print(f'❌ Request {i+1} failed')
            exit(1)
    
    avg_time = total_time / num_requests
    print(f'✅ Average response time: {avg_time:.3f}s ({num_requests} requests)')
    
    if avg_time < 2.0:  # Success if under 2 seconds
        exit(0)
    else:
        print(f'❌ Response time too slow (threshold: 2s)')
        exit(1)
        
except Exception as e:
    print(f'❌ Error during performance test: {e}')
    exit(1)
" && record_test_result "Response time performance" "PASS" || record_test_result "Response time performance" "Failed"
}

# Run code quality checks
run_code_quality_checks() {
    print_header "Running Code Quality Checks"
    
    # pytest coverage test
    if $PYTHON_CMD -m pytest --cov=src --cov-report=term-missing --cov-fail-under=70 -q; then
        record_test_result "Code coverage (70% or higher)" "PASS"
    else
        record_test_result "Code coverage (70% or higher)" "Below threshold"
    fi
    
    # flake8 code style check (optional)
    if command -v flake8 &> /dev/null; then
        if flake8 src/ --max-line-length=120 --ignore=E203,W503; then
            record_test_result "Code style check (flake8)" "PASS"
        else
            record_test_result "Code style check (flake8)" "Violations found"
        fi
    else
        print_info "flake8 not installed - skipping style check"
    fi
}

# Generate test report
generate_test_report() {
    print_header "Test Results Summary"
    
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    
    echo "Total tests: $TOTAL_TESTS"
    echo "Passed: $PASSED_TESTS"
    echo "Failed: $FAILED_TESTS"
    echo "Success rate: $(( (PASSED_TESTS * 100) / TOTAL_TESTS ))%"
    echo "Execution time: ${duration}s"
    
    # Generate HTML report (optional)
    if [ -d "htmlcov" ]; then
        print_info "Code coverage report: htmlcov/index.html"
    fi
    
    # Save test results to file
    cat > test_report.txt << EOF
AI Prompt Optimization Tool - Integration Test Report
===================================================

Execution time: $(date)
Total tests: $TOTAL_TESTS
Passed: $PASSED_TESTS
Failed: $FAILED_TESTS
Success rate: $(( (PASSED_TESTS * 100) / TOTAL_TESTS ))%
Execution time: ${duration}s

See pytest output for detailed results.
EOF
    
    print_info "Test report saved: test_report.txt"
}

# Main execution function
main() {
    print_header "AI Prompt Optimization Tool - Extended Integration Test"
    print_info "Start time: $(date)"
    
    # Check current directory
    if [ ! -f "src/services/optimizer.py" ]; then
        print_error "Please run from backend directory"
        exit 1
    fi
    
    # Run tests
    check_python_environment
    check_dependencies
    run_unit_tests
    run_integration_tests
    test_api_functionality
    test_edge_cases
    run_performance_tests
    run_code_quality_checks
    
    # Generate report
    generate_test_report
    
    # Final result
    if [ $FAILED_TESTS -eq 0 ]; then
        print_success "All tests passed successfully! 🎉"
        exit 0
    else
        print_error "$FAILED_TESTS test(s) failed."
        exit 1
    fi
}

# Execute script
main "$@" 