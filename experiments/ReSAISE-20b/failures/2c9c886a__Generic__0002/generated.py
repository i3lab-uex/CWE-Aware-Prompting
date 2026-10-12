import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------
# Mock data structures and storage
# ------------------------------------------------------------

@dataclass(frozen=True)
class Student:
    student_number: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)  # sensitive
    discipline_record: str = field(repr=False)  # sensitive

# In‑memory "database" of students
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of project"
    ),
}

# ------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------

def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholder names found in the template.
    Supports nested attributes (e.g., student.name).
    """
    pattern = r"{([^{}]+)}"
    placeholders = set(re.findall(pattern, template))
    return {p.strip() for p in placeholders if p}

def _validate_placeholders(placeholders: set, allowed_attrs: set) -> None:
    """
    Raise ValueError if any placeholder is not in the allowed_attrs.
    """
    invalid = placeholders - allowed_attrs
    if invalid:
        raise ValueError(f"Unauthorized placeholder(s) detected: {', '.join(sorted(invalid))}")

def _get_allowed_attrs() -> set:
    """
    Return a set of allowed attribute names for the Student class.
    """
    return {"name", "course", "age", "gpa"}

# ------------------------------------------------------------
# Main function
# ------------------------------------------------------------

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Args:
        student_number: Unique identifier of the student.
        report_template: Format string containing placeholders.

    Returns:
        A formatted report string with the student's data inserted.

    Raises:
        ValueError: If an unauthorized placeholder is used or
                    the student_number does not exist.
    """
    # Retrieve student record
    student = _STUDENT_DB.get(student_number)
    if not student:
        raise ValueError(f"Student with number '{student_number}' does not exist.")

    # Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    allowed_attrs = _get_allowed_attrs()
    _validate_placeholders(placeholders, allowed_attrs)

    # Build context dictionary
    context = {attr: getattr(student, attr) for attr in allowed_attrs}

    # Perform formatting
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report