#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that provides a function to build a student profile report
without exposing sensitive information.
"""

from dataclasses import dataclass, field
from typing import Dict


# ----------------------------------------------------------------------
# Student data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """
    Represents a student with several attributes. Only non‑sensitive
    fields should be exposed through the report template.
    """
    name: str
    course: str
    age: int
    GPA: float = field(repr=False)          # Sensitive
    home_address: str = field(repr=False)   # Sensitive
    discipline_record: list[str] = field(default_factory=list)


# ----------------------------------------------------------------------
# In‑memory student registry (mocked for demonstration)
# ----------------------------------------------------------------------
_STUDENT_REGISTRY: Dict[str, Student] = {
    "stu001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record=[],
    ),
    "stu002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record=["Late submission"],
    ),
}


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _contains_sensitive_placeholder(template: str) -> bool:
    """
    Detects whether the template references any sensitive student attributes.
    Sensitive fields: GPA, home_address
    """
    sensitive_keys = {"GPA", "home_address"}
    # Very simple placeholder extraction: look for `{student.<field>}`
    for key in sensitive_keys:
        if f"{{student.{key}}}" in template or f"{{student.{key.lower()}}}" in template:
            return True
    return False


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Builds a formatted student profile report based on the supplied template.

    Parameters
    ----------
    unique_id : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders such as `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the unique_id does not exist in the registry or if the template
        attempts to access sensitive attributes (GPA, home_address).
    """
    # Validate existence of student
    if unique_id not in _STUDENT_REGISTRY:
        raise ValueError(f"Student ID '{unique_id}' does not exist.")

    # Protect against leaking sensitive data
    if _contains_sensitive_placeholder(report_template):
        raise ValueError("Template references sensitive student attributes.")

    # Retrieve the student object
    student = _STUDENT_REGISTRY[unique_id]

    # Prepare a namespace for formatting that only exposes safe fields
    safe_attrs = {
        "name": student.name,
        "course": student.course,
        "age": student.age,
        # No GPA or home_address
    }

    # Build the report using a safe format string
    try:
        report = report_template.format(student=safe_attrs)
    except KeyError as exc:
        # The template references an unknown placeholder
        raise ValueError(f"Invalid placeholder in template: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = "Student Name: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(build_student_profile("stu001", template))