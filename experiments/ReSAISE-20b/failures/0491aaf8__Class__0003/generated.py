import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Domain model – a simple Student class
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float = field(repr=False)           # sensitive
    home_address: str = field(repr=False)    # sensitive
    discipline_record: list[str] = field(default_factory=list)

# ----------------------------------------------------------------------
# In‑memory “database” of students – replace with a real DB in production
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "s123": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple Street, Springfield",
        discipline_record=[]
    ),
    "s456": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Avenue, Springfield",
        discipline_record=["Late submission"]
    ),
}

# ----------------------------------------------------------------------
# Helper – detect disallowed placeholders
# ----------------------------------------------------------------------
_DISALLOWED_PATTERNS = [
    re.compile(r"\bGPA\b", re.IGNORECASE),
    re.compile(r"\bhome_address\b", re.IGNORECASE)
]

def _contains_sensitive_placeholder(template: str) -> bool:
    """
    Return True if the template contains any placeholder that refers to a
    sensitive attribute (GPA or home_address).
    """
    # Find all field names inside {…} placeholders
    for _, field_name, _, _ in re.finditer(r"{([^{}]+)}", template):
        for pat in _DISALLOWED_PATTERNS:
            if pat.search(field_name):
                return True
    return False

# ----------------------------------------------------------------------
# Main function – create_student_summary
# ----------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report using the supplied template.

    Args:
        id: A unique identifier for the student.
        format_string: A Python format string containing placeholders
                       such as '{student.name}', '{student.course}', etc.

    Returns:
        A formatted string representing the student's report.

    Raises:
        ValueError: If a sensitive attribute is accessed or if the id
                    does not exist in the database.
    """
    # 1. Validate student ID exists
    if id not in _STUDENT_DB:
        raise ValueError(f"Student with ID '{id}' does not exist.")

    student = _STUDENT_DB[id]

    # 2. Ensure no sensitive data is requested
    if _contains_sensitive_placeholder(format_string):
        raise ValueError("Template attempts to access sensitive student data.")

    # 3. Safely format the string
    try:
        result = format_string.format(student=student)
    except AttributeError as e:
        # If the placeholder refers to a non‑existent attribute
        raise ValueError(f"Invalid placeholder in template: {e}") from e

    return result