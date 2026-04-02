"""
Config loader for AutoBehavior.

Loads a default YAML config and merges it with an optional task-specific YAML,
so that task-level keys override defaults while everything else is inherited.

Usage
-----
    from utils.config_loader import load_config

    cfg = load_config()                       # uses default.yaml + task from default
    cfg = load_config(task="ant")             # overrides task to 'ant'
    cfg = load_config(config_path="my.yaml")  # use a different base config
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

# Repository root (two levels up from this file: utils/ -> repo root)
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CONFIG = _REPO_ROOT / "config" / "default.yaml"
_TASKS_DIR = _REPO_ROOT / "config" / "tasks"


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge *override* into *base*, returning a new dict."""
    merged = base.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(
    config_path: str | os.PathLike | None = None,
    task: str | None = None,
) -> dict[str, Any]:
    """Load and return the merged configuration dictionary.

    Parameters
    ----------
    config_path:
        Path to the base YAML config file.  Defaults to
        ``config/default.yaml`` relative to the repository root.
    task:
        Task name whose config file (``config/tasks/<task>.yaml``) will be
        merged on top of the base config.  When *None*, the task name is
        read from the base config's ``task.name`` key.

    Returns
    -------
    dict
        The fully merged configuration as a plain Python dictionary.

    Raises
    ------
    FileNotFoundError
        If the base config or the task-specific config file cannot be found.
    """
    # Load base config
    base_path = Path(config_path) if config_path is not None else _DEFAULT_CONFIG
    if not base_path.exists():
        raise FileNotFoundError(f"Base config not found: {base_path}")

    with base_path.open() as f:
        cfg: dict[str, Any] = yaml.safe_load(f) or {}

    # Resolve the task name
    task_name = task or cfg.get("task", {}).get("name")

    # Merge task-specific config if one exists
    if task_name:
        task_path = _TASKS_DIR / f"{task_name}.yaml"
        if task_path.exists():
            with task_path.open() as f:
                task_cfg: dict[str, Any] = yaml.safe_load(f) or {}
            cfg = _deep_merge(cfg, task_cfg)

    return cfg
