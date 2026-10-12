import string
from dataclasses import dataclass, asdict
from typing import Dict

# ------------------------------------------------------------------
# Mock student storage (in a real system this would be a database)
# ------------------------------------------------------------------
@dataclass
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str          # Sensitive
    discipline_record: str     # Sensitive

# Example data (in practice this would be loaded from a secure store)
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

# ------------------------------------------------------------------
# Allowed fields for report generation
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

def _extract_fields(template: str) -> set:
    """
    Parse a format string and return the set of field names it references.
    """
    formatter = string.Formatter()
    fields = set()
    for _, field_name, _, _ in formatter.parse(template):
        if field_name:
            # Handle nested attributes like 'student.name' (not allowed)
            base = field_name.split('.')[0]
            fields.add(base)
    return fields

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report from a template.

    Args:
        student_token: Unique identifier for the student.
        report_template: Format string containing placeholders.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the token is invalid, if sensitive data is requested,
                    or if the template contains unsupported placeholders.
    """
    # 1. Retrieve student
    student = _STUDENT_DB.get(student_token)
    if not student:
        raise ValueError("Invalid student token.")

    # 2. Validate template placeholders
    requested_fields = _extract_fields(report_template)
    if not requested_fields <= _ALLOWED_FIELDS:
        # Any field outside the allowed set is disallowed
        invalid = requested_fields - _ALLOWED_FIELDS
        raise ValueError(f"Unauthorized access to sensitive data: {', '.join(invalid)}")

    # 3. Prepare context for formatting
    student_dict = asdict(student)
    context = {field: student_dict[field] for field in requested_fields}

    # 4. Format the report
    try:
        return report_template.format(**context)
    except KeyError as e:
        # This should not happen due to prior validation
        raise ValueError(f"Missing data for placeholder: {e}") from e

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Student Report:\nName: {name}\nCourse: {course}\nAge: {age}\nGPA: {GPA}"
#     print(compile_student_report("token123", template))