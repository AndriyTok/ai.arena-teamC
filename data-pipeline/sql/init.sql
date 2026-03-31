CREATE TABLE IF NOT EXISTS battles (
    battle_id VARCHAR PRIMARY KEY,
    winner VARCHAR,
    actions_count INTEGER DEFAULT 0,
    extracted_at TIMESTAMP DEFAULT current_timestamp,
    raw_json VARCHAR
);

