#!/usr/bin/env python3
"""
Employee performance report generator.

This module defines a single public function, :func:`construct_employee_report`,
which accepts an employee identifier and a template string.  The function
replaces placeholders of the form ``{employee.field}`` or ``{performance.field}``
with the corresponding values from an :class:`Employee` instance and its
associated :class:`Performance` record.

The function validates the template to ensure that no restricted fields
(`feedback`, `bonus`) are exposed and that the supplied employee ID exists.
If either check fails, a :class:`ValueError` is raised.

The implementation avoids any dynamic code execution and uses
``string.Formatter`` for safe placeholder resolution.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Mock data structures (in a real system these would be imported)
# --------------------------------------------------------------------------- #

@dataclass
class Employee:
    """Represents an employee in the system."""
    id: str
    name: str
    position: str
    department: str


@dataclass
class Performance:
    """Represents an employee's performance record."""
    employee_id: str
    rating: float
    feedback: str = field(repr=False)  # Sensitive, not exposed publicly
    bonus: float = field(repr=False)   # Sensitive, not exposed publicly


# In-memory data store (replace with real database queries in production)
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer",
                     department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager",
                     department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating=4.5,
                        feedback="Excellent work on the backend overhaul.",
                        bonus=1500.00),
    "E002": Performance(employee_id="E002", rating=3.8,
                        feedback="Good leadership on the new feature.",
                        bonus=1200.00),
}


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

RESTRICTED_FIELDS = {"feedback", "bonus"}
PLACEHOLDER_PATTERN = re.compile(r"{\s*(?P<source>\w+)\.(?P<field>\w+)\s*}")


def construct_employee_report(employee_id: str, report_template: str) -> str:
    """
    Generate a performance summary for the given employee using the supplied
    template.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the target employee.
    report_template : str
        A string containing placeholders such as ``{employee.name}``,
        ``{performance.rating}``, etc.

    Returns
    -------
    str
        The formatted performance report.

    Raises
    ------
    ValueError
        If the employee ID is unknown, if the template references a restricted
        field (e.g., ``feedback`` or ``bonus``), or if the template contains
        an unknown placeholder source.

    Notes
    -----
    * The function does **not** evaluate arbitrary Python code; it performs a
      safe lookup of attributes.
    * Restricted fields are explicitly disallowed to prevent accidental
      leakage of confidential data.

    """
    # --------------------------------------------------------------------- #
    # 1. Validate employee existence
    # --------------------------------------------------------------------- #
    employee = EMPLOYEES.get(employee_id)
    if employee is None:
        raise ValueError(f"Employee ID '{employee_id}' not found.")

    performance = PERFORMANCES.get(employee_id)
    if performance is None:
        raise ValueError(f"Performance record for employee ID '{employee_id}' not found.")

    # --------------------------------------------------------------------- #
    # 2. Prepare a lookup dictionary for formatting
    # --------------------------------------------------------------------- #
    context: Dict[str, Any] = {
        "employee": employee,
        "performance": performance,
    }

    # --------------------------------------------------------------------- #
    # 3. Scan the template for placeholders
    # --------------------------------------------------------------------- #
    def replacement(match: re.Match) -> str:
        source = match.group("source")
        field_name = match.group("field")

        # Disallow restricted fields
        if source == "performance" and field_name in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is prohibited.")

        # Resolve the attribute
        try:
            obj = context[source]
        except KeyError:
            raise ValueError(f"Unknown placeholder source '{source}' in template.")

        try:
            value = getattr(obj, field_name)
        except AttributeError as exc:
            raise ValueError(
                f"Field '{field_name}' not found in source '{source}'."
            ) from exc

        # Convert to string for formatting
        return str(value)

    # --------------------------------------------------------------------- #
    # 4. Perform substitution safely
    # --------------------------------------------------------------------- #
    try:
        report = PLACEHOLDER_PATTERN.sub(replacement, report_template)
    except ValueError as e:
        # Re‑raise with the same message
        raise

    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Employee Report\n"
        "----------------\n"
        "Name: {employee.name}\n"
        "Position: {employee.position}\n"
        "Department: {employee.department}\n"
        "Rating: {performance.rating}\n"
    )
    print(construct_employee_report("E001", template))