#!/usr/bin/env python3
"""
Student report generator.

This module defines a small in‑memory database of students and provides the
`produce_student_report` function which renders a report for a given student
ID using a user supplied template.

Security constraints:
* The function refuses to expose sensitive attributes (GPA, home_address).
* It validates that the supplied template does not reference any of those
  attributes.
* If the student ID is unknown, a ValueError is raised.

The implementation deliberately avoids external dependencies and uses only
Python's standard library.
"""

import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Student data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    stu_id: str
    name: str
    course: str
    age: int
    GPA: float = field(repr=False)           # sensitive – omitted from repr
    home_address: str = field(repr=False)   # sensitive – omitted from repr

# --------------------------------------------------------------------------- #
# 2. In‑memory database (for demonstration purposes)
# --------------------------------------------------------------------------- #

_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
    ),
}

# --------------------------------------------------------------------------- #
# 3. Template validation helpers
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"GPA", "home_address"}
_PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive fields.
    Raises ValueError if a forbidden field is detected.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        attr = match.group(1)
        if attr in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{attr}' is forbidden.")
    # Optionally, we could also validate that all referenced attributes exist
    # on the Student class; omitted for brevity.

# --------------------------------------------------------------------------- #
# 4. Report generation
# --------------------------------------------------------------------------- #

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Render a student report using the supplied template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    custom_template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID is unknown, or if the template attempts to access a
        sensitive attribute.
    """
    # Validate template before any data lookup
    _validate_template(custom_template)

    student = _STUDENT_DB.get(stu_id)
    if student is None:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # Prepare a namespace for formatting
    context = {"student": student}

    try:
        report = custom_template.format(**context)
    except KeyError as exc:
        # This should not happen due to the earlier validation,
        # but we guard against it anyway.
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return report

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
    )
    print(produce_student_report("S001", template))