import re
from string import Template
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
# Mocked data layer – in a real system this would query a database or API.
# --------------------------------------------------------------------------- #

@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # sensitive
    discipline_record: str

# Sample in‑memory store
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in Math 101"
    ),
}

def _get_student_by_id(student_id: str) -> Student:
    """Retrieve a student instance by ID. Raises KeyError if not found."""
    try:
        return _STUDENT_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{student_id}' not found.") from exc

# --------------------------------------------------------------------------- #
# Report generation
# --------------------------------------------------------------------------- #

# Allowed template fields (non‑sensitive)
_ALLOWED_FIELDS = {
    "student.name",
    "student.course",
    "student.age",
    "student.gpa",
}

# Sensitive fields that must not appear in the template
_SENSITIVE_FIELDS = {
    "student.home_address",
    "student.discipline_record",
}

# Regular expression to extract placeholders like {student.name}
_PLACEHOLDER_RE = re.compile(r"{([^}]+)}")

def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a report string for the given student using the provided template.

    Parameters
    ----------
    student_id : str
        Unique identifier of the student.
    template : str
        Template string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the student ID is unknown, if the template contains disallowed or
        sensitive fields, or if formatting fails.
    """
    # Fetch the student data
    student = _get_student_by_id(student_id)

    # Extract placeholders from the template
    placeholders = set(_PLACEHOLDER_RE.findall(template))

    # Validate placeholders: no sensitive data and all are allowed
    if not placeholders.issubset(_ALLOWED_FIELDS | _SENSITIVE_FIELDS):
        invalid = placeholders - (_ALLOWED_FIELDS | _SENSITIVE_FIELDS)
        raise ValueError(f"Template contains invalid or disallowed fields: {invalid}")

    if placeholders & _SENSITIVE_FIELDS:
        raise ValueError(f"Template attempts to access sensitive fields: {placeholders & _SENSITIVE_FIELDS}")

    # Build a mapping for string.Template
    context = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": str(student.age),
        "student.gpa": f"{student.gpa:.2f}",
    }

    # Use string.Template for safe substitution
    try:
        tmpl = Template(template)
        report = tmpl.safe_substitute(context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return report