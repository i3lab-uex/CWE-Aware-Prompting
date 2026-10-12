import re
from dataclasses import dataclass, fields
from typing import Dict

# ------------------------------
# Mock Student database and class
# ------------------------------

@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str          # Sensitive
    discipline_record: str     # Sensitive

# In‑memory student repository (stu_id -> Student)
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission on 2024-06-15"
    ),
}

# ------------------------------
# Report generation logic
# ------------------------------

ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

def _extract_placeholders(template: str) -> set[str]:
    """
    Extracts placeholder names from a format string.
    Supports both simple {field} and advanced {{}} syntax.
    """
    # Regex to match {name}, {student.name} etc. but we only allow simple names
    pattern = r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return set(re.findall(pattern, template))

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generates a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    report_template : str
        Format string containing placeholders for allowed fields.

    Returns
    -------
    str
        The formatted report.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if the template contains disallowed fields.
    """
    # 1. Retrieve student
    try:
        student = STUDENT_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{stu_id}' not found.") from exc

    # 2. Validate placeholders
    placeholders = _extract_placeholders(report_template)
    disallowed = placeholders - ALLOWED_FIELDS
    if disallowed:
        raise ValueError(
            f"Unauthorized access to sensitive data: {', '.join(sorted(disallowed))}"
        )

    # 3. Build context dictionary
    context = {field: getattr(student, field) for field in placeholders}

    # 4. Format the template safely
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This shouldn't happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report

# ------------------------------
# Example usage (uncomment to test)
# ------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
        "GPA: {GPA:.2f}"
    )
    print(create_student_report("S001", template))