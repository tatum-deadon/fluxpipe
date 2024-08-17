"""Pipeline step -- single unit of work."""

from __future__ import annotations
from typing import Dict, Optional
import subprocess
import time


class Step:
    """A single step in a pipeline stage.

    Steps execute commands and track their output and status.
    """

    def __init__(self, name: Optional[str] = None, run: str = "",
                 timeout: int = 300, env: Optional[Dict] = None):
        self.name = name or run[:50]
        self.run_command = run
        self.timeout = timeout
        self.env = env

    @classmethod
    def from_dict(cls, data: Dict) -> "Step":
        return cls(
            name=data.get("name"),
            run=data.get("run", ""),
            timeout=data.get("timeout", 300),
            env=data.get("env"),
        )

    def run(self, context: Dict) -> Dict:
        """Execute this step."""
        start = time.perf_counter()
        try:
            result = subprocess.run(
                self.run_command, shell=True, capture_output=True,
                text=True, timeout=self.timeout, env=self.env,
            )
            elapsed = time.perf_counter() - start
            status = "passed" if result.returncode == 0 else "failed"
            return {
                "step": self.name,
                "status": status,
                "stdout": result.stdout[:1000],
                "stderr": result.stderr[:500],
                "elapsed": elapsed,
            }
        except subprocess.TimeoutExpired:
            return {"step": self.name, "status": "failed", "error": "timeout"}
        except Exception as e:
            return {"step": self.name, "status": "failed", "error": str(e)}

    def __repr__(self) -> str:
        return f"Step({self.name})"
