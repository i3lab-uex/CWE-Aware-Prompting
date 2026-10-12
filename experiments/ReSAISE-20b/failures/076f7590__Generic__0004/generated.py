import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
# Mock student data store and Student class
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive

# In‑memory token → Student mapping (for demonstration purposes)
STUDENT_DB: Dict[str, Student] = {
    "token_123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Main St, Anytown",
        discipline_record="None"
    ),
    "token_456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Othertown",
        discipline_record="Late submission"
    ),
}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "gpa"}

def _extract_placeholders(template: str) -> set[str]:
    """
    Extract all placeholder names from a format string.
    Placeholders are expected to be of the form {field}.
    """
    # The regex matches anything inside braces that is a valid identifier
    return set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", template))

def _student_to_dict(student: Student) -> Dict[str, str]:
    """
    Convert a Student instance into a dictionary of allowed attributes.
    Values are converted to strings for formatting.
    """
    return {f: str(getattr(student, f)) for f in ALLOWED_FIELDS}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Args:
        student_token: Unique identifier for the student.
        report_template: A format string containing placeholders
                         such as '{name}', '{course}', etc.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the token is invalid, or if the template
                    attempts to access disallowed student data.
    """
    # 1. Validate token and fetch student
    student = STUDENT_DB.get(student_token)
    if not student:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # 2. Validate placeholders
    placeholders = _extract_placeholders(report_template)
    unauthorized = placeholders - ALLOWED_FIELDS
    if unauthorized:
        raise ValueError(
            f"Unauthorized data access attempted: {', '.join(sorted(unauthorized))}"
        )

    # 3. Build context for formatting
    context = _student_to_dict(student)

    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # Should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report