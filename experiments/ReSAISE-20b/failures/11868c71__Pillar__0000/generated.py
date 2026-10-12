# -*- coding: utf-8 -*-
"""
Student profile report generator.

The module defines a simple in‑memory student registry and provides the
`build_student_profile` function which formats a report from a template.
Sensitive attributes (GPA, home_address) are disallowed in the template
and will raise a ValueError if referenced.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
#  Data model                                                                #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student with non‑sensitive attributes."""
    unique_id: str
    name: str
    course: str
    age: int
    # Sensitive data – must not be exposed via templates
    GPA: float = field(repr=False)
    home_address: str = field(repr=False)


# --------------------------------------------------------------------------- #
#  In‑memory registry                                                       #
# --------------------------------------------------------------------------- #

_student_registry: Dict[str, Student] = {}


def register_student(student: Student) -> None:
    """Adds a student to the registry."""
    _student_registry[student.unique_id] = student


def get_student_by_id(unique_id: str) -> Student:
    """Retrieve a student by unique ID or raise ValueError."""
    try:
        return _student_registry[unique_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{unique_id}' does not exist") from exc


# --------------------------------------------------------------------------- #
#  Template validation                                                      #
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"GPA", "home_address"}

# Regex to capture attribute access in the form `{student.<field>}`
_ATTR_REGEX = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")


def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference any sensitive fields.
    Raises ValueError if a forbidden field is found.
    """
    for match in _ATTR_REGEX.finditer(template):
        field_name = match.group(1)
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(f"Template references forbidden attribute '{field_name}'")


# --------------------------------------------------------------------------- #
#  Main API                                                                 #
# --------------------------------------------------------------------------- #

def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Build a formatted student profile from the provided template.

    Parameters
    ----------
    unique_id : str
        Unique identifier for the student.
    report_template : str
        Format string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template references a
        sensitive attribute.
    """
    # 1. Validate template for forbidden fields
    _validate_template(report_template)

    # 2. Retrieve the student (raises ValueError if not found)
    student = get_student_by_id(unique_id)

    # 3. Safely format the template
    try:
        report = report_template.format(student=student)
    except Exception as exc:  # pragma: no cover
        # Catch any formatting errors and surface them clearly
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#  Example usage (commented out – remove for production)                     #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Create and register a sample student
    s = Student(
        unique_id="S12345",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.9,
        home_address="123 Maple St, Springfield",
    )
    register_student(s)

    # Define a template
    tmpl = (
        "Student Report\n"
        "--------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
    )

    # Build the report
    print(build_student_profile("S12345", tmpl))