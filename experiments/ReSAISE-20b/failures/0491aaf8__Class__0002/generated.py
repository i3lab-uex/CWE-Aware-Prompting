import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Student model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """A simple immutable student data holder."""
    name: str
    course: str
    age: int
    GPA: float          # Sensitive – should never be exposed
    home_address: str   # Sensitive – should never be exposed
    discipline_record: str

# ----------------------------------------------------------------------
# In‑memory store of students (for demo purposes)
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "s123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.9,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "s456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.7,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late assignment"
    ),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _is_sensitive_placeholder(template: str) -> bool:
    """
    Detects any attempt to reference sensitive attributes in the template.
    Only 'name', 'course', and 'age' are allowed.
    """
    # Allowed placeholders
    allowed = {"name", "course", "age"}
    # Find all patterns like {student.attr}
    placeholders = re.findall(r"{\s*student\.([a-zA-Z_]\w*)\s*}", template)
    for attr in placeholders:
        if attr not in allowed:
            return True
    return False

def _safe_student_dict(student: Student) -> Dict[str, any]:
    """
    Returns a dictionary containing only non‑sensitive attributes
    that can safely be used in string formatting.
    """
    return {
        "name": student.name,
        "course": student.course,
        "age": student.age
    }

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generates a student report based on the provided template.

    Parameters
    ----------
    id : str
        Unique identifier of the student.
    format_string : str
        A template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if the template attempts to
        expose sensitive data (GPA, home_address, etc.).
    """
    # Validate ID existence
    student = _STUDENT_DB.get(id)
    if student is None:
        raise ValueError(f"Student ID '{id}' does not exist.")

    # Detect sensitive placeholders
    if _is_sensitive_placeholder(format_string):
        raise ValueError("Template attempts to access sensitive student attributes.")

    # Build a safe context for formatting
    context = {"student": _safe_student_dict(student)}

    try:
        result = format_string.format(**context)
    except KeyError as exc:
        # Provide a clear error message for unknown placeholders
        raise ValueError(f"Unknown placeholder in template: {exc}") from exc

    return result