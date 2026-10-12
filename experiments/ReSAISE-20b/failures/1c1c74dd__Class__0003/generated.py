# -*- coding: utf-8 -*-
"""
Utility for generating a student report with restricted data exposure.
"""

from dataclasses import dataclass
import re
from typing import Dict

# --------------------------------------------------------------------
# Sample data model (in a real system this would be imported from elsewhere)
# --------------------------------------------------------------------

@dataclass
class Student:
    """Represents a student with various attributes."""
    name: str
    course: str
    age: int
    gpa: float          # Sensitive
    home_address: str   # Sensitive
    discipline_record: str


# --------------------------------------------------------------------
# In-memory student database (for demonstration purposes)
# --------------------------------------------------------------------

_student_db: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023"
    ),
}


# --------------------------------------------------------------------
# Core functionality
# --------------------------------------------------------------------

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generates a student report using the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for the student.
    custom_template : str
        Format string containing placeholders (e.g., '{student.name}').

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID is not found, or if the template attempts to access
        sensitive attributes (GPA or home address).
    """

    # Validate student existence
    if stu_id not in _student_db:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    student = _student_db[stu_id]

    # Detect attempts to access sensitive fields
    # Allowed placeholders are: name, course, age, discipline_record
    allowed_fields = {"name", "course", "age", "discipline_record"}
    # Find all placeholders in the template
    placeholders = re.findall(r"{[^}]+}", custom_template)

    for placeholder in placeholders:
        # Normalize: strip braces and split by '.' if nested
        parts = placeholder.strip("{}").split(".")
        # We expect exactly 'student' followed by a field name
        if len(parts) != 2 or parts[0] != "student":
            raise ValueError(f"Invalid placeholder format: {placeholder}")

        field = parts[1]
        if field not in allowed_fields:
            raise ValueError(
                f"Access to sensitive attribute '{field}' is not permitted."
            )

    # Prepare the namespace for formatting
    context = {"student": student}

    try:
        report = custom_template.format(**context)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Template formatting failed: {exc}") from exc

    return report


# --------------------------------------------------------------------
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}"
    )
    print(produce_student_report("S001", template))