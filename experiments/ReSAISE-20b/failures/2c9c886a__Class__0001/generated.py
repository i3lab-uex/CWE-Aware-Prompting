import re
from dataclasses import dataclass, asdict

# -----------------------------
# Student model and mock storage
# -----------------------------

@dataclass(frozen=True)
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str      # Sensitive
    discipline_record: str # Sensitive

# In‑memory "database" of students
_STUDENTS_DB = {
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
        discipline_record="Late submission in Assignment 3"
    ),
}

# -----------------------------
# Helper utilities
# -----------------------------

ALLOWED_ATTRIBUTES = {"name", "course", "age", "GPA"}

PLACEHOLDER_PATTERN = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(template: str):
    """Return a set of attribute names referenced in the template."""
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _get_student(student_number: str) -> Student:
    """Retrieve a student or raise ValueError if not found."""
    try:
        return _STUDENTS_DB[student_number]
    except KeyError as exc:
        raise ValueError(f"Student number '{student_number}' does not exist.") from exc

# -----------------------------
# Main function
# -----------------------------

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report by filling in allowed attributes from the provided template.

    Args:
        student_number: Unique identifier of the student.
        report_template: Template string containing placeholders like '{student.name}'.

    Returns:
        A formatted string with the student's data substituted into the template.

    Raises:
        ValueError: If the student does not exist or if the template references
                    disallowed (sensitive) attributes.
    """
    # Retrieve student record
    student = _get_student(student_number)

    # Find all placeholders in the template
    used_attrs = _extract_placeholders(report_template)

    # Verify that no sensitive attributes are referenced
    if not used_attrs.issubset(ALLOWED_ATTRIBUTES):
        forbidden = used_attrs - ALLOWED_ATTRIBUTES
        raise ValueError(f"Unauthorized access to sensitive data: {', '.join(forbidden)}")

    # Build a safe mapping for formatting
    student_dict = {attr: getattr(student, attr) for attr in used_attrs}

    # Replace placeholders manually to avoid accidental format string exploits
    def replacer(match):
        attr = match.group(1)
        return str(student_dict[attr])

    safe_report = PLACEHOLDER_PATTERN.sub(replacer, report_template)
    return safe_report

# -----------------------------
# Example usage (for testing only)
# -----------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA}\n"
    )
    print(draft_student_report("S001", template))