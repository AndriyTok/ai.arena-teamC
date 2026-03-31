# AI Arena Team C

This project is a battle simulator with:
- frontend: React + Vite (`src/`)
- backend: ASP.NET Core (`Arena.AI/`)
- battle logic core: .NET library (`Arena.AI.Core/`)

Backend calculates the whole battle and returns a list of battle actions. Frontend replays those actions as animation.

## Project structure

- `Arena.AI/Controllers/BattleCalculatorController.cs` - API endpoints for battle generation/calculation
- `Arena.AI.Core/Logic/AutoBattleCalculator.cs` - main battle loop
- `Arena.AI.Core/Logic/DamageCalculations.cs` - damage and balance logic
- `src/components/Arena.jsx` - game screen and action playback on frontend
- `src/api/` - API client and calls

## Prerequisites

- Node.js 20+
- npm 10+
- .NET SDK 8+
- Python 3.10+ (optional, for `sim.py`)
- DuckDB CLI (optional, for analytics storage)

## First run

Install frontend dependencies:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
npm install
```

Run both backend + frontend with one script:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
chmod +x scripts/start-dev.sh scripts/stop-dev.sh
./scripts/start-dev.sh
```

Stop both processes:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
./scripts/stop-dev.sh
```

Default ports:
- frontend: `http://localhost:5173`
- backend API: `http://localhost:5222`

## API quick check

```bash
curl -s "http://localhost:5222/BattleCalculator/random-team" | head -c 300
```

```bash
curl -s -X POST "http://localhost:5222/BattleCalculator/calculate-random-team" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Generate sample battle data

Create folder for samples:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
mkdir -p data/samples
```

Generate 20 random battle results as JSON:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
for i in {1..20}; do
  curl -s -X POST "http://localhost:5222/BattleCalculator/calculate-random-team" \
    -H "Content-Type: application/json" \
    -d '{}' > "data/samples/battle_$(printf "%03d" "$i").json"
done
```

Run match-up simulations (existing script):

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
python3 sim.py
```

## DuckDB integration (store samples)

If your goal is to collect results in DuckDB for analysis, the simplest path is:
1. Generate JSON samples into `data/samples/`
2. Import them into `data/arena.duckdb`

Create DB and load JSON:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
mkdir -p data

duckdb data/arena.duckdb "
CREATE TABLE IF NOT EXISTS battles AS
SELECT * FROM read_json_auto('data/samples/*.json', maximum_object_size=10485760);
"
```

If table already exists and you want to append new samples:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
duckdb data/arena.duckdb "
INSERT INTO battles
SELECT * FROM read_json_auto('data/samples/*.json', maximum_object_size=10485760);
"
```

Basic analytics examples:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
duckdb data/arena.duckdb "SELECT winner, COUNT(*) AS total FROM battles GROUP BY winner ORDER BY total DESC;"
```

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
duckdb data/arena.duckdb "SELECT AVG(array_length(actions)) AS avg_actions FROM battles;"
```

## Logs and troubleshooting

Script logs are written to:
- `.dev/logs/backend.log`
- `.dev/logs/frontend.log`

Inspect logs:

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
tail -n 100 .dev/logs/backend.log
```

```bash
cd "/Users/andriytok/Documents/7-8_semester/СПзШІ/ai.arena-teamC"
tail -n 100 .dev/logs/frontend.log
```

Common issues:
- Frontend opens but no battle starts: check backend log and `/BattleCalculator/calculate-random-team` endpoint
- Port conflict: stop old processes with `./scripts/stop-dev.sh` and restart
- HTTPS certificate problems in scripts/tools: use HTTP `http://localhost:5222` for local automation

## Notes

- Current battle rules are server-side in `Arena.AI.Core`.
- Frontend mostly visualizes the action stream returned by backend.
- Existing `README.md` is left unchanged; this file is an expanded project guide.

