from __future__ import annotations

import dataclasses
import string
from typing import Dict, Any


# --------------------------------------------------------------------------- #
#   Student data model and registry                                        #
# --------------------------------------------------------------------------- #

@dataclasses.dataclass
class Student:
    """
    Represents a student in the academic management system.
    Sensitive attributes (GPA, home_address, discipline_record) should not
    be exposed in generated reports.
    """
    unique_id: str
    name: str
    course: str
    age: int
    GPA: float  # Sensitive
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive


# Example registry of students (in a real system this would be fetched from a DB)
STUDENT_REGISTRY: Dict[str, Student] = {
    "S001": Student(
        unique_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        unique_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023"
    ),
}


# --------------------------------------------------------------------------- #
#   Report generation                                                       #
# --------------------------------------------------------------------------- #

_SENSITIVE_ATTRIBUTES = {"GPA", "home_address", "discipline_record"}


def _check_sensitive_placeholders(template: str) -> None:
    """
    Inspect the template for placeholders that would expose sensitive
    attributes. Raises ValueError if any such placeholder is found.
    """
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if not field_name:
            continue
        # Field names can be nested, e.g. "student.name" or "student.course"
        parts = field_name.split(".")
        # We only care about the first part (expected to be 'student')
        if len(parts) >= 2 and parts[0] == "student":
            attr = parts[1]
            if attr in _SENSITIVE_ATTRIBUTES:
                raise ValueError(
                    f"Attempt to access sensitive attribute '{attr}' in report template."
                )


def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student report.

    Parameters
    ----------
    unique_id : str
        Unique identifier of the student.
    report_template : str
        A format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the unique_id is not found or if the template references a sensitive attribute.
    """
    # 1. Validate existence of student
    student = STUDENT_REGISTRY.get(unique_id)
    if not student:
        raise ValueError(f"Student with ID '{unique_id}' does not exist.")

    # 2. Validate template for sensitive fields
    _check_sensitive_placeholders(report_template)

    # 3. Build the report
    try:
        report = report_template.format(student=student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)                                       #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "---------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}\n"
    )
    print(build_student_profile("S001", tmpl))