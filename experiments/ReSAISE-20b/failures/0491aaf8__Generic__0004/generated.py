#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create_student_summary

Generate a student report from a format string.
Sensitive attributes (GPA, home_address) cannot be accessed.

Author: OpenAI
"""

import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
# Dummy in-memory database of students. In a real system this would be
# replaced by a proper persistence layer.
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Student:
    id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str


# Example data (normally this would come from a database)
_STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Townsville",
        discipline_record="None"
    ),
    "S002": Student(
        id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Villagetown",
        discipline_record="Late submission"
    ),
}


# --------------------------------------------------------------------------- #
# Helper: Safe proxy for Student that blocks sensitive attributes
# --------------------------------------------------------------------------- #
_SENSITIVE_ATTRS = {"GPA", "home_address"}


class _SafeStudent:
    """
    Wraps a Student instance and allows access only to non-sensitive
    attributes. Any attempt to read a sensitive attribute raises ValueError.
    """

    def __init__(self, student: Student):
        self._student = student

    def __getattr__(self, item):
        if item in _SENSITIVE_ATTRS:
            raise ValueError(f"Access to sensitive attribute '{item}' is prohibited.")
        # Delegate to the underlying Student
        return getattr(self._student, item)

    def __repr__(self):
        # Avoid leaking sensitive data in representation
        attrs = {f.name: getattr(self, f.name) for f in fields(Student)
                 if f.name not in _SENSITIVE_ATTRS}
        return f"_SafeStudent({attrs})"


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a formatted student report.

    Parameters
    ----------
    id : str
        Unique identifier for the student.
    format_string : str
        A string containing placeholders of the form {student.<attr>}.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student id is not found or if a sensitive attribute is accessed.
    """
    # 1. Retrieve the student
    try:
        student = _STUDENTS_DB[id]
    except KeyError as exc:
        raise ValueError(f"Student id '{id}' does not exist.") from exc

    # 2. Scan format string for placeholders
    # Regex finds patterns like {student.name}
    placeholder_pattern = re.compile(r"\{(?P<obj>[^.]+)\.(?P<attr>[^}]+)\}")
    for match in placeholder_pattern.finditer(format_string):
        obj_name = match.group("obj")
        attr_name = match.group("attr")

        # Ensure the placeholder refers to 'student'
        if obj_name != "student":
            raise ValueError(f"Unsupported placeholder object '{obj_name}'. "
                             f"Only 'student' is allowed.")

        # Disallow sensitive attributes
        if attr_name in _SENSITIVE_ATTRS:
            raise ValueError(f"Access to sensitive attribute '{attr_name}' is prohibited.")

    # 3. Create a safe proxy
    safe_student = _SafeStudent(student)

    # 4. Format the string
    try:
        report = format_string.format(student=safe_student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format string: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}"
    )
    print(create_student_summary("S001", template))