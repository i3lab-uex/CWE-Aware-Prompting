# -*- coding: utf-8 -*-
"""
Student report generator.

The module defines a simple in‑memory data store for `Student` objects
and a function ``generate_student_report`` that renders a report based
on a user supplied template.  The implementation is deliberately
resource‑safe: database connections are never left open and any attempt
to expose sensitive data raises ``ValueError``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from contextlib import contextmanager
from typing import Dict

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Student:
    """
    Immutable representation of a student.
    Sensitive fields are marked with ``_sensitive`` suffix to make
    accidental exposure obvious.
    """
    student_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str = field(repr=False)
    discipline_record: str = field(repr=False)


# ----------------------------------------------------------------------
# In‑memory "database"
# ----------------------------------------------------------------------


class StudentRepository:
    """
    A very small repository that mimics a database connection.
    The connection is opened and closed via a context manager
    to prevent resource leaks (CWE‑664).
    """

    def __init__(self) -> None:
        self._students: Dict[str, Student] = {}

    def add(self, student: Student) -> None:
        self._students[student.student_id] = student

    @contextmanager
    def get(self, student_id: str):
        """
        Context manager that yields a Student object and ensures the
        repository is closed immediately after use.
        """
        # In real life this would open a DB connection here
        student = self._students.get(student_id)
        if not student:
            raise ValueError(f"Student with id {student_id!r} not found")
        try:
            yield student
        finally:
            # In real life this would close the DB connection here
            pass


# ----------------------------------------------------------------------
# Report generator
# ----------------------------------------------------------------------


# Regular expression to find all placeholders in the template.
_PLACEHOLDER_RE = re.compile(r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

# Allowed attributes that can be used in a template.
_ALLOWED_FIELDS = {
    "name",
    "course",
    "age",
    "GPA",
}


def generate_student_report(student_id: str, template: str) -> str:
    """
    Render a student report based on the supplied ``template``.

    Parameters
    ----------
    student_id : str
        Unique identifier of the student to fetch.
    template : str
        Template string containing placeholders like ``{name}`` or
        ``{course}``.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the student cannot be found, or if the template contains a
        placeholder that is not in :data:`_ALLOWED_FIELDS` (i.e. it would
        expose sensitive data).
    """
    # Validate template placeholders first.
    for placeholder in _PLACEHOLDER_RE.findall(template):
        if placeholder not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Template contains disallowed field: {placeholder!r}"
            )

    # Fetch the student within a context manager to avoid leaking resources.
    repo = StudentRepository()
    # For demonstration purposes, we prepopulate the repository.
    # In a real application this would be loaded from persistent storage.
    if not repo._students:
        repo.add(
            Student(
                student_id="S001",
                name="Alice Smith",
                course="Computer Science",
                age=20,
                GPA=3.8,
                home_address="123 Maple St, Springfield",
                discipline_record="None",
            )
        )

    with repo.get(student_id) as student:
        # Build a mapping of allowed fields for formatting.
        context = {
            field: getattr(student, field)
            for field in _ALLOWED_FIELDS
        }
        try:
            report = template.format(**context)
        except KeyError as exc:
            # This should not happen because we filtered placeholders,
            # but guard against it anyway.
            raise ValueError(f"Missing data for placeholder {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------


if __name__ == "__main__":
    tmpl = "Student {name} is enrolled in {course}. GPA: {GPA}"
    print(generate_student_report("S001", tmpl))