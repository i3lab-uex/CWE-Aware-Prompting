# -*- coding: utf-8 -*-
"""
Performance report generator.

This module defines `compile_performance_report`, which renders a
performance summary for a given employee based on a template string.
Only non‑restricted fields are allowed in the template.  Attempts to
reference forbidden attributes such as `feedback` or `bonus`
will raise a ValueError.

The implementation uses only in‑memory data structures and does not
access external resources, so the risk of CWE‑664 (improper resource
control) is mitigated.  If this code were extended to use files or
network connections, those resources would be wrapped in context
managers (`with` statements) to guarantee proper release.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Domain model (minimal stubs for demonstration)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    """Represents an employee."""
    emp_id: str
    name: str
    position: str
    department: str


@dataclass
class Performance:
    """Represents an employee's performance data."""
    emp_id: str
    rating: float  # e.g. 4.2 out of 5
    feedback: str = field(repr=False)   # restricted
    bonus: float = field(repr=False)    # restricted


# --------------------------------------------------------------------------- #
# In‑memory data store
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith",
                     position="Senior Analyst", department="Finance"),
    "E002": Employee(emp_id="E002", name="Bob Jones",
                     position="Developer", department="Engineering"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.5,
                        feedback="Excellent work on Q2 report.",
                        bonus=1200.0),
    "E002": Performance(emp_id="E002", rating=3.8,
                        feedback="Good progress on project X.",
                        bonus=800.0),
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID, or raise ValueError if not found."""
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{emp_id}' does not exist.") from exc


def _get_performance(emp_id: str) -> Performance:
    """Retrieve performance data by employee ID, or raise ValueError if not found."""
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID '{emp_id}' not found.") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

_ALLOWED_FIELDS = {
    "employee.name",
    "employee.position",
    "employee.department",
    "performance.rating",
}

_FORBIDDEN_FIELDS = {
    "performance.feedback",
    "performance.bonus",
}


def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Render a performance summary for the given employee.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    report_template : str
        A template string that may contain placeholders such as
        '{employee.name}' or '{performance.rating}'.  Restricted fields
        (feedback, bonus) are not allowed.

    Returns
    -------
    str
        The formatted performance summary.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if a restricted field is
        referenced in the template.
    """
    # Fetch data (raises ValueError on failure)
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Build a mapping of allowed placeholders to actual values
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # Validate placeholders
    for ph in placeholders:
        if ph in _FORBIDDEN_FIELDS:
            raise ValueError(f"Access to restricted field '{ph}' is not allowed.")
        if ph not in _ALLOWED_FIELDS:
            raise ValueError(f"Unknown placeholder '{ph}' in template.")

    # Perform substitution
    try:
        result = report_template.format(**context)
    except KeyError as exc:  # pragma: no cover
        # This should not happen due to earlier validation, but guard anyway.
        raise ValueError(f"Missing data for placeholder {exc}") from exc

    return result


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee: {employee.name}\n"
        "Position: {employee.position} ({employee.department})\n"
        "Performance Rating: {performance.rating}/5.0\n"
    )
    print(compile_performance_report("E001", tmpl))