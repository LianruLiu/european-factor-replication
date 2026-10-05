"""YAML config loading and validation."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a study config file. Returns the config dict with ``_root`` set to
    the config file's parent directory (relative paths resolve against it)."""
    path = Path(path)
    with open(path) as fh:
        cfg = yaml.safe_load(fh)
    if not isinstance(cfg, dict):
        raise ValueError(f"config {path} must be a YAML mapping")
    cfg["_root"] = path.parent.resolve()
    _validate(cfg)
    return cfg


def resolve(path: str | Path, root: Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else root / p


def _validate(cfg: dict[str, Any]) -> None:
    data = cfg.get("data", {})
    if "factors" not in data or "portfolios" not in data:
        raise ValueError("config needs data.factors and data.portfolios")
    if not cfg.get("models"):
        raise ValueError("config needs at least one model under models:")
    uni = cfg.get("universe", {})
    if "factors" not in uni or "risk_free" not in uni:
        raise ValueError("config needs universe.factors and universe.risk_free")
