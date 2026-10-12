# -*- coding: utf-8 -*-
"""
Utility for generating a student report from a format string.

The function `create_student_summary` safely formats the provided template
using only non‑sensitive attributes of a Student instance.  It validates
the student ID, checks the template for forbidden fields (GPA and home_address),
and raises a ValueError if any violation is detected.
"""

from __future__ import annotations

import string
from dataclasses import dataclass, field
from typing import Dict


# --------------------------------------------------------------------------- #
#  Data model – normally provided by the system.  A minimal stub is supplied
#  here for illustration and unit testing.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Student:
    """A simple immutable representation of a student."""
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)          # Sensitive – should never be exposed
    home_address: str = field(repr=False)   # Sensitive – should never be exposed


# --------------------------------------------------------------------------- #
#  In‑memory store for demonstration purposes.  In a real system this would
#  be replaced by a database lookup or similar persistent store.
# --------------------------------------------------------------------------- #
STUDENT_STORE: Dict[str, Student] = {
    "S001": Student(name="Alice Smith", course="Computer Science", age=20,
                     gpa=3.8, home_address="123 Main St"),
    "S002": Student(name="Bob Jones", course="Mathematics", age=22,
                     gpa=3.6, home_address="456 Oak Ave"),
}


# --------------------------------------------------------------------------- #
#  Core function
# --------------------------------------------------------------------------- #
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report based on the supplied format string.

    Parameters
    ----------
    id : str
        Unique identifier for a student.
    format_string : str
        Template containing placeholders such as `{student.name}` or
        `{student.course}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if a sensitive attribute is
        referenced in the format string.
    """
    # --------------------------------------------------------------------- #
    # 1. Retrieve the student instance – raise if not found.
    # --------------------------------------------------------------------- #
    try:
        student = STUDENT_STORE[id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{id}' does not exist.") from exc

    # --------------------------------------------------------------------- #
    # 2. Inspect the format string for forbidden fields.
    # --------------------------------------------------------------------- #
    formatter = string.Formatter()
    forbidden_attrs = {"gpa", "home_address"}

    for _, field_name, *_ in formatter.parse(format_string):
        if not field_name:
            continue  # Empty placeholder – ignore

        # Only consider attributes accessed on the `student` object.
        # The format string may contain nested fields; we only care about
        # top‑level attributes of `student`.
        if field_name.startswith("student."):
            attr = field_name.split(".", 1)[1]
            if attr in forbidden_attrs:
                raise ValueError(
                    f"Access to sensitive attribute '{attr}' is prohibited."
                )

    # --------------------------------------------------------------------- #
    # 3. Perform the formatting.
    # --------------------------------------------------------------------- #
    try:
        report = format_string.format(student=student)
    except Exception as exc:  # Catch any formatting errors
        raise ValueError(f"Invalid format string: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test):
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     template = "Student: {student.name}, Course: {student.course}, Age: {student.age}"
#     print(create_student_summary("S001", template))