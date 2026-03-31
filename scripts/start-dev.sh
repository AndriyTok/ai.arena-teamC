#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$ROOT_DIR/.dev"
LOG_DIR="$STATE_DIR/logs"

FRONTEND_PID_FILE="$STATE_DIR/frontend.pid"
BACKEND_PID_FILE="$STATE_DIR/backend.pid"

mkdir -p "$LOG_DIR"

is_running() {
  local pid="$1"
  kill -0 "$pid" >/dev/null 2>&1
}

port_listener_pid() {
  local port="$1"
  lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null | head -n 1
}

start_backend() {
  local port_pid
  port_pid="$(port_listener_pid 5222 || true)"

  # If something is already listening on backend port, reuse it instead of starting a duplicate process.
  if [[ -n "$port_pid" ]]; then
    echo "[backend] port 5222 already in use by pid=$port_pid; assuming backend is already running"
    return
  fi

  if [[ -f "$BACKEND_PID_FILE" ]]; then
    local existing_pid
    existing_pid="$(cat "$BACKEND_PID_FILE")"
    if [[ -n "$existing_pid" ]] && is_running "$existing_pid"; then
      echo "[backend] already running (pid=$existing_pid)"
      return
    fi
    rm -f "$BACKEND_PID_FILE"
  fi

  echo "[backend] starting on http://localhost:5222"
  (
    cd "$ROOT_DIR"
    dotnet run --project "Arena.AI/Arena.AI.csproj" --urls "http://localhost:5222"
  ) >"$LOG_DIR/backend.log" 2>&1 &

  echo "$!" > "$BACKEND_PID_FILE"
  echo "[backend] pid=$(cat "$BACKEND_PID_FILE"), log=$LOG_DIR/backend.log"
}

start_frontend() {
  local port_pid
  port_pid="$(port_listener_pid 5173 || true)"

  if [[ -n "$port_pid" ]]; then
    echo "[frontend] port 5173 already in use by pid=$port_pid; assuming frontend is already running"
    return
  fi

  if [[ -f "$FRONTEND_PID_FILE" ]]; then
    local existing_pid
    existing_pid="$(cat "$FRONTEND_PID_FILE")"
    if [[ -n "$existing_pid" ]] && is_running "$existing_pid"; then
      echo "[frontend] already running (pid=$existing_pid)"
      return
    fi
    rm -f "$FRONTEND_PID_FILE"
  fi

  echo "[frontend] starting on http://localhost:5173"
  (
    cd "$ROOT_DIR"
    npm run dev
  ) >"$LOG_DIR/frontend.log" 2>&1 &

  echo "$!" > "$FRONTEND_PID_FILE"
  echo "[frontend] pid=$(cat "$FRONTEND_PID_FILE"), log=$LOG_DIR/frontend.log"
}

start_backend
start_frontend

echo
echo "Started. Open: http://localhost:5173"
echo "If something fails, check logs:"
echo "  tail -n 50 \"$LOG_DIR/backend.log\""
echo "  tail -n 50 \"$LOG_DIR/frontend.log\""

