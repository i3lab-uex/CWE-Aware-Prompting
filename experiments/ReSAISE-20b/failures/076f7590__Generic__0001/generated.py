import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Mock data structures and a simple in‑memory “database”
# --------------------------------------------------------------------

@dataclass
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str = field(repr=False)  # sensitive
    discipline_record: str = field(repr=False)  # sensitive

# Example in‑memory database keyed by student_token
STUDENT_DB: Dict[str, Student] = {
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
        home_address="456 Oak Ave, Rivertown",
        discipline_record="Late assignment"
    ),
}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

ALLOWED_ATTRIBUTES = {"name", "course", "age", "GPA"}

PLACEHOLDER_PATTERN = re.compile(r"{\s*([^}]+)\s*}")

def _extract_placeholders(template: str):
    """
    Return a set of placeholder keys found in the template.
    """
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _validate_placeholders(placeholders: set):
    """
    Ensure that all placeholders refer to allowed attributes of the student.
    Raise ValueError if an unauthorized attribute is detected.
    """
    for key in placeholders:
        # Expect keys of the form student.<attr>
        if not key.startswith("student."):
            raise ValueError(f"Invalid placeholder '{key}'. Only 'student' namespace is allowed.")
        attr = key.split(".", 1)[1]
        if attr not in ALLOWED_ATTRIBUTES:
            raise ValueError(f"Unauthorized access to sensitive attribute '{attr}'.")

def _build_context(student: Student):
    """
    Create a dictionary suitable for string formatting.
    The key is 'student' and the value is an object that exposes only
    the allowed attributes.
    """
    class StudentProxy:
        def __init__(self, orig: Student):
            self._orig = orig

        # Provide dynamic attribute access but only for allowed fields
        def __getattr__(self, name):
            if name in ALLOWED_ATTRIBUTES:
                return getattr(self._orig, name)
            raise AttributeError(f"Access to '{name}' is forbidden.")

    return {"student": StudentProxy(student)}

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report by rendering the provided template with
    allowed attributes of the specified student.

    Parameters
    ----------
    student_token : str
        Unique identifier for the student.
    report_template : str
        Format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the token is unknown, or if the template tries to access
        disallowed data.
    """
    # 1. Retrieve student
    student = STUDENT_DB.get(student_token)
    if not student:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # 2. Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # 3. Build context and render
    context = _build_context(student)
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

    return report