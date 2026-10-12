import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Mock Student data model and storage (simulating a database)
# --------------------------------------------------------------------

@dataclass
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float          # considered sensitive
    home_address: str   # sensitive
    discipline_record: str  # sensitive

# In‑memory "database" of students
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2023-05-12"
    ),
    # Add more students as needed
}

# --------------------------------------------------------------------
# Helper utilities for safe report generation
# --------------------------------------------------------------------

ALLOWED_FIELDS = {"name", "course", "age"}
SENSITIVE_FIELDS = {"GPA", "home_address", "discipline_record"}

PLACEHOLDER_PATTERN = re.compile(r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _validate_placeholders(placeholders: set):
    """Ensure no sensitive fields are referenced."""
    if placeholders & SENSITIVE_FIELDS:
        raise ValueError(
            f"Unauthorized access to sensitive data: {placeholders & SENSITIVE_FIELDS}"
        )

def _build_context(student: Student) -> Dict[str, str]:
    """Create a context dictionary with only allowed fields."""
    return {
        "name": student.name,
        "course": student.course,
        "age": str(student.age),
    }

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def draft_student_report(
    student_number: str,
    report_template: str
) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_number : str
        Unique identifier for the student.
    report_template : str
        A format string containing placeholders like `{name}` or `{course}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student_number does not exist or if the template references
        sensitive data.
    """
    # Retrieve student record; raise error if not found
    student = STUDENT_DB.get(student_number)
    if not student:
        raise ValueError(f"Student with number '{student_number}' does not exist.")

    # Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # Build context and perform safe formatting
    context = _build_context(student)
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to earlier validation
        raise ValueError(f"Missing placeholder in context: {exc}") from exc

    return report

# --------------------------------------------------------------------
# Example usage (for testing purposes only)
# --------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
    )
    print(draft_student_report("S001", template))