# -*- coding: utf-8 -*-
"""
Performance report compilation module.

This module provides a single public function `compile_performance_report`
which takes an employee ID and a template string, replaces allowed
placeholders with the employee's data, and returns the resulting report.
"""

from __future__ import annotations

import string
from dataclasses import dataclass
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Mock data structures (replace with real implementations in production)
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
    """Represents performance data for an employee."""
    emp_id: str
    rating: float
    feedback: str  # sensitive field – must not be exposed
    bonus: float   # sensitive field – must not be exposed


# In‑memory "database" of employees and performance records.
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(emp_id="E001", name="Alice Smith", position="Senior Analyst",
                     department="Finance"),
    "E002": Employee(emp_id="E002", name="Bob Johnson", position="Developer",
                     department="Engineering"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(emp_id="E001", rating=4.5,
                        feedback="Excellent analytical skills.",
                        bonus=1200.00),
    "E002": Performance(emp_id="E002", rating=3.8,
                        feedback="Good teamwork.",
                        bonus=800.00),
}


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def _get_employee(emp_id: str) -> Employee:
    """Retrieve an employee by ID or raise ValueError."""
    try:
        return EMPLOYEES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Employee ID '{emp_id}' not found.") from exc


def _get_performance(emp_id: str) -> Performance:
    """Retrieve performance data for an employee or raise ValueError."""
    try:
        return PERFORMANCES[emp_id]
    except KeyError as exc:
        raise ValueError(f"Performance data for employee ID '{emp_id}' not found.") from exc


def _extract_placeholders(template: str) -> set[str]:
    """
    Parse the template and return a set of all field names used.
    Raises ValueError if restricted fields are referenced.
    """
    formatter = string.Formatter()
    placeholders: set[str] = set()

    for literal_text, field_name, format_spec, conversion in formatter.parse(template):
        if field_name is None:
            continue  # no placeholder
        # Disallow sensitive fields
        if field_name.startswith("performance."):
            subfield = field_name.split(".", 1)[-1]
            if subfield in {"feedback", "bonus"}:
                raise ValueError(f"Access to restricted field '{field_name}' is not allowed.")
        placeholders.add(field_name)

    return placeholders


def compile_performance_report(emp_id: str, report_template: str) -> str:
    """
    Generate a performance report for the given employee ID using the supplied template.

    Parameters
    ----------
    emp_id : str
        The unique identifier of the employee.
    report_template : str
        A format string containing placeholders such as '{employee.name}' or
        '{performance.rating}'. Restricted fields ('feedback', 'bonus') are not allowed.

    Returns
    -------
    str
        The formatted performance report string.

    Raises
    ------
    ValueError
        If the employee ID is invalid or if the template references restricted fields.
    """
    # Validate placeholders first (protect against injection of disallowed data)
    placeholders = _extract_placeholders(report_template)

    # Fetch the employee and performance records
    employee = _get_employee(emp_id)
    performance = _get_performance(emp_id)

    # Build the mapping dictionary for formatting
    context: Dict[str, Any] = {
        "employee.name": employee.name,
        "employee.position": employee.position,
        "employee.department": employee.department,
        "performance.rating": performance.rating,
    }

    # Perform the substitution
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        missing_field = exc.args[0]
        raise ValueError(f"Template references unknown field '{missing_field}'.") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}/5.0\n"
    )
    print(compile_performance_report("E001", template))