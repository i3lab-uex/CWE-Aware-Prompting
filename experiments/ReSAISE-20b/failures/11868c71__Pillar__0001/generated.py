#!/usr/bin/env python3
"""
Student report builder.

The module defines a minimal Student data structure and a helper function
`build_student_profile`.  The function formats a report string using the
provided template while protecting sensitive attributes from being exposed.
"""

from __future__ import annotations

import string
from dataclasses import dataclass, field
from typing import Dict, Mapping, Any

# --------------------------------------------------------------------------- #
# Data model                                                             #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)          # Sensitive
    home_address: str = field(repr=False)   # Sensitive
    discipline_record: str

# --------------------------------------------------------------------------- #
# In‑memory storage (simulating a database)                               #
# --------------------------------------------------------------------------- #

_students: Dict[str, Student] = {
    "s12345": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.9,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "s67890": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late assignment on 2023-07-01"
    ),
}

# --------------------------------------------------------------------------- #
# Helper utilities                                                        #
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"gpa", "home_address"}


def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive attributes.
    Raises ValueError if a forbidden field is detected.
    """
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if not field_name:
            continue  # Skip literal braces
        # Handle nested attributes (e.g., student.name)
        parts = field_name.split(".")
        if len(parts) == 2 and parts[0] == "student":
            attr = parts[1]
        else:
            # Unexpected format; treat as error for safety
            raise ValueError(f"Unsupported placeholder '{field_name}'.")
        if attr in _SENSITIVE_FIELDS:
            raise ValueError(
                f"Access to sensitive attribute '{attr}' is prohibited."
            )


def _build_context(student: Student) -> Mapping[str, Any]:
    """
    Build a safe context dictionary for formatting.
    Only non‑sensitive attributes are exposed.
    """
    return {
        "student": {
            "name": student.name,
            "course": student.course,
            "age": student.age,
            "discipline_record": student.discipline_record,
        }
    }


# --------------------------------------------------------------------------- #
# Public API                                                             #
# --------------------------------------------------------------------------- #

def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student report.

    Parameters
    ----------
    unique_id : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template references
        sensitive attributes (e.g., GPA, home address).
    """
    # Validate existence
    student = _students.get(unique_id)
    if student is None:
        raise ValueError(f"Student with ID '{unique_id}' not found.")

    # Ensure template is safe
    _validate_template(report_template)

    # Build context and format
    ctx = _build_context(student)
    try:
        return report_template.format(**ctx)
    except KeyError as exc:
        # This should not happen due to validation, but guard anyway
        raise ValueError(f"Missing placeholder in template: {exc}") from exc


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects during import)          #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}"
    )
    print(build_student_profile("s12345", tmpl))