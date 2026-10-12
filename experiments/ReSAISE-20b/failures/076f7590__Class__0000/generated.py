import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Domain model – a minimal Student representation
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float
    # Sensitive fields that must never be exposed in a report
    home_address: str = field(repr=False, compare=False)
    discipline_record: str = field(repr=False, compare=False)


# ------------------------------------------------------------------
# In‑memory “database” of students keyed by a unique token
# ------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "token_123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "token_456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission of Assignment 3"
    ),
}


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

_PLACEHOLDER_PATTERN = re.compile(r"{student\.([a-zA-Z_][a-zA-Z0-9_]*)}")


def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference any disallowed student attributes.
    Raises ValueError if an unauthorized placeholder is found.
    """
    for match in _PLACEHOLDER_PATTERN.finditer(template):
        field_name = match.group(1)
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive student field '{field_name}' in template."
            )


def _safe_student_dict(student: Student) -> Dict[str, object]:
    """
    Return a dictionary containing only the allowed student attributes.
    """
    return {k: getattr(student, k) for k in _ALLOWED_FIELDS}


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a report for the student identified by `student_token` using
    `report_template`. The template may contain placeholders such as
    `{student.name}` or `{student.course}`.

    Args:
        student_token: Unique identifier for the student.
        report_template: A format string containing placeholders.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the token is unknown, or if the template attempts to
                    access sensitive data.
    """
    # 1. Validate that the token exists
    student = _STUDENT_DB.get(student_token)
    if not student:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # 2. Validate the template for unauthorized placeholders
    _validate_template(report_template)

    # 3. Prepare a safe mapping of allowed fields
    safe_mapping = _safe_student_dict(student)

    # 4. Perform formatting – any missing keys will raise KeyError,
    #    but this should not happen because of the earlier validation.
    try:
        report = report_template.format(student=safe_mapping)
    except KeyError as exc:
        raise ValueError(f"Template references missing field: {exc}") from None

    return report


# ------------------------------------------------------------------
# Example usage (for local testing only – remove in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA}\n"
    )
    print(compile_student_report("token_123", template))