"""Framework configuration loading."""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent


def _deep_merge(base: dict, override: dict) -> dict:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_settings(config_dir: Path | None = None) -> dict:
    config_dir = Path(config_dir) if config_dir else ROOT / "config"
    settings = yaml.safe_load((config_dir / "default.yaml").read_text(encoding="utf-8")) or {}
    local = config_dir / "local.yaml"
    if local.exists():
        settings = _deep_merge(settings, yaml.safe_load(local.read_text(encoding="utf-8")) or {})
    load_dotenv(ROOT / ".env")
    adapter_name = os.environ.get("NV_EVAL_ADAPTER")
    if adapter_name:
        settings.setdefault("adapter", {})["name"] = adapter_name
    return settings
