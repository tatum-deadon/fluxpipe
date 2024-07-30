"""Pipeline definition and runner."""

from __future__ import annotations
from typing import List, Dict, Optional, Any
from fluxpipe.pipeline.stage import Stage
import time
import yaml
import os


class Pipeline:
    """A CI/CD pipeline consisting of stages.

    Pipelines are defined declaratively and executed sequentially.
    Each stage can contain parallel steps.
    """

    def __init__(self, name: str, stages: Optional[List[Stage]] = None,
                 trigger: str = "manual", config: Optional[Dict] = None):
        self.name = name
        self.stages = stages or []
        self.trigger = trigger
        self.config = config or {}
        self._status = "pending"
        self._start_time = None
        self._end_time = None

    @classmethod
    def from_yaml(cls, path: str) -> "Pipeline":
        """Load a pipeline from a YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        stages = [Stage.from_dict(s) for s in data.get("stages", [])]
        return cls(
            name=data.get("name", "unnamed"),
            stages=stages,
            trigger=data.get("trigger", "manual"),
        )

    def run(self, context: Optional[Dict] = None) -> PipelineResult:
        """Execute the pipeline."""
        self._status = "running"
        self._start_time = time.perf_counter()
        context = context or {}
        stage_results = []

        for stage in self.stages:
            if stage.should_skip(context):
                stage_results.append({"stage": stage.name, "status": "skipped"})
                continue
            result = stage.run(context)
            stage_results.append(result)
            if result["status"] == "failed":
                self._status = "failed"
                break
        else:
            self._status = "passed"

        self._end_time = time.perf_counter()
        elapsed = self._end_time - self._start_time
        return PipelineResult(self.name, self._status, stage_results, elapsed)

    def add_stage(self, stage: Stage) -> None:
        self.stages.append(stage)

    @property
    def status(self) -> str:
        return self._status

    def __repr__(self) -> str:
        return f"Pipeline({self.name}, {len(self.stages)} stages, {self._status})"


class PipelineResult:
    """Result of a pipeline execution."""

    def __init__(self, name: str, status: str, stages: List[Dict], elapsed: float):
        self.name = name
        self.status = status
        self.stages = stages
        self.elapsed = elapsed

    def summary(self) -> str:
        lines = [f"Pipeline: {self.name}", f"Status: {self.status}", f"Time: {self.elapsed:.2f}s", ""]
        for s in self.stages:
            lines.append(f"  [{s['status']}] {s['stage']}")
        return "\n".join(lines)
