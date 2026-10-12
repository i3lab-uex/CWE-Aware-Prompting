import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data layer – in a real system this would query a database
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    stu_id: str          # unique identifier
    name: str
    course: str
    age: int
    GPA: float
    home_address: str   # sensitive
    discipline_record: str  # sensitive

# Example in‑memory store of students
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission in 2023"
    ),
}

def _get_student_by_id(stu_id: str) -> Student:
    """Retrieve a student from the mock database or raise an error."""
    student = _STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")
    return student

# --------------------------------------------------------------------------- #
# Report generation
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

_placeholder_pattern = re.compile(r"{([^{}]+)}")

def _validate_template(template: str) -> None:
    """
    Ensure that all placeholders in the template reference only allowed fields.
    Raises ValueError if a forbidden field is detected.
    """
    for match in _placeholder_pattern.finditer(template):
        placeholder = match.group(1).strip()
        # Only support simple attribute access like 'student.name'
        parts = placeholder.split(".")
        if len(parts) != 2 or parts[0] != "student":
            raise ValueError(f"Invalid placeholder syntax: '{placeholder}'. "
                             f"Only 'student.<field>' is allowed.")
        field_name = parts[1]
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive or disallowed field '{field_name}' "
                             f"is not permitted in the report template.")

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report by formatting the provided template with
    non-sensitive attributes of the specified student.

    Parameters:
        stu_id (str): Unique identifier for the student.
        report_template (str): Template containing placeholders like
                               '{student.name}', '{student.course}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the student ID does not exist or if the template
                    attempts to access disallowed data.
    """
    # Retrieve student record
    student = _get_student_by_id(stu_id)

    # Validate placeholders in the template
    _validate_template(report_template)

    # Build a mapping of allowed fields for formatting
    field_values = {field: getattr(student, field) for field in ALLOWED_FIELDS}

    # Perform formatting
    try:
        report = report_template.format(student=field_values)
    except KeyError as exc:
        # This should not happen due to validation, but guard anyway
        raise ValueError(f"Missing placeholder data: {exc}") from exc

    return report

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}"
    )
    print(create_student_report("S001", template))