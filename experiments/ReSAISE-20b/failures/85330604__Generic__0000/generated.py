#!/usr/bin/env python3
"""
Student report generator.

The module defines a simple in‑memory student database and provides the
`create_student_report` function which builds a report from a template
string while enforcing strict data‑privacy rules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Student data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    name: str
    course: str
    age: int
    gpa: float
    # Sensitive data – must never be exposed in a report
    home_address: str = field(repr=False, compare=False)
    discipline_record: str = field(repr=False, compare=False)


# --------------------------------------------------------------------------- #
# 2. In‑memory student database (for demo purposes)
# --------------------------------------------------------------------------- #

_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in Math 101"
    ),
}


# --------------------------------------------------------------------------- #
# 3. Report generation logic
# --------------------------------------------------------------------------- #

_ALLOWED_ATTRS = {"name", "course", "age", "gpa"}
_FORBIDDEN_PATTERN = re.compile(r"\{student\.([^\}]+)\}")

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Create a personalized report for the student identified by `stu_id`.

    Parameters
    ----------
    stu_id : str
        The unique identifier of the student.
    report_template : str
        A format string that may contain placeholders such as
        `{student.name}`, `{student.course}`, etc.

    Returns
    -------
    str
        The formatted report string with placeholders replaced by the
        corresponding student attributes.

    Raises
    ------
    ValueError
        If `stu_id` is not found in the system or if the template attempts to
        access a forbidden attribute (e.g., home_address, discipline_record).
    """
    # 1. Retrieve the student record
    try:
        student = _STUDENT_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' does not exist.") from exc

    # 2. Validate that the template does not reference forbidden data
    for match in _FORBIDDEN_PATTERN.finditer(report_template):
        attr_name = match.group(1).strip()
        if attr_name not in _ALLOWED_ATTRS:
            raise ValueError(
                f"Unauthorized access to sensitive data: '{attr_name}'. "
                "Only name, course, age, and gpa are permitted."
            )

    # 3. Render the template
    try:
        report = report_template.format(student=student)
    except Exception as exc:  # pragma: no cover
        # Any formatting error is treated as a misuse of the template.
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# 4. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
    )
    print(create_student_report("S001", template))