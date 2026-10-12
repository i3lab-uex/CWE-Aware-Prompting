import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Student model – in a real system this would be loaded from a database
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    unique_id: str
    name: str
    course: str
    age: int
    gpa: float          # sensitive
    home_address: str   # sensitive
    discipline_record: str

# ----------------------------------------------------------------------
# In‑memory "database" of students (for demonstration purposes)
# ----------------------------------------------------------------------
STUDENT_DB: Dict[str, Student] = {
    "s123": Student(
        unique_id="s123",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.9,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "s456": Student(
        unique_id="s456",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late assignment"
    ),
}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"gpa", "home_address"}
_PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(template: str) -> set:
    """
    Extract attribute names from a template string.
    Example: "{student.name} is {student.age}" -> {"name", "age"}
    """
    return set(match.group(1) for match in _PLACEHOLDER_RE.finditer(template))

def _validate_no_sensitive_access(placeholders: set):
    """
    Raise ValueError if any placeholder refers to a sensitive attribute.
    """
    intersection = placeholders & _SENSITIVE_FIELDS
    if intersection:
        raise ValueError(f"Access to sensitive attributes forbidden: {', '.join(intersection)}")

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Build a formatted student profile string based on the provided template.

    Parameters
    ----------
    unique_id : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted student profile string.

    Raises
    ------
    ValueError
        If the unique_id is not found or if the template attempts to access a sensitive attribute.
    """
    # 1. Retrieve student data
    student = STUDENT_DB.get(unique_id)
    if not student:
        raise ValueError(f"Student with unique_id '{unique_id}' does not exist.")

    # 2. Validate template for sensitive attribute access
    placeholders = _extract_placeholders(report_template)
    _validate_no_sensitive_access(placeholders)

    # 3. Prepare a dictionary of allowed attributes
    student_dict = {k: v for k, v in asdict(student).items() if k not in _SENSITIVE_FIELDS}

    # 4. Perform the formatting
    try:
        formatted = report_template.format(student=student_dict)
    except KeyError as e:
        raise ValueError(f"Template references unknown attribute: {e.args[0]}") from e

    return formatted