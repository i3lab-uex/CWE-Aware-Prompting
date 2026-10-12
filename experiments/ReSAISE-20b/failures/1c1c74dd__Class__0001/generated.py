#!/usr/bin/env python3
"""
A small module that generates a student report from a template.

The implementation protects against accidental leakage of sensitive data
such as GPA or home address.  If the template contains any references to
those attributes, a ValueError is raised.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student in the academic system."""
    name: str
    course: str
    age: int
    GPA: float          # Sensitive
    home_address: str   # Sensitive
    discipline_record: str


# --------------------------------------------------------------------------- #
# In‑memory student database (for demonstration purposes)
# --------------------------------------------------------------------------- #

_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2024-01-15"
    ),
    # Add more students as needed
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive attributes.
    Allowed placeholders are limited to name, course, age, and discipline_record.

    Raises:
        ValueError: If a forbidden attribute is detected.
    """
    # Extract all attribute references of the form {student.<attr>}
    attr_pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    for match in attr_pattern.finditer(template):
        attr = match.group(1)
        if attr in {"GPA", "home_address"}:
            raise ValueError(
                f"Template contains sensitive attribute '{attr}'. "
                "Access to this data is not permitted."
            )


def _build_safe_student_context(student: Student) -> Dict[str, Any]:
    """
    Build a dictionary containing only non‑sensitive attributes of the student.
    The returned mapping can be used directly with str.format().
    """
    allowed_attrs = {"name", "course", "age", "discipline_record"}
    safe_dict: Dict[str, Any] = {}
    for field_name in allowed_attrs:
        safe_dict[field_name] = getattr(student, field_name)
    # Wrap into a simple namespace for attribute access in the template
    return {"student": type("StudentNamespace", (), safe_dict)()}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a formatted report for the student identified by ``stu_id`` using
    ``custom_template``.

    Args:
        stu_id: Unique identifier of the student.
        custom_template: A format string that may contain placeholders such as
                         '{student.name}', '{student.course}', etc.

    Returns:
        A string containing the formatted report.

    Raises:
        ValueError: If ``stu_id`` does not exist or if the template tries to
                    access sensitive data.
    """
    # Retrieve student record
    student = _STUDENT_DB.get(stu_id)
    if student is None:
        raise ValueError(f"Student ID '{stu_id}' not found.")

    # Validate the template for sensitive attributes
    _validate_template(custom_template)

    # Build safe context and format the string
    context = _build_safe_student_context(student)
    try:
        report = custom_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Error formatting template: {exc}") from None

    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "--------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}"
    )
    try:
        print(produce_student_report("S001", template))
    except ValueError as e:
        print(f"Error: {e}")