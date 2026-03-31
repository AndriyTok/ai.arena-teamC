import os
from pathlib import Path


def read_env_file(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_path.exists():
        return values

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, val = stripped.split("=", 1)
        values[key.strip()] = val.strip()
    return values


def get_config() -> dict[str, str]:
    repo_root = Path(__file__).resolve().parents[2]
    env_file = repo_root / "data-pipeline" / "config" / ".env"
    defaults = read_env_file(repo_root / "data-pipeline" / "config" / ".env.example")
    overrides = read_env_file(env_file)

    cfg = {**defaults, **overrides}

    # Allow direct shell env vars to override file settings.
    for key in list(cfg.keys()):
        if key in os.environ:
            cfg[key] = os.environ[key]

    cfg["REPO_ROOT"] = str(repo_root)
    return cfg


def ensure_parent(path_str: str) -> Path:
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

