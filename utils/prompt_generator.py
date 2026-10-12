"""Compatibility wrapper around the experiment's prompt builder."""

from __future__ import annotations

from cwe_experiment.dataset import Sample
from cwe_experiment.prompts import build_prompt, build_prompt_conditions

__all__ = ["Sample", "build_prompt", "build_prompt_conditions"]
