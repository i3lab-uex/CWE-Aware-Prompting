#!/usr/bin/env python3
"""
Performance summary generator.

The module defines a single public function:

    create_performance_summary(emp_id: str, summary_template: str) -> str

It uses in‑memory mock data for `Employee` and `Performance` objects.
Only a limited set of fields are permitted to be accessed from the
template; attempting to reference any restricted field (e.g. `feedback`
or `bonus`) results in a `ValueError`.  An invalid employee ID also
raises a `ValueError`.

The implementation deliberately avoids using `eval` or other unsafe
mechanisms.  It uses a custom mapping that resolves attribute chains in a
controlled way and validates the requested fields before formatting.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# ----------------------------------------------------------------------
# Mock data models
# ----------------------------------------------------------------------


@dataclass
class Performance:
    rating: str
    feedback: str = field(repr=False)  # sensitive, not exposed in summary
    bonus: float = field(repr=False)


@dataclass
class Employee:
    emp_id: str
    name: str
    position: str
    department: str
    performance: Performance


# In‑memory employee store (id -> Employee)
_EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(
        emp_id="E001",
        name="Alice Smith",
        position="Senior Engineer",
        department="R&D",
        performance=Performance(
            rating="Excellent",
            feedback="Outstanding contribution to project X.",
            bonus=1200.00,
        ),
    ),
    "E002": Employee(
        emp_id="E002",
        name="Bob Johnson",
        position="Marketing Lead",
        department="Marketing",
        performance=Performance(
            rating="Satisfactory",
            feedback="Meets expectations.",
            bonus=800.00,
        ),
    ),
}


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------


def _get_attribute_chain(obj: Any, chain: str) -> Any:
    """
    Resolve an attribute chain like 'employee.name' on the given object.
    Raises AttributeError if any part of the chain is missing.
    """
    current = obj
    for attr in chain.split("."):
        if not hasattr(current, attr):
            raise AttributeError(f"Attribute '{attr}' not found in {current!r}")
        current = getattr(current, attr)
    return current


# ----------------------------------------------------------------------
# Main API
# ----------------------------------------------------------------------


def create_performance_summary(emp_id: str, summary_template: str) -> str:
    """
    Generate a performance summary for the employee identified by `emp_id`
    using the provided `summary_template`.

    The template may contain placeholders in the form `{employee.<field>}` or
    `{performance.<field>}`.  Only a restricted set of fields are allowed:
        - employee.name
        - employee.position
        - employee.department
        - performance.rating

    Accessing any other field (e.g. `feedback`, `bonus`) will raise a
    ValueError.

    Parameters:
        emp_id (str): The unique identifier of the employee.
        summary_template (str): A format string containing placeholders.

    Returns:
        str: The formatted performance summary.

    Raises:
        ValueError: If the employee ID is invalid or if the template
                    references a restricted field.
    """
    # Validate employee existence
    try:
        employee = _EMPLOYEE_DB[emp_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {emp_id}") from exc

    # Allowed placeholders
    allowed_keys = {
        "employee.name",
        "employee.position",
        "employee.department",
        "performance.rating",
    }

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^\{\}]+)\}")
    placeholders = set(placeholder_pattern.findall(summary_template))

    # Check for restricted fields
    for key in placeholders:
        if key not in allowed_keys:
            raise ValueError(f"Access to restricted or unknown field '{key}' is not permitted")

    # Build a mapping for formatting
    mapping: Dict[str, Any] = {}
    for key in placeholders:
        try:
            value = _get_attribute_chain(employee, key)
        except AttributeError as exc:
            raise ValueError(f"Invalid placeholder '{key}' in template") from exc
        mapping[key] = value

    # Perform formatting safely
    try:
        summary = summary_template.format_map(mapping)
    except KeyError as exc:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing value for placeholder {exc}") from exc

    return summary


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}"
    )
    print(create_performance_summary("E001", template))