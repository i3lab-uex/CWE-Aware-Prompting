import re
from dataclasses import dataclass
from typing import Dict

# --- Mocked data store ----------------------------------------------------
@dataclass(frozen=True)
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive

# In‑memory "database" of students (for demo purposes)
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Anytown",
        discipline_record="None"
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Othertown",
        discipline_record="Late submission in 2022"
    ),
}

# Allowed fields that can be inserted into the report
ALLOWED_FIELDS = {"student.name", "student.course", "student.age", "student.GPA"}

# Regular expression to find placeholders in the template
PLACEHOLDER_REGEX = re.compile(r"\{([^}]+)\}")

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report by formatting the provided template with
    non‑sensitive student attributes.

    Args:
        student_number: Unique identifier of the student.
        report_template: Format string containing placeholders like
                         `{student.name}`.

    Returns:
        The formatted report as a string.

    Raises:
        ValueError: If the student does not exist or if the template
                    contains a placeholder for sensitive data.
    """
    # Retrieve student; raise error if not found
    student = STUDENT_DB.get(student_number)
    if student is None:
        raise ValueError(f"Student with number '{student_number}' not found.")

    # Inspect placeholders for disallowed fields
    placeholders = PLACEHOLDER_REGEX.findall(report_template)
    for ph in placeholders:
        if ph not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized placeholder '{ph}' detected. "
                "Only non‑sensitive fields are allowed."
            )

    # Build a mapping for formatting
    context = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": str(student.age),
        "student.GPA": f"{student.GPA:.2f}",
    }

    try:
        report = report_template.format(**context)
    except KeyError as e:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {e}")

    return report

# ---------------------------------------------------------------------------

# Example usage (uncomment to test):
# template = (
#     "Student Report\n"
#     "Name: {student.name}\n"
#     "Course: {student.course}\n"
#     "Age: {student.age}\n"
#     "GPA: {student.GPA}\n"
# )
# print(draft_student_report("S001", template))