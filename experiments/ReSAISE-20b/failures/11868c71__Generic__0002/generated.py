import string
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Domain model – a very small Student entity
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    unique_id: str
    name: str
    course: str
    age: int
    GPA: float = field(repr=False)          # Sensitive – not allowed in reports
    home_address: str = field(repr=False)   # Sensitive – not allowed in reports

# ----------------------------------------------------------------------
# In‑memory data store (for demonstration purposes)
# ----------------------------------------------------------------------
STUDENTS: Dict[str, Student] = {
    "S001": Student(
        unique_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
    ),
    "S002": Student(
        unique_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
    ),
}

# ----------------------------------------------------------------------
# Utility – detect placeholders in a format string
# ----------------------------------------------------------------------
def _extract_placeholders(template: str) -> set[str]:
    """
    Return a set of all field names used in the format string.
    Example: '{student.name} is {student.age}' -> {'student.name', 'student.age'}
    """
    formatter = string.Formatter()
    return {field_name for _, field_name, _, _ in formatter.parse(template) if field_name}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Build a formatted student profile using the provided template.

    Raises
    ------
    ValueError
        If a sensitive attribute (GPA or home_address) is referenced in the template,
        or if the unique_id does not correspond to a known student.
    """
    # 1. Validate existence of the student
    if unique_id not in STUDENTS:
        raise ValueError(f"Student with id '{unique_id}' does not exist.")

    student = STUDENTS[unique_id]

    # 2. Parse the template for placeholders
    placeholders = _extract_placeholders(report_template)

    # 3. Guard against sensitive fields
    SENSITIVE_FIELDS = {"student.GPA", "student.home_address"}
    if placeholders & SENSITIVE_FIELDS:
        raise ValueError(
            f"Template contains sensitive fields: {placeholders & SENSITIVE_FIELDS}"
        )

    # 4. Build a context dictionary for formatting
    context = {"student": student}

    # 5. Format and return the report
    try:
        return report_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}"
    )
    print(build_student_profile("S001", template))