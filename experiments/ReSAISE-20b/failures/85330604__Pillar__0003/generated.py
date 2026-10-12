# -*- coding: utf-8 -*-
"""
Student report generator.

The module contains a minimal in‑memory representation of students and
provides the ``create_student_report`` function which safely renders a
report from a user supplied template.  Only non‑sensitive attributes are
exposed and any attempt to reference disallowed data raises a
``ValueError``.

Author: ChatGPT
"""

from __future__ import annotations

import string
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
#  Data model – in‑memory student repository (mocked for this example)
# --------------------------------------------------------------------------- #

@dataclass
class Student:
    """Represents a student in the system."""
    stu_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)          # Sensitive
    discipline_record: str = field(repr=False)     # Sensitive


# Mock database (student id -> Student)
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023"
    ),
}


# --------------------------------------------------------------------------- #
#  Helper utilities
# --------------------------------------------------------------------------- #

_ALLOWED_ATTRS = {"name", "course", "age", "gpa"}


def _extract_fields(template: str) -> set[str]:
    """
    Extract all placeholder field names from the template.
    """
    return {
        field
        for _, field, _, _ in string.Formatter().parse(template)
        if field is not None and field != ""
    }


def _validate_template_fields(fields: set[str]) -> None:
    """
    Ensure that all placeholders refer to allowed student attributes.
    Raises ValueError if any disallowed field is found.
    """
    for f in fields:
        # All placeholders must start with 'student.'
        if not f.startswith("student."):
            raise ValueError(f"Unauthorized placeholder '{f}'. Only 'student.*' is allowed.")
        attr = f.split(".", 1)[1]
        if attr not in _ALLOWED_ATTRS:
            raise ValueError(f"Access to sensitive attribute '{attr}' is forbidden.")


def _build_context(student: Student) -> dict:
    """
    Build a dictionary of allowed attributes for formatting.
    """
    return {attr: getattr(student, attr) for attr in _ALLOWED_ATTRS}


# --------------------------------------------------------------------------- #
#  Main API
# --------------------------------------------------------------------------- #

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report from the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    report_template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student id does not exist, or if the template contains
        disallowed placeholders.
    """
    # 1. Retrieve student (raise if not found)
    try:
        student = _STUDENT_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student with id '{stu_id}' does not exist.") from exc

    # 2. Validate template placeholders
    fields = _extract_fields(report_template)
    _validate_template_fields(fields)

    # 3. Prepare context and sanitize template
    context = _build_context(student)
    sanitized_template = report_template.replace("student.", "")

    # 4. Render the report
    try:
        report = sanitized_template.format(**context)
    except KeyError as exc:
        # This should not happen because we validated the fields
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#  Example usage (commented out – for illustration only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tpl = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
    )
    print(create_student_report("S001", tpl))