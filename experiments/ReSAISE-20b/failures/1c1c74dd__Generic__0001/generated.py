#!/usr/bin/env python3
"""
Student report generator.

The module defines a small in‑memory student store and a function that
produces a formatted report from a user supplied template.  The function
rejects any attempt to expose sensitive data such as GPA or home address.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Dict


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str


# --------------------------------------------------------------------------- #
# In‑memory store (stub for a real database)
# --------------------------------------------------------------------------- #

# Example data – in a real system this would be fetched from a DB.
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission on 2023-03-15"
    ),
}


# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #

SENSITIVE_FIELDS = {"GPA", "home_address"}

def _check_sensitive_placeholders(template: str) -> None:
    """
    Ensure that the template does not reference any sensitive fields.
    Raises ValueError if a forbidden placeholder is found.
    """
    # Find all placeholders of the form {field} or {object.field}
    placeholders = re.findall(r"{([^{}]+)}", template)
    for placeholder in placeholders:
        # Handle nested attributes like 'student.GPA'
        parts = placeholder.split(".")
        field_name = parts[-1]
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{field_name}' is prohibited.")


def _get_student(stu_id: str) -> Student:
    """
    Retrieve a student from the in‑memory store.
    Raises ValueError if the ID is unknown.
    """
    student = STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")
    return student


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a formatted student report.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        A format string containing placeholders like '{student.name}' or
        simply '{name}'.  The template must not reference sensitive data.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID is unknown or if a sensitive attribute is requested.
    """
    # Validate template first to avoid leaking data
    _check_sensitive_placeholders(custom_template)

    # Retrieve the student record
    student = _get_student(stu_id)

    # Prepare a namespace for formatting.
    # We expose both the student object and its individual attributes
    # to allow flexible placeholder usage.
    namespace = {"student": student, **asdict(student)}

    # Perform formatting safely
    try:
        report = custom_template.format(**namespace)
    except KeyError as exc:
        # Provide a clear error message if an unknown placeholder is used
        raise ValueError(f"Unknown placeholder in template: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "--------------\n"
        "Name   : {student.name}\n"
        "Course : {course}\n"
        "Age    : {age}\n"
        "Record : {discipline_record}"
    )
    print(produce_student_report("S001", template))