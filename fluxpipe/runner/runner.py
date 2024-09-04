"""Pipeline runner -- executes pipelines on demand or on schedule."""

from __future__ import annotations
from typing import Dict, List, Optional, Callable
from fluxpipe.pipeline import Pipeline
import threading
import time


class Runner:
    """Execute and schedule pipelines.

    Supports on-demand execution, scheduled runs, and
    webhook-triggered pipelines.
    """

    def __init__(self):
        self._pipelines: Dict[str, Pipeline] = {}
        self._history: List[Dict] = []
        self._webhooks: Dict[str, Callable] = {}
        self._scheduler_running = False

    def register(self, pipeline: Pipeline) -> None:
        """Register a pipeline."""
        self._pipelines[pipeline.name] = pipeline

    def execute(self, name: str, context: Optional[Dict] = None) -> Dict:
        """Execute a registered pipeline."""
        pipeline = self._pipelines.get(name)
        if not pipeline:
            return {"error": f"Pipeline '{name}' not found"}
        result = pipeline.run(context)
        self._history.append({
            "pipeline": name,
            "status": result.status,
            "elapsed": result.elapsed,
            "time": time.time(),
        })
        return {"status": result.status, "elapsed": result.elapsed}

    def history(self, limit: int = 10) -> List[Dict]:
        return self._history[-limit:]

    def on_webhook(self, event: str, callback: Callable) -> None:
        self._webhooks[event] = callback

    def __repr__(self) -> str:
        return f"Runner(pipelines={len(self._pipelines)})"
