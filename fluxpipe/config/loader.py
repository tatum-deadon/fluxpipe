"""Configuration loader."""

from __future__ import annotations
from typing import Dict, Any
import yaml
import os


def load_config(path: str = "fluxpipe.yaml") -> Dict[str, Any]:
    """Load pipeline configuration from YAML."""
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def create_default_config(path: str = "fluxpipe.yaml") -> str:
    """Create a default pipeline configuration."""
    config = {
        "name": "my-pipeline",
        "trigger": "push",
        "stages": [
            {"name": "build", "steps": [{"run": "echo 'Building...'"}]},
            {"name": "test", "steps": [{"run": "echo 'Testing...'"}]},
            {"name": "deploy", "when": 'branch == "main"',
             "steps": [{"run": "echo 'Deploying...'"}]},
        ],
    }
    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    return path
