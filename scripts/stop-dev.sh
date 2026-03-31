#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$ROOT_DIR/.dev"

FRONTEND_PID_FILE="$STATE_DIR/frontend.pid"
BACKEND_PID_FILE="$STATE_DIR/backend.pid"

port_listener_pid() {
  local port="$1"
  lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null | head -n 1
}

stop_known_process_on_port() {
  local name="$1"
  local port="$2"
  local expected_a="$3"
  local expected_b="$4"

  local pid
  pid="$(port_listener_pid "$port" || true)"

  if [[ -z "$pid" ]]; then
    return
  fi

  local cmd
  cmd="$(ps -p "$pid" -o command= 2>/dev/null || true)"

  if [[ "$cmd" == *"$expected_a"* || "$cmd" == *"$expected_b"* ]]; then
    kill "$pid" >/dev/null 2>&1 || true
    echo "[$name] stopped process on port $port (pid=$pid)"
  else
    echo "[$name] port $port is used by another process (pid=$pid), not stopping it"
  fi
}

stop_by_pid_file() {
  local name="$1"
  local pid_file="$2"

  if [[ ! -f "$pid_file" ]]; then
    echo "[$name] pid file not found, nothing to stop"
    return
  fi

  local pid
  pid="$(cat "$pid_file")"

  if [[ -z "$pid" ]]; then
    echo "[$name] pid file is empty"
    rm -f "$pid_file"
    return
  fi

  if kill -0 "$pid" >/dev/null 2>&1; then
    kill "$pid" >/dev/null 2>&1 || true

    # Wait up to 5s for graceful stop.
    local retries=25
    while kill -0 "$pid" >/dev/null 2>&1 && (( retries > 0 )); do
      sleep 0.2
      ((retries--))
    done

    if kill -0 "$pid" >/dev/null 2>&1; then
      kill -9 "$pid" >/dev/null 2>&1 || true
      echo "[$name] force-stopped pid=$pid"
    else
      echo "[$name] stopped pid=$pid"
    fi
  else
    echo "[$name] process pid=$pid is not running"
  fi

  rm -f "$pid_file"
}

stop_by_pid_file "frontend" "$FRONTEND_PID_FILE"
stop_by_pid_file "backend" "$BACKEND_PID_FILE"

# Fallback for processes started outside scripts (no pid files).
stop_known_process_on_port "frontend" 5173 "vite" "node"
stop_known_process_on_port "backend" 5222 "dotnet" "Arena.AI"

echo "Done."

