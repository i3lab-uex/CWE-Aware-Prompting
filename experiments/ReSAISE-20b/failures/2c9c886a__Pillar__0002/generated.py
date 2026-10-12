#!/usr/bin/env python3
"""
Implementation of `draft_student_report` for a student management system.
The function safely generates a report from a user‑supplied template while
preventing access to sensitive data and handling invalid input gracefully.
"""

from __future__ import annotations

import re
import string
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Domain model (simplified for demonstration)
# --------------------------------------------------------------------------- #

@dataclass
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    # Sensitive fields – must never appear in reports
    home_address: str = field(repr=False)
    discipline_record: Dict[str, str] = field(default_factory=dict, repr=False)

# In‑memory "database" of students
_STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record={"2022": "Good standing"},
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record={"2021": "Late submission"},
    ),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _get_student(student_number: str) -> Student:
    """Retrieve a student from the in‑memory database."""
    try:
        return _STUDENTS_DB[student_number]
    except KeyError as exc:
        raise ValueError(f"Student number '{student_number}' does not exist.") from exc


def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of placeholder names found in the template.
    This uses string.Formatter to correctly parse format fields.
    """
    formatter = string.Formatter()
    return {fname for _, fname, _, _ in formatter.parse(template) if fname}


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on a user‑supplied template.

    Parameters
    ----------
    student_number : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist, or if the template references
        disallowed (sensitive) fields.
    """
    # 1. Validate student existence
    student = _get_student(student_number)

    # 2. Define allowed fields (whitelist)
    ALLOWED_FIELDS = {
        "student.name",
        "student.course",
        "student.age",
        "student.GPA",
    }

    # 3. Extract placeholders and validate against whitelist
    placeholders = _extract_placeholders(report_template)
    disallowed = placeholders - ALLOWED_FIELDS

    if disallowed:
        raise ValueError(
            f"Template references disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # 4. Prepare mapping for safe formatting
    context = {
        "student": {
            "name": student.name,
            "course": student.course,
            "age": student.age,
            "GPA": student.GPA,
        }
    }

    # 5. Perform formatting in a safe manner
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen because we validated placeholders,
        # but catch it just in case.
        raise ValueError(f"Missing placeholder data: {exc}") from exc
    except Exception as exc:
        # Catch any other formatting errors (e.g., type errors)
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}\n"
    )
    try:
        print(draft_student_report("S001", template))
    except ValueError as e:
        print(f"Error: {e}")