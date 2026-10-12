import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
#  Domain model – Student
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student with non‑sensitive data."""
    id: str
    name: str
    course: str
    age: int
    # Sensitive attributes – do not expose them in reports
    GPA: float = field(repr=False, compare=False)
    home_address: str = field(repr=False, compare=False)
    discipline_record: list[str] = field(default_factory=list, repr=False, compare=False)

# --------------------------------------------------------------------------- #
#  In‑memory repository (stub for demonstration)
# --------------------------------------------------------------------------- #

STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple Street, Springfield",
        discipline_record=[],
    ),
    "S002": Student(
        id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Avenue, Springfield",
        discipline_record=["Late submission of Assignment 3"],
    ),
}

# --------------------------------------------------------------------------- #
#  Utility – Detect sensitive attribute usage in a format string
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"GPA", "home_address", "discipline_record"}

def _contains_sensitive_placeholders(format_string: str) -> bool:
    """
    Returns True if the format string contains placeholders for sensitive fields.
    Uses a simple regex to extract attributes accessed via 'student.<attr>'.
    """
    pattern = r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    for match in re.finditer(pattern, format_string):
        attr = match.group(1)
        if attr in _SENSITIVE_FIELDS:
            return True
    return False

# --------------------------------------------------------------------------- #
#  Main function – create_student_summary
# --------------------------------------------------------------------------- #

def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a formatted student report using the provided template.

    Parameters
    ----------
    id : str
        Unique identifier of the student.
    format_string : str
        Template containing placeholders like '{student.name}' or
        '{student.course}'. Must not reference sensitive fields.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the format string attempts to
        access a sensitive attribute.
    """
    # Validate student existence
    student = STUDENT_DB.get(id)
    if not student:
        raise ValueError(f"Student with id '{id}' does not exist.")

    # Check for sensitive placeholders
    if _contains_sensitive_placeholders(format_string):
        raise ValueError("Format string contains references to sensitive data.")

    try:
        report = format_string.format(student=student)
    except KeyError as exc:
        # Provide a clearer error message
        raise ValueError(f"Unknown placeholder in format string: {exc}") from exc

    return report

# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = "Student Report:\nName: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(create_student_summary("S001", template))