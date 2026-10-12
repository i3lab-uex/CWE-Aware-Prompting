#!/usr/bin/env python3
"""
Student summary generator.

The module defines a small in‑memory student database and the function
`create_student_summary`, which renders a template string using only
non‑sensitive attributes of the requested student.  Attempts to access
restricted or non‑existent fields raise a `ValueError`.  The function
also validates the student ID.

This implementation is deliberately simple; in a real system the data
source would be external (database, API, etc.) and the security checks
would be more extensive.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Dict


# --------------------------------------------------------------------------- #
# 1. Student data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """
    Represents a student with basic personal and academic information.
    Only the attributes listed in `ALLOWED_ATTRS` are considered safe for
    external exposure.
    """
    stu_id: str          # Unique identifier (e.g. "S12345")
    name: str
    course: str
    age: int
    gpa: float
    # Sensitive / restricted fields (not to be exposed via the template)
    address: str | None = None
    disciplinary_record: str | None = None


# --------------------------------------------------------------------------- #
# 2. In‑memory database (for demonstration purposes)
# --------------------------------------------------------------------------- #

# Simulated student repository
_STUDENT_DB: Dict[str, Student] = {
    "S1001": Student(
        stu_id="S1001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Maple St, Springfield",
        disciplinary_record="None",
    ),
    "S1002": Student(
        stu_id="S1002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        address="456 Oak Ave, Springfield",
        disciplinary_record="Late submission in Assignment 3",
    ),
}


# --------------------------------------------------------------------------- #
# 3. Template rendering
# --------------------------------------------------------------------------- #

# Allowed attributes that may appear in the template.
ALLOWED_ATTRS = {f.name for f in fields(Student) if f.name not in {"address", "disciplinary_record"}}

# Regular expression to find placeholders like `{student.name}`.
_PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")


def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of attribute names referenced in the template.
    Raises ValueError if any restricted or unknown attributes are used.
    """
    placeholders = set(_PLACEHOLDER_RE.findall(template))
    for attr in placeholders:
        if attr not in ALLOWED_ATTRS:
            raise ValueError(f"Access to restricted or unknown attribute '{attr}' is not allowed.")
    return placeholders


def _render_template(template: str, student: Student) -> str:
    """
    Replace `{student.<attr>}` placeholders with the corresponding student
    attribute values.  The function assumes that all placeholders are
    validated beforehand.
    """
    def repl(match: re.Match) -> str:
        attr_name = match.group(1)
        return getattr(student, attr_name)

    return _PLACEHOLDER_RE.sub(repl, template)


# --------------------------------------------------------------------------- #
# 4. Public API
# --------------------------------------------------------------------------- #

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report from the supplied template.

    Parameters
    ----------
    stu_id : str
        The unique student identifier.
    summary_template : str
        A string containing placeholders of the form `{student.<attr>}`.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the student ID is not found, or if the template references a
        restricted or unknown attribute.
    """
    # Validate student ID
    if stu_id not in _STUDENT_DB:
        raise ValueError(f"Student ID '{stu_id}' is invalid or does not exist.")

    student = _STUDENT_DB[stu_id]

    # Validate placeholders
    _extract_placeholders(summary_template)

    # Render the report
    return _render_template(summary_template, student)


# --------------------------------------------------------------------------- #
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}\n"
        "GPA    : {student.gpa:.2f}"
    )
    try:
        report = create_student_summary("S1001", template)
        print(report)
    except ValueError as exc:
        print(f"Error: {exc}")