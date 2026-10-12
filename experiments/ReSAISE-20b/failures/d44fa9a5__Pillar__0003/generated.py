# -*- coding: utf-8 -*-
"""
Employee performance report generator.

The module defines a single public function `create_employee_report` that
produces a formatted performance summary for a given worker ID.  The
function only exposes non‑sensitive fields (name, department,
rating) and raises a `ValueError` if the template tries to access
restricted data such as feedback or bonus.

The implementation uses a lightweight in‑memory repository for demo
purposes, but the API can be replaced with real persistence layers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data models (minimal stubs for demonstration)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    """Represents an employee."""
    worker_id: str
    name: str
    department: str


@dataclass
class Performance:
    """Represents an employee's performance assessment."""
    worker_id: str
    rating: float  # e.g. 4.5 out of 5
    feedback: str = field(repr=False)   # Sensitive – should not be exposed
    bonus: float = field(default=0.0, repr=False)  # Sensitive


# --------------------------------------------------------------------------- #
# In‑memory repository (replaceable with a database backend)
# --------------------------------------------------------------------------- #

class Repository:
    """Simple in‑memory data store."""

    _employees: Dict[str, Employee] = {}
    _performances: Dict[str, Performance] = {}

    @classmethod
    def add_employee(cls, employee: Employee) -> None:
        cls._employees[employee.worker_id] = employee

    @classmethod
    def add_performance(cls, performance: Performance) -> None:
        cls._performances[performance.worker_id] = performance

    @classmethod
    def get_employee(cls, worker_id: str) -> Employee:
        try:
            return cls._employees[worker_id]
        except KeyError as exc:
            raise ValueError(f"Invalid worker ID: {worker_id}") from exc

    @classmethod
    def get_performance(cls, worker_id: str) -> Performance:
        try:
            return cls._performances[worker_id]
        except KeyError as exc:
            raise ValueError(f"No performance record for worker ID: {worker_id}") from exc


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

# Regular expression to find placeholders in the form {something}
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

# Set of allowed fields that can be used in the template
_ALLOWED_FIELDS = {"worker.name", "worker.department", "assessment.rating"}


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1).strip() for match in _PLACEHOLDER_RE.finditer(template)}


def _build_context(worker: Employee, performance: Performance) -> Dict[str, Any]:
    """Build a mapping that can be used with str.format."""
    return {
        "worker.name": worker.name,
        "worker.department": worker.department,
        "assessment.rating": performance.rating,
    }


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def create_employee_report(worker_id: str, template: str) -> str:
    """
    Generate a performance report for the given worker.

    Parameters
    ----------
    worker_id : str
        Unique identifier of the employee.
    template : str
        Template string containing placeholders such as
        '{worker.name}', '{worker.department}', and '{assessment.rating}'.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the worker ID is unknown, or if the template contains
        placeholders for restricted data (e.g., feedback, bonus).
    """
    # Validate template placeholders early
    placeholders = _extract_placeholders(template)
    unauthorized = placeholders - _ALLOWED_FIELDS
    if unauthorized:
        raise ValueError(
            f"Template contains disallowed placeholders: {', '.join(sorted(unauthorized))}"
        )

    # Retrieve data
    worker = Repository.get_employee(worker_id)
    performance = Repository.get_performance(worker_id)

    # Build context and format
    ctx = _build_context(worker, performance)
    try:
        return template.format(**ctx)
    except KeyError as exc:  # pragma: no cover
        # This should not happen because we pre‑validated placeholders,
        # but guard against any unforeseen errors.
        raise ValueError(f"Missing data for placeholder: {exc}") from exc


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate repository with demo data
    Repository.add_employee(Employee(worker_id="E123", name="Alice Smith", department="Engineering"))
    Repository.add_performance(
        Performance(worker_id="E123", rating=4.7, feedback="Excellent teamwork.", bonus=1200.00)
    )

    # Define a safe template
    tmpl = (
        "Employee Report\n"
        "Name: {worker.name}\n"
        "Department: {worker.department}\n"
        "Rating: {assessment.rating}/5\n"
    )

    # Generate report
    print(create_employee_report("E123", tmpl))