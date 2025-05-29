#!/bin/bash

# Integration test script
# Performs full stack integration testing in development and production environments.

echo "===== AI Prompt Optimization Tool Integration Test ====="
echo "Test start time: $(date)"
echo "----------------------------------------"

# Set working directories
BASE_DIR="/home/ubuntu/ai-prompt-optimizer-restructured"
FRONTEND_DIR="$BASE_DIR/frontend"
BACKEND_DIR="$BASE_DIR/backend"
TEST_RESULTS_DIR="$BASE_DIR/tests/results"

# Create test results directory
mkdir -p $TEST_RESULTS_DIR

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
if [[ $MODELS_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ Models list API working properly"
  echo "Model count: $(echo $MODELS_RESPONSE | grep -o "model_id" | wc -l)"
else
  echo "✗ Models list API test failed"
  echo "Response: $MODELS_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test prompt optimization API
echo "Testing prompt optimization API..."
OPTIMIZE_RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d '{"input_text":"Please write an essay about the future of AI", "model_id":"gpt-4o"}' http://localhost:5000/api/optimize)
if [[ $OPTIMIZE_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ Prompt optimization API working properly"
else
  echo "✗ Prompt optimization API test failed"
  echo "Response: $OPTIMIZE_RESPONSE"
  kill $BACKEND_PID
  exit 1
fi

# Test model tips API
echo "Testing model tips API..."
TIPS_RESPONSE=$(curl -s http://localhost:5000/api/model/gpt-4o/tips)
if [[ $TIPS_RESPONSE == *"\"success\":true"* ]]; then
  echo "✓ Model tips API working properly"
else
  echo "✗ Model tips API test failed"
  echo "Response: $TIPS_RESPONSE"
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
