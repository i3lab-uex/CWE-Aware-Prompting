# -*- coding: utf-8 -*-
"""
Student profile compilation module.

This module defines a simple in‑memory representation of student data and
provides the function `compile_student_profile` that renders a report
based on a template string containing placeholders such as
'{student.name}' or '{student.course}'.  The function guards against
accessing restricted attributes (e.g. disciplinary records) and
raises `ValueError` for invalid student identifiers or attempts to
expose sensitive data.

The module also demonstrates proper resource handling by using a context
manager (`StudentDataSource`) that ensures the data source is closed
once it is no longer needed, thereby mitigating CWE‑664.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass, field
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    code: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    # Sensitive data – should never be exposed via the template.
    disciplinary_record: Dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------------------------------- #
# In‑memory data source with context manager
# --------------------------------------------------------------------------- #

class StudentDataSource:
    """
    A mock data source that mimics a database connection.
    It implements the context‑manager protocol to ensure proper
    acquisition and release of resources (CWE‑664 compliance).
    """

    def __init__(self):
        self._students: Dict[str, Student] = {}
        self._closed: bool = False

    def add_student(self, student: Student) -> None:
        if self._closed:
            raise RuntimeError("Cannot add to a closed data source")
        self._students[student.code] = student

    def get_student(self, code: str) -> Student:
        if self._closed:
            raise RuntimeError("Cannot query a closed data source")
        try:
            return self._students[code]
        except KeyError as exc:
            raise ValueError(f"Student with code '{code}' not found") from exc

    # Context‑manager protocol
    def __enter__(self) -> "StudentDataSource":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._closed = True
        # In a real implementation, close DB connections here.


# --------------------------------------------------------------------------- #
# Global data source instance (for demo purposes)
# --------------------------------------------------------------------------- #

_GLOBAL_DATA_SOURCE = StudentDataSource()
# Populate with sample data
_GLOBAL_DATA_SOURCE.add_student(
    Student(
        code="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record={"probation": False},
    )
)
_GLOBAL_DATA_SOURCE.add_student(
    Student(
        code="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record={"probation": True},
    )
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Render a student report based on the supplied template.

    Parameters
    ----------
    learner_code : str
        Unique identifier of the student.
    profile_template : str
        Template containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the student ID is invalid or if the template attempts to access a
        restricted attribute (e.g. 'disciplinary_record').
    """
    # Restrict access to sensitive fields
    RESTRICTED_ATTRS = {"disciplinary_record"}

    # Acquire the student data safely using a context manager
    with _GLOBAL_DATA_SOURCE as ds:
        student = ds.get_student(learner_code)

    # Prepare a namespace for formatting
    safe_attrs: Dict[str, Any] = {
        k: getattr(student, k)
        for k in student.__dataclass_fields__
        if k not in RESTRICTED_ATTRS
    }

    # Detect prohibited placeholders early
    placeholder_names = _extract_placeholder_names(profile_template)
    for name in placeholder_names:
        if "." in name:
            obj, attr = name.split(".", 1)
            if obj != "student":
                raise ValueError(f"Unsupported placeholder '{{{name}}}'")
            if attr in RESTRICTED_ATTRS:
                raise ValueError(
                    f"Attempt to access restricted attribute '{attr}'"
                )
        else:
            # If the placeholder is not of form student.attr, reject
            raise ValueError(f"Unsupported placeholder '{{{name}}}'")

    try:
        report = profile_template.format(student=student)
    except AttributeError as exc:
        # Catch formatting errors due to missing attributes
        raise ValueError("Template contains invalid placeholder") from exc

    return report


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _extract_placeholder_names(template: str) -> set[str]:
    """
    Extract all placeholder names from a format string.

    This function parses the template using Python's
    `string.Formatter` to identify all field names.
    """
    import string

    formatter = string.Formatter()
    return {fname for _, fname, _, _ in formatter.parse(template) if fname}


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}"
    )
    print(compile_student_profile("S001", tmpl))