# -*- coding: utf-8 -*-
"""
Employee performance report generator.

This module defines the `create_employee_report` function that
retrieves employee and performance data, substitutes placeholders
in a template string, and returns the formatted report.

Restricted fields (`feedback`, `bonus`) cannot be requested in
the template.  Attempting to do so raises a ValueError.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data model (simplified for this example)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    """Represents an employee record."""
    emp_id: str
    name: str
    position: str
    department: str


@dataclass
class Performance:
    """Represents performance data for an employee."""
    emp_id: str
    rating: float  # e.g., out of 5.0
    feedback: str = field(repr=False)  # Sensitive; not exposed in reports
    bonus: float = field(repr=False)   # Sensitive; not exposed in reports


# --------------------------------------------------------------------------- #
# In‑memory repository (replace with real DB access in production)
# --------------------------------------------------------------------------- #

EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith",
                     position="Software Engineer", department="Engineering"),
    "E002": Employee(emp_id="E002", name="Bob Johnson",
                     position="Product Manager", department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.5,
                        feedback="Excellent problem solving skills.",
                        bonus=1200.0),
    "E002": Performance(emp_id="E002", rating=3.8,
                        feedback="Great leadership on the Q2 launch.",
                        bonus=800.0),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

PLACEHOLDER_RE = re.compile(r"\{(?P<path>[\w\.]+)\}")


def _fetch_employee(emp_id: str) -> Employee:
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee with id '{emp_id}' not found") from exc


def _fetch_performance(emp_id: str) -> Performance:
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee '{emp_id}' not found") from exc


def _build_context(emp: Employee, perf: Performance) -> Dict[str, Any]:
    """
    Build a nested context dictionary for formatting.
    Restricted fields are omitted.
    """
    return {
        "employee": {
            "emp_id": emp.emp_id,
            "name": emp.name,
            "position": emp.position,
            "department": emp.department,
        },
        "performance": {
            "rating": perf.rating,
            # 'feedback' and 'bonus' are intentionally omitted
        },
    }


def _resolve_path(context: Dict[str, Any], path: str) -> Any:
    """
    Resolve a dotted path (e.g., 'employee.name') in the context dict.
    Raises KeyError if any part is missing.
    """
    parts = path.split(".")
    obj: Any = context
    for part in parts:
        if isinstance(obj, dict):
            obj = obj[part]
        else:
            # For nested dataclass objects
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                raise KeyError(f"Missing key '{part}' in path '{path}'")
    return obj


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def create_employee_report(emp_id: str, template_str: str) -> str:
    """
    Generate a formatted employee performance report.

    Parameters
    ----------
    emp_id : str
        Identifier of the employee.
    template_str : str
        Template string containing placeholders like '{employee.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance data is missing, or if a restricted
        field (`feedback`, `bonus`) is requested in the template.
    """
    # Validate restricted fields
    for match in PLACEHOLDER_RE.finditer(template_str):
        path = match.group("path")
        if path in {"performance.feedback", "performance.bonus"}:
            raise ValueError(f"Access to restricted field '{path}' is not allowed")

    # Retrieve data
    employee = _fetch_employee(emp_id)
    performance = _fetch_performance(emp_id)

    # Build context
    context = _build_context(employee, performance)

    # Resolve placeholders
    def replacer(match: re.Match) -> str:
        path = match.group("path")
        try:
            value = _resolve_path(context, path)
            return str(value)
        except KeyError as exc:
            raise ValueError(f"Invalid placeholder '{path}'") from exc

    # Perform substitution
    report = PLACEHOLDER_RE.sub(replacer, template_str)
    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Employee Report for {employee.name} ({employee.position})\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}/5\n"
    )
    print(create_employee_report("E001", tmpl))