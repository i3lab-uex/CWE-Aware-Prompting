import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Dummy in-memory student store (replace with real database access)
# ------------------------------------------------------------------
@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)      # sensitive
    discipline_record: str = field(repr=False)  # sensitive

# Sample data for demonstration purposes
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023"
    ),
}

# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {"student.name", "student.course", "student.age", "student.gpa"}

def _get_student(student_id: str) -> Student:
    """Retrieve a student by ID, raising ValueError if not found."""
    try:
        return _STUDENT_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{student_id}' not found.") from exc

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholders found in the template."""
    # Matches {student.field}
    return set(re.findall(r"\{([^{}]+)\}", template))

def _validate_placeholders(placeholders: set):
    """Ensure that all placeholders are allowed."""
    for ph in placeholders:
        if ph not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive or unknown field '{ph}' is not allowed.")

def _prepare_context(student: Student) -> Dict[str, str]:
    """Create a context dictionary for formatting."""
    return {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": str(student.age),
        "student.gpa": f"{student.gpa:.2f}",
    }

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_id : str
        The unique identifier of the student.
    template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student is not found or if a placeholder references sensitive
        or unknown data.
    """
    # Retrieve student record
    student = _get_student(student_id)

    # Validate placeholders for security
    placeholders = _extract_placeholders(template)
    _validate_placeholders(placeholders)

    # Prepare context for formatting
    context = _prepare_context(student)

    try:
        report = template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation
        raise ValueError(f"Missing placeholder in context: {exc}") from exc

    return report