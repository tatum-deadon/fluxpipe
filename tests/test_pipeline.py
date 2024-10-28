"""Tests for Pipeline."""

import pytest
from fluxpipe.pipeline import Pipeline, Stage, Step


def test_pipeline_creation():
    p = Pipeline("test")
    assert p.name == "test"
    assert p.status == "pending"


def test_stage_skip():
    stage = Stage("deploy", when="branch == main")
    assert stage.should_skip({"branch": "dev"})
    assert not stage.should_skip({"branch": "main"})


def test_step_creation():
    step = Step(run="echo hello")
    assert step.run_command == "echo hello"
