#!/usr/bin/env python3
"""
Module: student_report

Provides a single function `produce_student_report` that generates a
student report from a format string while protecting sensitive data.
"""

from __future__ import annotations

import dataclasses
import re
from typing import Dict, Any


# --------------------------------------------------------------------------- #
#  Data structures
# --------------------------------------------------------------------------- #

@dataclasses.dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str


# In‑memory "database" of students for demonstration purposes.
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2023-04-12",
    ),
}


# --------------------------------------------------------------------------- #
#  Helper functions
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"GPA", "home_address"}


def _extract_placeholders(template: str) -> set[str]:
    """
    Extracts all placeholders from a format string.

    Returns a set of placeholder names, e.g. {"student.name", "student.course"}.
    """
    placeholders = set()
    # Use a regex that matches {name} patterns, including nested attributes.
    pattern = re.compile(r"\{([^{}]+)\}")
    for match in pattern.finditer(template):
        placeholders.add(match.group(1).strip())
    return placeholders


def _validate_placeholders(placeholders: set[str]) -> None:
    """
    Raises ValueError if any placeholder refers to a sensitive field.
    """
    for ph in placeholders:
        # Split by '.' and check each part if it matches a sensitive field.
        parts = ph.split(".")
        # We only care about the attribute part after 'student.'
        if len(parts) >= 2 and parts[0] == "student":
            attr = parts[-1]
            if attr in _SENSITIVE_FIELDS:
                raise ValueError(
                    f"Access to sensitive attribute '{attr}' is prohibited."
                )


# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a student report using the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        Format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if a placeholder accesses a
        sensitive attribute (GPA, home_address).
    """
    # Validate student existence.
    student = _STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # Validate placeholders for sensitive data.
    placeholders = _extract_placeholders(custom_template)
    _validate_placeholders(placeholders)

    # Build a mapping for formatting.
    context: Dict[str, Any] = {"student": student}

    try:
        report = custom_template.format(**context)
    except KeyError as exc:
        # In case the template refers to an attribute that doesn't exist.
        raise ValueError(f"Invalid placeholder: {exc}") from exc
    except Exception as exc:
        # Catch any other formatting errors.
        raise ValueError(f"Error while generating report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}"
    )
    print(produce_student_report("S001", tmpl))