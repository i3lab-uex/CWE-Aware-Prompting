#!/usr/bin/env python3
"""
Implementation of build_employee_report that safely renders a template
with employee data.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
# Dummy data model – in a real project these would come from a database or
# external service.  They are defined here only so that the module is self‑
# contained and testable.
# --------------------------------------------------------------------------- #
@dataclass
class Employee:
    """Represents an employee."""
    id: str
    name: str
    position: str
    department: str


@dataclass
class Performance:
    """Represents an employee's performance record."""
    employee_id: str
    rating: str
    feedback: str = field(repr=False)  # Sensitive information – not exposed by default
    bonus: float = field(repr=False)   # Sensitive information


# --------------------------------------------------------------------------- #
# In‑memory "database" – replace with real persistence in production.
# --------------------------------------------------------------------------- #
EMPLOYEES: Dict[str, Employee] = {
    "E001": Employee(id="E001", name="Alice Smith", position="Software Engineer", department="Engineering"),
    "E002": Employee(id="E002", name="Bob Johnson", position="Product Manager", department="Product"),
}

PERFORMANCES: Dict[str, Performance] = {
    "E001": Performance(employee_id="E001", rating="Excellent",
                        feedback="Outstanding performance in Q2.",
                        bonus=1500.00),
    "E002": Performance(employee_id="E002", rating="Good",
                        feedback="Met all deliverables.",
                        bonus=1200.00),
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _get_employee(employee_id: str) -> Employee:
    """Retrieve an employee by ID, raising ValueError if not found."""
    try:
        return EMPLOYEES[employee_id]
    except KeyError as exc:
        raise ValueError(f"Invalid employee ID: {employee_id}") from exc


def _get_performance(employee_id: str) -> Performance:
    """Retrieve a performance record by employee ID, raising ValueError if not found."""
    try:
        return PERFORMANCES[employee_id]
    except KeyError as exc:
        raise ValueError(f"No performance record for employee ID: {employee_id}") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def build_employee_report(employee_id: str, template: str) -> str:
    """
    Render a performance report for the given employee based on the supplied
    template string.

    Parameters
    ----------
    employee_id : str
        The unique identifier of the employee.
    template : str
        A template containing placeholders such as {staff.name},
        {staff.position}, and {evaluation.rating}.

    Returns
    -------
    str
        The fully rendered performance report.

    Raises
    ------
    ValueError
        If the employee ID is invalid, or if the template attempts to
        access sensitive data (feedback or bonus).
    """
    # Fetch required data objects
    employee = _get_employee(employee_id)
    performance = _get_performance(employee_id)

    # Regular expression to find placeholders like {staff.name}
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")

    def _replacement(match: re.Match) -> str:
        key = match.group(1).strip()

        # Security check – disallow sensitive fields
        if any(secret in key for secret in ("feedback", "bonus")):
            raise ValueError(f"Unauthorized access to sensitive data: '{key}'")

        # Resolve the placeholder
        if key.startswith("staff."):
            attr = key.split(".", 1)[1]
            try:
                return str(getattr(employee, attr))
            except AttributeError as exc:
                raise ValueError(f"Unknown staff attribute: '{attr}'") from exc

        if key.startswith("evaluation."):
            attr = key.split(".", 1)[1]
            try:
                return str(getattr(performance, attr))
            except AttributeError as exc:
                raise ValueError(f"Unknown evaluation attribute: '{attr}'") from exc

        # If the key doesn't match known namespaces, raise an error
        raise ValueError(f"Unsupported placeholder: '{key}'")

    # Perform the substitution safely
    try:
        report = placeholder_pattern.sub(_replacement, template)
    except re.error as exc:  # pragma: no cover – regex compile errors are unlikely
        raise ValueError("Invalid template syntax") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = (
        "Employee Report for {staff.name}\n"
        "Position: {staff.position} in {staff.department}\n"
        "Performance Rating: {evaluation.rating}"
    )
    print(build_employee_report("E001", tmpl))