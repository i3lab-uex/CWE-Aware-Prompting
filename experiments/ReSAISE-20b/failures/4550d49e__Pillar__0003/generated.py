#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance report generator.

This module provides a single public function:
    construct_employee_report(employee_id: str, report_template: str) -> str

The function retrieves an employee's data from the global registry
(`EMPLOYEE_DB`) and substitutes placeholders in *report_template*
with corresponding attributes.  Any attempt to access restricted
fields (``feedback`` or ``bonus``) results in a :class:`ValueError`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Dummy data model (replace with real implementations in production)
# --------------------------------------------------------------------------- #

@dataclass
class Performance:
    rating: float
    feedback: str = field(repr=False)
    bonus: float = field(repr=False)


@dataclass
class Employee:
    employee_id: str
    name: str
    position: str
    department: str
    performance: Performance


# --------------------------------------------------------------------------- #
# Global employee registry (mock database)
# --------------------------------------------------------------------------- #

EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        employee_id="E001",
        name="Alice Smith",
        position="Senior Developer",
        department="Engineering",
        performance=Performance(
            rating=4.5,
            feedback="Excellent problem‑solving skills.",
            bonus=1200.0
        ),
    ),
    "E002": Employee(
        employee_id="E002",
        name="Bob Johnson",
        position="Product Manager",
        department="Product",
        performance=Performance(
            rating=4.0,
            feedback="Strong leadership.",
            bonus=1500.0
        ),
    ),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

PLACEHOLDER_REGEX = re.compile(r"\{([^}]+)\}")

RESTRICTED_FIELDS = {"feedback", "bonus"}


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of unique placeholder names found in *template*."""
    return {match.group(1) for match in PLACEHOLDER_REGEX.finditer(template)}


def _build_context(employee: Employee) -> Dict[str, Any]:
    """
    Build a mapping from placeholder keys to their values.

    The key format is ``{entity.attribute}`` where *entity* is either
    ``employee`` or ``performance``.
    """
    ctx: Dict[str, Any] = {}

    # Employee attributes
    for field_name in employee.__dataclass_fields__:
        if field_name == "performance":
            continue
        ctx[f"employee.{field_name}"] = getattr(employee, field_name)

    # Performance attributes
    perf = employee.performance
    for field_name in perf.__dataclass_fields__:
        ctx[f"performance.{field_name}"] = getattr(perf, field_name)

    return ctx


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Generate a performance report for *employee_id* based on
    *report_template*.

    Parameters
    ----------
    employee_id : str
        Unique identifier of the employee.
    report_template : str
        Template string containing placeholders such as
        ``{employee.name}`` or ``{performance.rating}``.

    Returns
    -------
    str
        The formatted report.

    Raises
    ------
    ValueError
        If *employee_id* is not found, or if the template attempts to
        access restricted fields (``feedback`` or ``bonus``).
    """
    # 1. Validate employee existence
    try:
        employee = EMPLOYEE_DB[employee_id]
    except KeyError as exc:
        raise ValueError(f"Unknown employee ID: {employee_id}") from exc

    # 2. Extract placeholders and validate
    placeholders = _extract_placeholders(report_template)

    for key in placeholders:
        if any(key.startswith(prefix) for prefix in ("employee.", "performance.")):
            # Check for restricted fields
            _, attr = key.split(".", 1)
            if attr in RESTRICTED_FIELDS:
                raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
        else:
            # Unknown placeholder format
            raise ValueError(f"Unsupported placeholder '{key}' in template.")

    # 3. Build context and perform formatting
    ctx = _build_context(employee)

    try:
        formatted_report = report_template.format(**ctx)
    except KeyError as exc:
        # This should not happen because we validated placeholders,
        # but guard against unexpected errors.
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted_report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Employee Report for {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Performance Rating: {performance.rating}/5.0\n"
    )
    print(construct_employee_report("E001", template))