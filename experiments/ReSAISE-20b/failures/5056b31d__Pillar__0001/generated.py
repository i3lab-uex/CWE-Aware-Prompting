#!/usr/bin/env python3
"""
Student report generator.

This module defines a minimal Student class and a function
`generate_student_report` that produces a report string from a template.
Sensitive fields (home_address, discipline_record) are protected and will
cause the function to raise a ValueError if accessed through the template.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """
    Represents a student's personal and academic information.

    Attributes
    ----------
    student_id : str
        Unique identifier for the student.
    name : str
        Student's full name.
    course : str
        Current course of study.
    age : int
        Student's age.
    gpa : float
        Grade Point Average.
    home_address : str
        Residential address (sensitive).
    discipline_record : str
        Record of disciplinary actions (sensitive).
    """
    student_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)
    discipline_record: str = field(repr=False)


# --------------------------------------------------------------------------- #
# In‑memory registry
# --------------------------------------------------------------------------- #

# Example data; in a real system this would be fetched from a database.
_STUDENT_REGISTRY: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission of Assignment 3"
    ),
}


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _get_student(student_id: str) -> Student:
    """
    Retrieve a student from the registry.

    Parameters
    ----------
    student_id : str
        The unique identifier of the student to fetch.

    Returns
    -------
    Student
        The matching Student instance.

    Raises
    ------
    ValueError
        If the student_id does not exist in the registry.
    """
    try:
        return _STUDENT_REGISTRY[student_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{student_id}' not found.") from exc


# --------------------------------------------------------------------------- #
# Main functionality
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"home_address", "discipline_record"}
_TEMPLATE_VAR_PATTERN = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")


def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report string based on the provided template.

    The function substitutes placeholders of the form `{student.<field>}`
    with the corresponding attribute from the Student object. If a
    placeholder references a sensitive field (e.g., `home_address` or
    `discipline_record`) the function raises a ValueError to prevent
    accidental leakage of confidential information.

    Parameters
    ----------
    student_id : str
        The unique identifier for the student.
    template : str
        The template string containing placeholders.

    Returns
    -------
    str
        The fully rendered report string.

    Raises
    ------
    ValueError
        If the student_id is invalid, or if the template references a
        sensitive field.
    """
    # Retrieve student safely
    student = _get_student(student_id)

    # Detect all placeholders in the template
    placeholders = set(match.group(1) for match in _TEMPLATE_VAR_PATTERN.finditer(template))

    # Check for disallowed (sensitive) fields
    if placeholders & _SENSITIVE_FIELDS:
        sensitive = placeholders & _SENSITIVE_FIELDS
        raise ValueError(
            f"Access to sensitive field(s) prohibited: {', '.join(sorted(sensitive))}"
        )

    # Build a mapping for formatting
    student_dict: Dict[str, Any] = {
        key: getattr(student, key) for key in placeholders
    }

    try:
        report = template.format_map(student_dict)
    except KeyError as exc:
        # This should not happen because we filtered placeholders,
        # but guard against missing attributes.
        raise ValueError(f"Missing attribute for placeholder: {exc}") from exc
    except Exception as exc:
        # Generic catch to avoid leaking internal details
        raise ValueError(f"Failed to render template: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Student Report for {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
    )
    print(generate_student_report("S001", tmpl))