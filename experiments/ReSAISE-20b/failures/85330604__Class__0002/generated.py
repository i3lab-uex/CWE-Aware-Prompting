import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Simulated student storage (in a real system this would be a DB)
# ------------------------------------------------------------------
@dataclass
class Student:
    """Represents a student record."""
    id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)  # sensitive
    discipline_record: str = field(repr=False)  # sensitive


# In-memory "database" of students
_STUDENTS: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of assignment"
    ),
}


# ------------------------------------------------------------------
# Report generation
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age"}

_PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")


def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report based on the supplied template.

    Args:
        stu_id: Unique identifier of the student.
        report_template: A format string containing placeholders
            like `{student.name}`. Only non-sensitive attributes are allowed.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the student ID does not exist, or if the template
            attempts to access a disallowed attribute.
    """
    # Retrieve student record
    student = _STUDENTS.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # Find all placeholders in the template
    placeholders = _PLACEHOLDER_RE.findall(report_template)

    # Validate each placeholder
    for field_name in placeholders:
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive data field '{field_name}'."
            )

    # Prepare a mapping for formatting
    context = {f"student.{k}": getattr(student, k) for k in _ALLOWED_FIELDS}

    # Perform substitution
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value: {exc}") from exc

    return report


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}"
    )
    print(create_student_report("S001", tmpl))