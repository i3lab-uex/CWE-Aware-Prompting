import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
#  Student data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    id: str
    name: str
    course: str
    age: int
    GPA: float          # sensitive
    home_address: str   # sensitive
    discipline_record: str

# ----------------------------------------------------------------------
#  In‑memory storage of students (for demonstration purposes)
# ----------------------------------------------------------------------
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.6,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023"
    ),
}

# ----------------------------------------------------------------------
#  Utility functions
# ----------------------------------------------------------------------
def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from a format string.
    Only simple attribute access is allowed (e.g. {student.name}).
    """
    pattern = r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return set(re.findall(pattern, template))

def _validate_no_sensitive(placeholders: set) -> None:
    """
    Ensure that no sensitive attributes are requested.
    Raises ValueError if a forbidden attribute is found.
    """
    sensitive = {"GPA", "home_address"}
    if placeholders & sensitive:
        raise ValueError(
            f"Access to sensitive attributes {placeholders & sensitive} is forbidden."
        )

# ----------------------------------------------------------------------
#  Main function
# ----------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report based on the provided format string.

    Args:
        id: The unique identifier of the student.
        format_string: A Python format string containing placeholders such as
                       '{student.name}', '{student.course}', etc.

    Returns:
        A string containing the formatted report.

    Raises:
        ValueError: If the student ID does not exist or if the template tries
                    to access sensitive attributes (GPA, home_address).
    """
    # 1. Validate student existence
    student = STUDENT_DB.get(id)
    if not student:
        raise ValueError(f"Student ID '{id}' does not exist.")

    # 2. Parse placeholders and check for sensitive data
    placeholders = _extract_placeholders(format_string)
    _validate_no_sensitive(placeholders)

    # 3. Build a simple namespace for formatting
    namespace = {"student": student}

    try:
        result = format_string.format(**namespace)
    except KeyError as exc:
        # The placeholder was not a valid Student attribute
        raise ValueError(f"Invalid placeholder in format string: {exc}") from exc

    return result