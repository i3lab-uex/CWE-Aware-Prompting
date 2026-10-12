import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------- Student Model ---------------------------------

@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive

# --------------------------- In‑memory Store ---------------------------------

# Example in‑memory storage. In a real system this would be a database.
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2023-04-12"
    ),
}

# --------------------------- Allowed Attributes -----------------------------

# Derive the set of attributes that are safe to expose in a report.
_ALLOWED_ATTRS = {f.name for f in fields(Student)} - {"home_address", "discipline_record"}

# --------------------------- Template Parsing --------------------------------

_PLACEHOLDER_RE = re.compile(r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(template: str) -> set:
    """Return the set of placeholder names found in *template*."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

# --------------------------- Core Function ----------------------------------

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report from *report_template* by substituting
    placeholders with data from the student identified by *stu_id*.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    report_template : str
        A format string containing placeholders such as '{name}' or '{course}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist or if the template attempts to access
        disallowed (sensitive) attributes.
    """
    # Fetch student or raise error if not found
    try:
        student = _STUDENT_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{stu_id}' not found.") from exc

    # Validate placeholders
    placeholders = _extract_placeholders(report_template)
    unauthorized = placeholders - _ALLOWED_ATTRS
    if unauthorized:
        raise ValueError(
            f"Template contains disallowed placeholders: {', '.join(sorted(unauthorized))}"
        )

    # Build mapping of allowed attributes
    student_dict = {attr: getattr(student, attr) for attr in _ALLOWED_ATTRS}

    # Perform safe formatting
    try:
        report = report_template.format(**student_dict)
    except KeyError as exc:  # Should not happen due to earlier validation
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report