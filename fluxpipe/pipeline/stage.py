"""Pipeline stage."""

from __future__ import annotations
from typing import List, Dict, Optional, Any
from fluxpipe.pipeline.step import Step


class Stage:
    """A stage in a pipeline containing parallel steps."""

    def __init__(self, name: str, steps: Optional[List[Step]] = None,
                 when: Optional[str] = None):
        self.name = name
        self.steps = steps or []
        self.when = when

    @classmethod
    def from_dict(cls, data: Dict) -> "Stage":
        steps = [Step.from_dict(s) for s in data.get("steps", [])]
        return cls(name=data["name"], steps=steps, when=data.get("when"))

    def should_skip(self, context: Dict) -> bool:
        """Evaluate condition to determine if stage should run."""
        if not self.when:
            return False
        # Simple condition evaluation
        if "==" in self.when:
            key, value = self.when.split("==")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            return context.get(key) != value
        return False

    def run(self, context: Dict) -> Dict:
        """Execute all steps in this stage."""
        step_results = []
        for step in self.steps:
            result = step.run(context)
            step_results.append(result)
            if result["status"] == "failed":
                return {"stage": self.name, "status": "failed", "steps": step_results}
        return {"stage": self.name, "status": "passed", "steps": step_results}

    def add_step(self, step: Step) -> None:
        self.steps.append(step)

    def __repr__(self) -> str:
        return f"Stage({self.name}, {len(self.steps)} steps)"
