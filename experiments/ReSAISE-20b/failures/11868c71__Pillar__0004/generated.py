# -*- coding: utf-8 -*-
"""
Student report builder.

The module defines a simple `Student` data model and a function
``build_student_profile`` that produces a report string from a template.
The function validates the supplied student ID, checks for forbidden
attributes (GPA and home address) in the template, and safely formats
the report.

Security notes:
* The function refuses to expose sensitive attributes even if a user
  tries to reference them in the template.
* It uses ``string.Formatter`` to inspect placeholder names without
  evaluating them, preventing accidental execution of arbitrary code.
* No external resources are opened or closed; the function operates
  purely on in‑memory data, avoiding CWE‑664.
"""

from __future__ import annotations

import string
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
# 1. Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Simple immutable student representation."""
    name: str
    course: str
    age: int
    GPA: float = field(repr=False)          # Sensitive – hidden in repr
    home_address: str = field(repr=False)   # Sensitive – hidden in repr
    discipline_record: str | None = None


# --------------------------------------------------------------------------- #
# 2. In‑memory student database
# --------------------------------------------------------------------------- #

# NOTE: In a real application this would be replaced by a persistent store.
_STUDENT_DB: Dict[str, Student] = {
    "S12345": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple Street, Springfield",
        discipline_record=None,
    ),
    "S67890": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Avenue, Shelbyville",
        discipline_record="Late submission on 2024-01-15",
    ),
}


# --------------------------------------------------------------------------- #
# 3. Report builder
# --------------------------------------------------------------------------- #

def _contains_sensitive_field(template: str) -> bool:
    """
    Inspect the template for references to sensitive student attributes.

    Parameters
    ----------
    template : str
        The format string supplied by the caller.

    Returns
    -------
    bool
        ``True`` if a forbidden attribute is referenced, otherwise ``False``.
    """
    # The safe way to parse format fields without evaluating them
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if field_name:
            # Reject any access to GPA or home_address via the `student` object
            if field_name in {"student.GPA", "student.home_address"}:
                return True
    return False


def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a student report from the supplied template.

    Parameters
    ----------
    unique_id : str
        The unique identifier of a student in the system.
    report_template : str
        A format string containing placeholders such as ``{student.name}``
        or ``{student.course}``.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if the template references a
        sensitive attribute (GPA or home address).
    """
    # 1. Validate the student ID
    if unique_id not in _STUDENT_DB:
        raise ValueError(f"Student ID '{unique_id}' does not exist.")

    # 2. Prevent exposure of sensitive fields
    if _contains_sensitive_field(report_template):
        raise ValueError(
            "Template attempts to access sensitive student data "
            "(GPA or home address)."
        )

    # 3. Safely format the report
    student = _STUDENT_DB[unique_id]
    try:
        report = report_template.format(student=student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# 4. Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "--------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}\n"
        "Notes  : {student.discipline_record}"
    )
    try:
        print(build_student_profile("S12345", template))
    except ValueError as e:
        print(f"Error: {e}")