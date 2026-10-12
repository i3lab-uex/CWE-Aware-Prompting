from dataclasses import dataclass, fields
import re
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model – in a real system this would be provided elsewhere
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float          # Sensitive – must not be exposed in reports
    home_address: str   # Sensitive – must not be exposed in reports
    discipline_record: str

# --------------------------------------------------------------------------- #
# In‑memory “database” of students – for demo purposes
# --------------------------------------------------------------------------- #

_STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "s002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission in Math 101"
    ),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"GPA", "home_address"}

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive fields.
    Raises ValueError if a forbidden placeholder is detected.
    """
    # Find all placeholders of the form {student.field}
    placeholders = re.findall(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}", template)
    for field in placeholders:
        if field in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{field}' is prohibited in the report template.")


def _get_student_by_id(unique_id: str) -> Student:
    """
    Retrieve a student instance by ID.
    Raises ValueError if the ID does not exist.
    """
    try:
        return _STUDENT_DB[unique_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{unique_id}' does not exist.") from exc


def _build_context(student: Student) -> Dict[str, any]:
    """
    Build a dictionary suitable for str.format_map that contains only
    non‑sensitive attributes under the key 'student'.
    """
    allowed_attrs = {
        f.name: getattr(student, f.name)
        for f in fields(Student) if f.name not in _SENSITIVE_FIELDS
    }
    return {"student": allowed_attrs}


# --------------------------------------------------------------------------- #
# Public API – the requested function
# --------------------------------------------------------------------------- #

def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student profile using the provided template.

    Parameters
    ----------
    unique_id : str
        Unique identifier of the student.
    report_template : str
        A format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the template references a sensitive attribute or if the student ID is unknown.
    """
    # 1. Validate that template does not expose sensitive data
    _validate_template(report_template)

    # 2. Retrieve the student record
    student = _get_student_by_id(unique_id)

    # 3. Build the formatting context
    context = _build_context(student)

    # 4. Perform formatting – using format_map to avoid KeyError on missing fields
    try:
        report = report_template.format_map(context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return report