import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str          # Sensitive
    disciplinary_record: str  # Sensitive


# --------------------------------------------------------------------------- #
# In‑memory repository (stub for demonstration)
# --------------------------------------------------------------------------- #

class StudentRepository:
    """Simple in‑memory store of students."""
    _students: Dict[str, Student] = {
        "S001": Student(
            name="Alice Johnson",
            course="Computer Science",
            age=20,
            gpa=3.8,
            home_address="123 Maple St, Springfield",
            disciplinary_record="None"
        ),
        "S002": Student(
            name="Bob Smith",
            course="Mathematics",
            age=22,
            gpa=3.5,
            home_address="456 Oak Ave, Shelbyville",
            disciplinary_record="Late submission of assignment 3"
        ),
    }

    @classmethod
    def get(cls, stu_id: str) -> Student:
        """Retrieve a student by ID."""
        if not isinstance(stu_id, str):
            raise ValueError("Student ID must be a string.")
        student = cls._students.get(stu_id)
        if student is None:
            raise ValueError(f"Student ID '{stu_id}' not found.")
        return student


# --------------------------------------------------------------------------- #
# Summary generation
# --------------------------------------------------------------------------- #

# Attributes that are considered sensitive and must not be exposed in the template.
_RESTRICTED_ATTRS = {"home_address", "disciplinary_record"}

# Regular expression to find placeholders like {student.attr}
_PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report by filling in placeholders from the provided template.

    Args:
        stu_id (str): Unique identifier for a student.
        summary_template (str): Template string containing placeholders such as
                                '{student.name}', '{student.course}'.

    Returns:
        str: The formatted student report.

    Raises:
        ValueError: If the template references restricted fields, or if the
                    student ID is invalid.
    """
    # Retrieve the student record
    student = StudentRepository.get(stu_id)

    # Find all placeholders in the template
    placeholders = _PLACEHOLDER_RE.findall(summary_template)

    # Validate that no restricted attribute is used
    for attr in placeholders:
        if attr not in {f.name for f in fields(Student)}:
            raise ValueError(f"Invalid placeholder '{{student.{attr}}}' not found in Student attributes.")
        if attr in _RESTRICTED_ATTRS:
            raise ValueError(f"Access to restricted attribute '{{student.{attr}}}' is prohibited.")

    # Prepare a mapping for formatting
    context = {f"student.{field.name}": getattr(student, field.name) for field in fields(Student)
               if field.name not in _RESTRICTED_ATTRS}

    # Replace placeholders safely
    def replacer(match: re.Match) -> str:
        key = match.group(0)  # e.g., '{student.name}'
        return str(context.get(key, match.group(0)))

    result = _PLACEHOLDER_RE.sub(replacer, summary_template)
    return result