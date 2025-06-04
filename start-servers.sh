#!/bin/bash
# Simple script to start frontend and backend servers together
# Usage: ./start-servers.sh [dev|prod]

set -e

MODE="${1:-dev}"
FRONTEND_PORT=5173
BACKEND_PORT=5001

SCRIPT_DIR=$(cd -- "$(dirname "$0")" && pwd)
FRONTEND_DIR="$SCRIPT_DIR/frontend"
BACKEND_DIR="$SCRIPT_DIR/backend"

start_backend() {
  echo "Starting backend server ($MODE) on port $BACKEND_PORT"
  pushd "$BACKEND_DIR" >/dev/null
  export FLASK_ENV=$([ "$MODE" = "prod" ] && echo "production" || echo "development")
  export PORT=$BACKEND_PORT
  python -m src.main &
  BACKEND_PID=$!
  popd >/dev/null
}

start_frontend() {
  echo "Starting frontend server ($MODE) on port $FRONTEND_PORT"
  pushd "$FRONTEND_DIR" >/dev/null
  if [ ! -d node_modules ]; then
    npm install
  fi
  if [ "$MODE" = "prod" ]; then
    npm run build
    npm run preview -- --host 0.0.0.0 --port $FRONTEND_PORT &
  else
    npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT &
  fi
  FRONTEND_PID=$!
  popd >/dev/null
}

cleanup() {
  echo "Stopping servers..."
  kill $FRONTEND_PID $BACKEND_PID 2>/dev/null || true
}
trap cleanup INT TERM

start_backend
start_frontend

wait $BACKEND_PID $FRONTEND_PID
