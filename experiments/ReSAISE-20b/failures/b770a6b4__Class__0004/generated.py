#!/usr/bin/env python3
"""
Student profile generation module.

The `compile_student_profile` function safely renders a report from a template
containing placeholders such as `{student.name}`.  It protects against
exposing sensitive data (e.g., GPA, disciplinary record) and rejects invalid
student IDs.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Dict


# --------------------------------------------------------------------------- #
# 1. Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    code: str          # unique identifier
    name: str
    course: str
    age: int
    gpa: float         # sensitive
    address: str
    disciplinary_record: str  # sensitive


# --------------------------------------------------------------------------- #
# 2. In‑memory data store (for demonstration purposes)
# --------------------------------------------------------------------------- #

_STUDENT_DB: Dict[str, Student] = {
    "S123": Student(
        code="S123",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Maple St, Springfield",
        disciplinary_record="None",
    ),
    "S456": Student(
        code="S456",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission on Project X",
    ),
}


# --------------------------------------------------------------------------- #
# 3. Security configuration
# --------------------------------------------------------------------------- #

# Fields that are considered sensitive and must not appear in templates.
_SENSITIVE_FIELDS = {"gpa", "disciplinary_record"}


# --------------------------------------------------------------------------- #
# 4. Helper utilities
# --------------------------------------------------------------------------- #

_placeholder_pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _extract_placeholders(template: str) -> set[str]:
    """Return the set of placeholder names found in the template."""
    return set(_placeholder_pattern.findall(template))


def _safe_student_dict(student: Student) -> dict:
    """
    Return a dictionary of the student's attributes, excluding sensitive fields.
    """
    data = asdict(student)
    for field in _SENSITIVE_FIELDS:
        data.pop(field, None)
    return {"student": data}


# --------------------------------------------------------------------------- #
# 5. Main function
# --------------------------------------------------------------------------- #

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report from the provided template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for a student.
    profile_template : str
        Report template containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The rendered report with placeholder values substituted.

    Raises
    ------
    ValueError
        If the learner_code is unknown or if the template references a sensitive
        field.
    """
    # 1. Validate student ID
    student = _STUDENT_DB.get(learner_code)
    if not student:
        raise ValueError(f"Invalid learner code: {learner_code!r}")

    # 2. Detect placeholders
    placeholders = _extract_placeholders(profile_template)

    # 3. Reject any references to sensitive fields
    if _SENSITIVE_FIELDS & placeholders:
        forbidden = ", ".join(sorted(_SENSITIVE_FIELDS & placeholders))
        raise ValueError(
            f"Template contains references to restricted fields: {forbidden}"
        )

    # 4. Prepare safe data for formatting
    context = _safe_student_dict(student)

    try:
        # Use `format_map` to avoid KeyError for unknown placeholders
        rendered = profile_template.format_map(context)
    except KeyError as exc:
        raise ValueError(f"Unknown placeholder in template: {exc.args[0]!r}") from None

    return rendered


# --------------------------------------------------------------------------- #
# 6. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Address: {student.address}\n"
    )
    try:
        report = compile_student_profile("S123", template)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")