from .baseline import build_prompt as baseline_prompt

# Pipelines registration
PIPELINES = {
    "baseline": baseline_prompt
}