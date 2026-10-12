import re
from dataclasses import dataclass, fields
from typing import Dict

# -------------------- Student model & storage ---------------------------------

@dataclass(frozen=True)
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str          # Sensitive
    discipline_record: str     # Sensitive

# Mock database of students
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of Assignment 3"
    ),
}

# -------------------- Report generation -------------------------------------

ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Args:
        student_number: Unique identifier of the student.
        report_template: Format string containing placeholders such as
                         '{student.name}', '{student.course}', etc.

    Returns:
        A formatted string with the student's data inserted into the template.

    Raises:
        ValueError: If the student_number is not found, or if a sensitive
                    field (home_address, discipline_record) is requested in the
                    template.
    """
    # Retrieve student record
    student = STUDENT_DB.get(student_number)
    if not student:
        raise ValueError(f"Student with number {student_number} does not exist.")

    # Extract placeholders from the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # Build a mapping for allowed fields
    student_dict = {f"student.{field}": getattr(student, field) for field in ALLOWED_FIELDS}

    # Check each placeholder
    for key in placeholders:
        if key not in student_dict:
            raise ValueError(f"Unauthorized or unknown placeholder '{key}' detected.")
        # Replacement will be handled by str.format

    try:
        report = report_template.format(**student_dict)
    except KeyError as e:
        # In case the placeholder mapping was incomplete
        raise ValueError(f"Missing data for placeholder: {e}") from e

    return report