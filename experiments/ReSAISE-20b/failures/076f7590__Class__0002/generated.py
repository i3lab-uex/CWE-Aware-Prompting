import re
from dataclasses import dataclass, fields
from typing import Dict

# --- Mock student storage ----------------------------------------------------
# In a real system this would be replaced with database access logic.
@dataclass
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str   # sensitive
    discipline_record: str  # sensitive

# Example in‑memory database of students keyed by token
_STUDENT_DB: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "token456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission"
    ),
}

# --- Allowed attributes ------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

# --- Utility functions ------------------------------------------------------
def _extract_template_fields(template: str) -> set:
    """
    Extract placeholder field names from a format string.
    Supports nested attribute access like {student.name}.
    """
    # Regex matches the key part of a format field, e.g. 'student.name'
    pattern = r"{(?P<field>[^{}]+)}"
    fields_found = set()
    for match in re.finditer(pattern, template):
        key = match.group("field")
        # Only consider the first component before a dot
        fields_found.add(key.split(".", 1)[0])
    return fields_found

# --- Main function -----------------------------------------------------------
def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_token : str
        Unique identifier for the student.
    report_template : str
        Format string containing placeholders for allowed fields.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token does not exist or if the template attempts to access
        disallowed (sensitive) fields.
    """
    # Validate token
    student = _STUDENT_DB.get(student_token)
    if not student:
        raise ValueError("Invalid or unknown student token")

    # Parse template for placeholders
    used_fields = _extract_template_fields(report_template)

    # Ensure no sensitive fields are requested
    if not used_fields.issubset(_ALLOWED_FIELDS):
        disallowed = used_fields - _ALLOWED_FIELDS
        raise ValueError(
            f"Template contains disallowed fields: {', '.join(disallowed)}"
        )

    # Prepare context dictionary for formatting
    context = {field: getattr(student, field) for field in used_fields}

    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # Should not happen because we validated fields, but catch just in case
        raise ValueError(f"Missing field in context: {exc}") from exc

    return report