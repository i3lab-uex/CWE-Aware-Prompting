import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Domain model (simplified)
# ----------------------------------------------------------------------
@dataclass
class Student:
    """Represents a student record in the system."""
    name: str
    course: str
    age: int
    gpa: float          # considered sensitive
    home_address: str   # considered sensitive
    discipline_record: str  # considered sensitive


# ----------------------------------------------------------------------
# In‑memory storage of students keyed by a unique token
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "token456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023"
    ),
}


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age"}

_PLACEHOLDER_PATTERN = re.compile(r"\{(?P<field>[^{}]+)\}")


def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {m.group("field") for m in _PLACEHOLDER_PATTERN.finditer(template)}


def _validate_placeholders(placeholders: set[str]) -> None:
    """Ensure all placeholders are permitted."""
    forbidden = placeholders - _ALLOWED_FIELDS
    if forbidden:
        raise ValueError(
            f"Unauthorized placeholder(s) in template: {', '.join(forbidden)}"
        )


# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student‑specific report from a template.

    Parameters
    ----------
    student_token : str
        Unique identifier for the target student.
    report_template : str
        Template containing placeholders such as `{student.name}` or `{student.course}`.

    Returns
    -------
    str
        The report with placeholders substituted by actual student data.

    Raises
    ------
    ValueError
        If the token is unknown, or if the template contains placeholders for sensitive data.
    """
    # 1. Retrieve student record
    student = _STUDENT_DB.get(student_token)
    if not student:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # 2. Parse placeholders
    placeholders = _extract_placeholders(report_template)

    # 3. Validate that only allowed fields are referenced
    _validate_placeholders(placeholders)

    # 4. Build a mapping of allowed attributes for substitution
    context = {field: getattr(student, field) for field in placeholders}

    # 5. Perform substitution safely
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (for manual testing)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
    )
    print(compile_student_report("token123", template))