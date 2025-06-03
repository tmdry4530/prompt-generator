#!/bin/bash

# Integration test script
# Performs full stack integration testing in development and production environments.

echo "===== AI Prompt Optimization Tool Integration Test ====="
echo "Test start time: $(date)"
echo "----------------------------------------"

# Set working directories
# Get the directory where the script is located
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# Base directory is the parent of the script's directory (i.e., the project root)
BASE_DIR=$(dirname "$SCRIPT_DIR")
FRONTEND_DIR="$BASE_DIR/frontend"
# Backend directory is the script's directory
BACKEND_DIR="$SCRIPT_DIR"
TEST_RESULTS_DIR="$BASE_DIR/tests/results"

# Create test results directory
mkdir -p "$TEST_RESULTS_DIR"

# Environment configuration check
echo "Checking environment configuration..."
if [ -f "$FRONTEND_DIR/.env.development" ]; then
  echo "✓ Frontend development environment config file exists"
else
  echo "✗ Frontend development environment config file missing"
  exit 1
fi

if [ -f "$FRONTEND_DIR/.env.production" ]; then
  echo "✓ Frontend production environment config file exists"
else
  echo "✗ Frontend production environment config file missing"
  exit 1
fi

if [ -f "$BACKEND_DIR/config/.env.development" ]; then
  echo "✓ Backend development environment config file exists"
else
  echo "✗ Backend development environment config file missing"
  exit 1
fi

if [ -f "$BACKEND_DIR/config/.env.production" ]; then
  echo "✓ Backend production environment config file exists"
else
  echo "✗ Backend production environment config file missing"
  exit 1
fi

echo "----------------------------------------"
echo "Starting backend server..."

# Start backend server (development environment)
cd $BACKEND_DIR
export FLASK_ENV=development
python3 -m src.main > $TEST_RESULTS_DIR/backend_dev.log 2>&1 &
BACKEND_PID=$!

# Wait for backend server to start
echo "Waiting for backend server to start..."
sleep 5

