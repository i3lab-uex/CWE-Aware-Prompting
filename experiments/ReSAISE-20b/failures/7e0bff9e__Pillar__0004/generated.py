# -*- coding: utf-8 -*-
"""
Implementation of a simple employee performance reporting system.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data models
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Employee:
    """Represents an employee."""
    emp_code: str
    name: str
    position: str
    department: str


@dataclass(frozen=True)
class Performance:
    """Represents an employee's performance record."""
    emp_code: str
    rating: float            # e.g. 4.5 out of 5
    comments: str
    feedback: str = field(repr=False)   # sensitive, not exposed in reports
    bonus: float = field(repr=False)    # sensitive, not exposed


# --------------------------------------------------------------------------- #
# In‑memory datastore
# --------------------------------------------------------------------------- #

# Sample data – in a real system this would be retrieved from a database.
EMPLOYEE_DB: Dict[str, Employee] = {
    "E001": Employee(emp_code="E001", name="Alice Smith",
                     position="Software Engineer", department="Engineering"),
    "E002": Employee(emp_code="E002", name="Bob Jones",
                     position="Product Manager", department="Product"),
}

PERFORMANCE_DB: Dict[str, Performance] = {
    "E001": Performance(emp_code="E001", rating=4.8,
                        comments="Excellent problem‑solving skills.",
                        feedback="Keep up the great work!",
                        bonus=1200.00),
    "E002": Performance(emp_code="E002", rating=4.2,
                        comments="Strong leadership.",
                        feedback="Consider mentoring junior staff.",
                        bonus=950.00),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

PLACEHOLDER_PATTERN = re.compile(r"{(?P<path>[^}]+)}")


def _get_attr_from_path(obj: Any, path: str) -> Any:
    """
    Safely retrieve a nested attribute from an object following a dot‑separated path.
    Raises ValueError if the attribute does not exist or is restricted.
    """
    # Disallow access to private or dunder attributes
    if path.startswith("_") or "__" in path:
        raise ValueError(f"Access to private attribute '{path}' is forbidden.")

    # Disallow restricted fields
    if path in {"performance.feedback", "performance.bonus"}:
        raise ValueError(f"Access to restricted field '{path}' is forbidden.")

    # Resolve the path
    parts = path.split(".")
    if not parts:
        raise ValueError("Empty placeholder path.")

    current = obj
    for part in parts:
        if not hasattr(current, part):
            raise ValueError(f"Attribute '{part}' not found in {current!r}.")
        current = getattr(current, part)
    return current


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def create_performance_report(emp_code: str, summary_template: str) -> str:
    """
    Generate a performance report for the given employee using the supplied template.

    Parameters
    ----------
    emp_code : str
        The unique identifier for the employee.
    summary_template : str
        Template string containing placeholders like '{employee.name}' or
        '{performance.rating}'. Restricted fields (feedback, bonus) cannot be used.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the employee or performance record does not exist, if a placeholder is invalid,
        or if restricted fields are requested.
    """
    # Retrieve data – in a real implementation these would be database calls
    employee = EMPLOYEE_DB.get(emp_code)
    if employee is None:
        raise ValueError(f"Employee with code '{emp_code}' not found.")

    performance = PERFORMANCE_DB.get(emp_code)
    if performance is None:
        raise ValueError(f"Performance record for employee '{emp_code}' not found.")

    # Build a context dictionary mapping top‑level names to objects
    context = {
        "employee": employee,
        "performance": performance,
    }

    # Find all placeholders in the template
    def replace_placeholder(match: re.Match) -> str:
        path = match.group("path")
        try:
            value = _get_attr_from_path(context, path)
        except ValueError as exc:
            raise ValueError(f"Invalid placeholder '{path}': {exc}") from None
        # Convert the value to string for formatting
        return str(value)

    try:
        result = PLACEHOLDER_PATTERN.sub(replace_placeholder, summary_template)
    except ValueError as exc:
        # Re‑raise with a clear message
        raise ValueError(f"Failed to generate report: {exc}") from None

    return result


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Employee: {employee.name}\n"
        "Position: {employee.position} in {employee.department}\n"
        "Performance Rating: {performance.rating}\n"
        "Comments: {performance.comments}"
    )
    print(create_performance_report("E001", template))