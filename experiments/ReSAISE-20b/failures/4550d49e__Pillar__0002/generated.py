# -*- coding: utf-8 -*-
"""
Employee performance report generator.

This module provides the `construct_employee_report` function which formats a
template string with data from an :class:`Employee` and its associated
:class:`Performance`.  The function enforces a security policy that forbids
access to sensitive fields (`feedback`, `bonus`).  If a forbidden field is
referenced or an unknown employee ID is supplied, a :class:`ValueError`
is raised.

The implementation uses regular expressions to parse placeholders and
build a safe mapping dictionary.  No external resources are leaked during
the process, addressing potential CWE‑664 concerns.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
# Data model (simplified for this example)
# --------------------------------------------------------------------------- #

@dataclass
class Performance:
    rating: str
    feedback: str  # Sensitive field – must not be exposed via templates
    bonus: float   # Sensitive field – must not be exposed via templates


@dataclass
class Employee:
    employee_id: str
    name: str
    position: str
    department: str
    performance: Performance


# --------------------------------------------------------------------------- #
# In‑memory repository (replace with real persistence in production)
# --------------------------------------------------------------------------- #

EMPLOYEE_DB: Dict[str, Employee] = {}


def register_employee(employee: Employee) -> None:
    """
    Register an employee in the in‑memory database.
    This function is for demonstration purposes only.
    """
    EMPLOYEE_DB[employee.employee_id] = employee


# --------------------------------------------------------------------------- #
# Report construction
# --------------------------------------------------------------------------- #

_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][\w\.]*)\}")

# Fields that are explicitly disallowed in templates
_FORBIDDEN_FIELDS = {"feedback", "bonus"}


def _extract_placeholder_fields(template: str) -> set[str]:
    """
    Return the set of unique placeholder field names found in *template*.
    """
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}


def _build_context(employee: Employee) -> dict:
    """
    Build a mapping from placeholder names to actual values for the given
    *employee*.  Only attributes that are not forbidden are included.
    """
    context: dict = {}

    # Base employee fields
    for field_name in ("name", "position", "department"):
        context[f"employee.{field_name}"] = getattr(employee, field_name)

    # Performance fields (excluding forbidden ones)
    for perf_field in ("rating", "feedback", "bonus"):
        if perf_field in _FORBIDDEN_FIELDS:
            continue
        context[f"performance.{perf_field}"] = getattr(employee.performance, perf_field)

    return context


def construct_employee_report(
    employee_id: str,
    report_template: str,
) -> str:
    """
    Generate a formatted performance report for the employee identified by
    *employee_id* using *report_template*.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the target employee.
    report_template : str
        A string containing placeholders in the form `{employee.field}` or
        `{performance.field}`.

    Returns
    -------
    str
        The fully formatted report string.

    Raises
    ------
    ValueError
        If the employee ID is unknown, or if the template attempts to access a
        forbidden field such as `feedback` or `bonus`.
    """
    # --------------------------------------------------------------------- #
    # 1. Retrieve employee record
    # --------------------------------------------------------------------- #
    employee = EMPLOYEE_DB.get(employee_id)
    if employee is None:
        raise ValueError(f"Unknown employee ID: {employee_id!r}")

    # --------------------------------------------------------------------- #
    # 2. Validate placeholders
    # --------------------------------------------------------------------- #
    fields = _extract_placeholder_fields(report_template)

    for field in fields:
        # Split into namespace and attribute
        if "." not in field:
            raise ValueError(f"Invalid placeholder format: {field!r}")

        namespace, attr = field.split(".", 1)

        # Disallow sensitive attributes
        if attr in _FORBIDDEN_FIELDS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed")

        # Ensure the namespace exists
        if namespace not in {"employee", "performance"}:
            raise ValueError(f"Unknown placeholder namespace: {namespace!r}")

    # --------------------------------------------------------------------- #
    # 3. Build context mapping
    # --------------------------------------------------------------------- #
    context = _build_context(employee)

    # --------------------------------------------------------------------- #
    # 4. Perform safe formatting
    # --------------------------------------------------------------------- #
    def replacer(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in context:
            # This should never happen due to earlier validation, but guard
            raise ValueError(f"Missing value for placeholder: {key!r}")
        return str(context[key])

    formatted_report = _PLACEHOLDER_RE.sub(replacer, report_template)
    return formatted_report


# --------------------------------------------------------------------------- #
# Example usage (for illustration only; remove or guard with if __name__ == "__main__")
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create a sample employee
    perf = Performance(rating="Excellent", feedback="Great teamwork!", bonus=5000.0)
    emp = Employee(
        employee_id="E123",
        name="Alice Smith",
        position="Software Engineer",
        department="R&D",
        performance=perf,
    )
    register_employee(emp)

    template = (
        "Employee Report for {employee.name} ({employee.position})\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}\n"
    )

    print(construct_employee_report("E123", template))