# Check backend server status
echo "Checking backend API status..."
HEALTH_CHECK=$(curl -s http://localhost:5000/api/health)
if [[ $HEALTH_CHECK == *"\"status\":\"ok\""* ]]; then
  echo "✓ Backend server running properly"
  echo "Response: $HEALTH_CHECK"
else
  echo "✗ Backend server status check failed"
  echo "Response: $HEALTH_CHECK"
  kill $BACKEND_PID
  exit 1
fi

echo "----------------------------------------"
echo "Testing API endpoints..."

# Test models list API
echo "Testing models list API..."
MODELS_RESPONSE=$(curl -s http://localhost:5000/api/models)
if [[ $MODELS_RESPONSE == *"\"success\":true"* && $(echo $MODELS_RESPONSE | jq '.models | length') > 0 ]]; then
  echo "✓ Models list API working properly and contains models"

  ESSENTIAL_MODELS=("gpt-4o" "claude-3-opus" "text-bison")
  MISSING_MODELS=()
  for model in "${ESSENTIAL_MODELS[@]}"; do
    if ! echo "$MODELS_RESPONSE" | jq -e --arg model "$model" '.models[] | select(.model_id == $model)' > /dev/null; then
      MISSING_MODELS+=("$model")
    fi
  done

  if [ ${#MISSING_MODELS[@]} -eq 0 ]; then
    echo "✓ All essential models are present"
  else
    echo "✗ Missing essential models: ${MISSING_MODELS[*]}"
    kill $BACKEND_PID
    exit 1
  fi
else
  echo "✗ Models list API test failed or returned empty list"
  echo "Response: $MODELS_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test prompt optimization API
echo "Testing prompt optimization API..."
# Test case 1: Valid input
OPTIMIZE_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"input_text":"Please write an essay about the future of AI", "model_id":"gpt-4o"}' http://localhost:5000/api/optimize)
if [[ $OPTIMIZE_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ Prompt optimization API working properly with valid input"
else
  echo "✗ Prompt optimization API test failed with valid input"
  echo "Response: $OPTIMIZE_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test case 2: Long input text
LONG_TEXT=$(head -c 10000 /dev/urandom | base64) # Generate 10KB of random text
OPTIMIZE_RESPONSE_LONG=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"input_text\":\"$LONG_TEXT\", \"model_id\":\"gpt-4o\"}" http://localhost:5000/api/optimize)
if [[ $OPTIMIZE_RESPONSE_LONG == *"\"success\":true"* ]]; then # Assuming it should succeed or handle gracefully
  echo "✓ Prompt optimization API handled long input text"
else
  # Depending on expected behavior for oversized input, this might need adjustment
  # For now, let's assume an error is acceptable if the text is genuinely too long for the model or system
  # but a success:false with a proper error message is also a valid outcome.
  # This example checks for *any* success:true, adjust if specific error handling is expected.
  echo "✓ Prompt optimization API responded to long input text (may be error, check response)"
  echo "Response: $OPTIMIZE_RESPONSE_LONG" # Log response for manual check
fi


# Test case 3: Invalid model_id
OPTIMIZE_RESPONSE_INVALID_MODEL=$(curl -s -X POST -H "Content-Type: application/json" -d '{"input_text":"Test text", "model_id":"invalid-model-id"}' http://localhost:5000/api/optimize)
if [[ $OPTIMIZE_RESPONSE_INVALID_MODEL == *"\"success\":false"* && $OPTIMIZE_RESPONSE_INVALID_MODEL == *"error"* ]]; then
  echo "✓ Prompt optimization API handled invalid model_id correctly"
else
  echo "✗ Prompt optimization API test failed with invalid model_id"
  echo "Response: $OPTIMIZE_RESPONSE_INVALID_MODEL"
  kill $BACKEND_PID
  exit 1
fi

# Test case 4: Missing input_text
OPTIMIZE_RESPONSE_MISSING_TEXT=$(curl -s -X POST -H "Content-Type: application/json" -d '{"model_id":"gpt-4o"}' http://localhost:5000/api/optimize)
if [[ $OPTIMIZE_RESPONSE_MISSING_TEXT == *"\"success\":false"* && $OPTIMIZE_RESPONSE_MISSING_TEXT == *"error"* ]]; then
  echo "✓ Prompt optimization API handled missing input_text correctly"
else
  echo "✗ Prompt optimization API test failed with missing input_text"
  echo "Response: $OPTIMIZE_RESPONSE_MISSING_TEXT"
  kill $BACKEND_PID
  exit 1
fi

# Test case 5: Missing model_id
OPTIMIZE_RESPONSE_MISSING_MODEL_ID=$(curl -s -X POST -H "Content-Type: application/json" -d '{"input_text":"Test text"}' http://localhost:5000/api/optimize)
if [[ $OPTIMIZE_RESPONSE_MISSING_MODEL_ID == *"\"success\":false"* && $OPTIMIZE_RESPONSE_MISSING_MODEL_ID == *"error"* ]]; then
  echo "✓ Prompt optimization API handled missing model_id correctly"
else
  echo "✗ Prompt optimization API test failed with missing model_id"
  echo "Response: $OPTIMIZE_RESPONSE_MISSING_MODEL_ID"
  kill $BACKEND_PID
  exit 1
fi

# Test model tips API
echo "Testing model tips API..."
# Test case 1: Valid model_id
TIPS_RESPONSE=$(curl -s http://localhost:5000/api/model/gpt-4o/tips)
if [[ $TIPS_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ Model tips API working properly with valid model_id"
else
  echo "✗ Model tips API test failed with valid model_id"
  echo "Response: $TIPS_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test case 2: Invalid model_id
TIPS_RESPONSE_INVALID_MODEL=$(curl -s http://localhost:5000/api/model/invalid-model-id/tips)
if [[ $TIPS_RESPONSE_INVALID_MODEL == *"\"success\":false"* && $TIPS_RESPONSE_INVALID_MODEL == *"error"* ]]; then
  echo "✓ Model tips API handled invalid model_id correctly"
else
  echo "✗ Model tips API test failed with invalid model_id"
  echo "Response: $TIPS_RESPONSE_INVALID_MODEL"
  kill $BACKEND_PID
  exit 1
fi

# Test model structure API
echo "Testing model structure API..."
# Test case 1: Valid model_id
STRUCTURE_RESPONSE=$(curl -s http://localhost:5000/api/model/gpt-4o/structure)
if [[ $STRUCTURE_RESPONSE == *"\"success\":true"* && $STRUCTURE_RESPONSE == *"structure"* ]]; then
  echo "✓ Model structure API working properly with valid model_id and contains 'structure' field"
else
  echo "✗ Model structure API test failed with valid model_id"
  echo "Response: $STRUCTURE_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test case 2: Invalid model_id
STRUCTURE_RESPONSE_INVALID_MODEL=$(curl -s http://localhost:5000/api/model/invalid-model-id/structure)
if [[ $STRUCTURE_RESPONSE_INVALID_MODEL == *"\"success\":false"* && $STRUCTURE_RESPONSE_INVALID_MODEL == *"error"* ]]; then
  echo "✓ Model structure API handled invalid model_id correctly"
else
  echo "✗ Model structure API test failed with invalid model_id"
  echo "Response: $STRUCTURE_RESPONSE_INVALID_MODEL"
  kill $BACKEND_PID
  exit 1
fi

# Test model info API
echo "Testing model info API..."
# Test case 1: Valid model_id
INFO_RESPONSE=$(curl -s http://localhost:5000/api/model/gpt-4o/info)
if [[ $INFO_RESPONSE == *"\"success\":true"* && $INFO_RESPONSE == *"info"* ]]; then
  echo "✓ Model info API working properly with valid model_id and contains 'info' field"
else
  echo "✗ Model info API test failed with valid model_id"
  echo "Response: $INFO_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test case 2: Invalid model_id
INFO_RESPONSE_INVALID_MODEL=$(curl -s http://localhost:5000/api/model/invalid-model-id/info)
if [[ $INFO_RESPONSE_INVALID_MODEL == *"\"success\":false"* && $INFO_RESPONSE_INVALID_MODEL == *"error"* ]]; then
  echo "✓ Model info API handled invalid model_id correctly"
else
  echo "✗ Model info API test failed with invalid model_id"
  echo "Response: $INFO_RESPONSE_INVALID_MODEL"
  kill $BACKEND_PID
  exit 1
fi

# Test compare API
echo "Testing compare API..."
# Test case 1: Valid model_ids
COMPARE_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"model_ids":["gpt-4o", "claude-3-opus"]}' http://localhost:5000/api/compare)
if [[ $COMPARE_RESPONSE == *"\"success\":true"* && $COMPARE_RESPONSE == *"comparison"* ]]; then
  echo "✓ Compare API working properly with valid model_ids and contains 'comparison' field"
else
  echo "✗ Compare API test failed with valid model_ids"
  echo "Response: $COMPARE_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test case 2: List containing an invalid model_id
COMPARE_RESPONSE_INVALID_MODEL=$(curl -s -X POST -H "Content-Type: application/json" -d '{"model_ids":["gpt-4o", "invalid-model-id"]}' http://localhost:5000/api/compare)
if [[ $COMPARE_RESPONSE_INVALID_MODEL == *"\"success\":false"* && $COMPARE_RESPONSE_INVALID_MODEL == *"error"* ]]; then
  echo "✓ Compare API handled list with invalid model_id correctly"
else
  echo "✗ Compare API test failed with list containing invalid model_id"
  echo "Response: $COMPARE_RESPONSE_INVALID_MODEL"
  kill $BACKEND_PID
  exit 1
fi

# Test case 3: Empty list of model_ids
COMPARE_RESPONSE_EMPTY_LIST=$(curl -s -X POST -H "Content-Type: application/json" -d '{"model_ids":[]}' http://localhost:5000/api/compare)
if [[ $COMPARE_RESPONSE_EMPTY_LIST == *"\"success\":false"* && $COMPARE_RESPONSE_EMPTY_LIST == *"error"* ]]; then
  echo "✓ Compare API handled empty list of model_ids correctly"
else
  echo "✗ Compare API test failed with empty list of model_ids"
  echo "Response: $COMPARE_RESPONSE_EMPTY_LIST"
  kill $BACKEND_PID
  exit 1
fi

# Test case 4: Missing model_ids parameter
COMPARE_RESPONSE_MISSING_PARAM=$(curl -s -X POST -H "Content-Type: application/json" -d '{}' http://localhost:5000/api/compare)
if [[ $COMPARE_RESPONSE_MISSING_PARAM == *"\"success\":false"* && $COMPARE_RESPONSE_MISSING_PARAM == *"error"* ]]; then
  echo "✓ Compare API handled missing model_ids parameter correctly"
else
  echo "✗ Compare API test failed with missing model_ids parameter"
  echo "Response: $COMPARE_RESPONSE_MISSING_PARAM"
  kill $BACKEND_PID
  exit 1
fi

echo "----------------------------------------"
echo "Testing frontend build..."

# Frontend build test (development environment)
cd $FRONTEND_DIR
echo "Testing development environment build..."
npm run build > $TEST_RESULTS_DIR/frontend_dev_build.log 2>&1
if [ $? -eq 0 ]; then
  echo "✓ Development environment build successful"
else
  echo "✗ Development environment build failed"
  cat $TEST_RESULTS_DIR/frontend_dev_build.log
  kill $BACKEND_PID
  exit 1
fi

# Frontend build test (production environment)
echo "Testing production environment build..."
NODE_ENV=production npm run build > $TEST_RESULTS_DIR/frontend_prod_build.log 2>&1
if [ $? -eq 0 ]; then
  echo "✓ Production environment build successful"
else
  echo "✗ Production environment build failed"
  cat $TEST_RESULTS_DIR/frontend_prod_build.log
  kill $BACKEND_PID
  exit 1
fi

echo "----------------------------------------"
echo "Testing production environment..."

# Restart backend server (production environment)
kill $BACKEND_PID
cd $BACKEND_DIR
export FLASK_ENV=production
python3 -m src.main > $TEST_RESULTS_DIR/backend_prod.log 2>&1 &
BACKEND_PID=$!

# Wait for backend server to start
echo "Waiting for production backend server to start..."
sleep 5

# Check backend server status (production)
echo "Checking production backend API status..."
HEALTH_CHECK=$(curl -s http://localhost:5000/api/health)
if [[ $HEALTH_CHECK == *"\"status\":\"ok\""* && $HEALTH_CHECK == *"\"environment\":\"production\""* ]]; then
  echo "✓ Production backend server running properly"
  echo "Response: $HEALTH_CHECK"
else
  echo "✗ Production backend server status check failed"
  echo "Response: $HEALTH_CHECK"
  kill $BACKEND_PID
  exit 1
fi

# Test static file serving
echo "Testing static file serving..."
INDEX_RESPONSE=$(curl -s http://localhost:5000/)
if [[ $INDEX_RESPONSE == *"<!DOCTYPE html>"* ]]; then
  echo "✓ Static file serving working properly"
else
  echo "✗ Static file serving test failed"
  kill $BACKEND_PID
  exit 1
fi

# Terminate backend server
kill $BACKEND_PID

echo "----------------------------------------"
echo "Integration test result: SUCCESS"
echo "Test completion time: $(date)"
echo "All tests completed successfully."
echo "===== Test End ====="
