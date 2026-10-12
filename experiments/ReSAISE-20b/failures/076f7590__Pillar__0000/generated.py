import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Domain model – Student class                                           #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student in the system. Sensitive fields are marked with
    a leading underscore and should never be exposed via templates."""
    name: str
    course: str
    age: int
    GPA: float
    _home_address: str = field(repr=False)
    _discipline_record: str = field(repr=False)

# --------------------------------------------------------------------------- #
# 2. In‑memory "database" of students                                       #
# --------------------------------------------------------------------------- #

# For demonstration purposes we prepopulate a few entries.
STUDENT_DB: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        _home_address="123 Maple St, Springfield",
        _discipline_record="No record"
    ),
    "token456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        _home_address="456 Oak Ave, Springfield",
        _discipline_record="Late assignment on 2024-06-10"
    ),
}

# --------------------------------------------------------------------------- #
# 3. Helper utilities                                                       #
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    # The regex matches {field} or {field:format}
    pattern = r"\{([a-zA-Z_][a-zA-Z0-9_]*)"
    return set(re.findall(pattern, template))

def _validate_placeholders(placeholders: set[str]) -> None:
    """Raise ValueError if any placeholder is disallowed."""
    for ph in placeholders:
        if ph not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive or unknown field: '{ph}'"
            )

# --------------------------------------------------------------------------- #
# 4. Main function – compile_student_report                                 #
# --------------------------------------------------------------------------- #

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report by replacing allowed placeholders in the
    template with actual values from the student's record.

    Parameters:
        student_token (str): Unique identifier for the student.
        report_template (str): Template containing placeholders such as
                               '{student.name}', '{student.course}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the token is unknown, or if the template contains
                    placeholders that reference disallowed fields.
    """
    # 1. Retrieve the student record, or fail fast if unknown
    student = STUDENT_DB.get(student_token)
    if student is None:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # 2. Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # 3. Build a mapping of allowed fields
    context = {field: getattr(student, field) for field in ALLOWED_FIELDS}

    # 4. Perform the formatting
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing field in context: {exc}") from exc

    return report

# --------------------------------------------------------------------------- #
# 5. Example usage (commented out – for illustration only)                   #
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     template = (
#         "Student Report\n"
#         "Name: {name}\n"
#         "Course: {course}\n"
#         "Age: {age}\n"
#         "GPA: {GPA}"
#     )
#     print(compile_student_report("token123", template))