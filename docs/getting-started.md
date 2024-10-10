# Getting Started

## Installation

```bash
pip install fluxpipe
```

## Initialize a Pipeline

```bash
fluxpipe init
```

This creates a `fluxpipe.yaml` with a basic build-test-deploy pipeline.

## Run Your Pipeline

```bash
fluxpipe run
```

## Pipeline Syntax

```yaml
name: my-pipeline
trigger: push  # push, pull_request, schedule, manual

stages:
  - name: build
    steps:
      - run: pip install -e .
  
  - name: test
    steps:
      - run: pytest tests/
  
  - name: deploy
    when: branch == "main"
    steps:
      - run: ./deploy.sh
```
