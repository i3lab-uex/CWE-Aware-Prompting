from __future__ import annotations

import dataclasses
import string
from typing import Dict, Any


@dataclasses.dataclass(frozen=True)
class Student:
    """Represents a student in the academic management system."""
    unique_id: str
    name: str
    course: str
    age: int
    GPA: float  # Sensitive
    home_address: str  # Sensitive
    discipline_record: str


# In‑memory data store (in a real system this would be a database query)
STUDENT_STORE: Dict[str, Student] = {
    "S001": Student(
        unique_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "S002": Student(
        unique_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late for class",
    ),
}


def _has_sensitive_placeholder(template: str) -> bool:
    """
    Detect if the template contains placeholders that refer to sensitive
    attributes (GPA or home_address).  The check is performed using the
    string.Formatter parser which reliably extracts field names.
    """
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if field_name:
            # Handle nested attributes like student.GPA
            if "." in field_name:
                _, attr = field_name.split(".", 1)
            else:
                attr = field_name
            if attr in {"GPA", "home_address"}:
                return True
    return False


def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student profile based on the provided template.

    Parameters
    ----------
    unique_id : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders that map to student attributes,
        e.g. "{student.name} is enrolled in {student.course}."

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the unique_id does not correspond to a known student, or if the
        template attempts to access sensitive attributes such as GPA or home address.
    """
    # Validate existence of student
    student = STUDENT_STORE.get(unique_id)
    if student is None:
        raise ValueError(f"Student with ID '{unique_id}' does not exist.")

    # Check for sensitive placeholders
    if _has_sensitive_placeholder(report_template):
        raise ValueError("Template contains access to sensitive student data (GPA or home address).")

    # Build a simple namespace for formatting
    # The template is expected to use 'student' as the root object.
    namespace: Dict[str, Any] = {"student": student}

    try:
        formatted_report = report_template.format(**namespace)
    except KeyError as exc:
        # Provide a clearer error message
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return formatted_report


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     template = "Student {student.name}, aged {student.age}, is enrolled in {student.course}."
#     print(build_student_profile("S001", template))