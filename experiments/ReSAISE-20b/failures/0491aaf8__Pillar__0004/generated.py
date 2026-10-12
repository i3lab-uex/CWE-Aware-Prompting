import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Domain model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Represents a student in the academic system."""
    name: str
    course: str
    age: int
    GPA: float            # Sensitive
    home_address: str     # Sensitive
    discipline_record: str

# ----------------------------------------------------------------------
# In‑memory storage (in a real system this would be a database)
# ----------------------------------------------------------------------
STUDENTS_DB: Dict[str, Student] = {
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
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission"
    ),
}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
PLACEHOLDER_REGEX = re.compile(r"{student\.([a-zA-Z_][a-zA-Z0-9_]*)}")

SENSITIVE_FIELDS = {"GPA", "home_address"}

def _extract_placeholders(template: str) -> set:
    """Return a set of attribute names referenced in the template."""
    return {match.group(1) for match in PLACEHOLDER_REGEX.finditer(template)}

def _validate_placeholders(placeholders: set):
    """Ensure no sensitive data is requested."""
    for field in placeholders:
        if field in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{field}' is prohibited.")
        if not hasattr(Student, field):
            raise ValueError(f"Unknown student attribute '{field}'.")

# ----------------------------------------------------------------------
# Main API
# ----------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a formatted student report based on the provided template.

    Parameters
    ----------
    id : str
        Unique identifier for the student.
    format_string : str
        A template containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student id is unknown, a placeholder references sensitive data,
        or an unknown attribute is requested.
    """
    # Retrieve the student; raise if not found
    student = STUDENTS_DB.get(id)
    if student is None:
        raise ValueError(f"Student with id '{id}' does not exist.")

    # Parse and validate placeholders
    placeholders = _extract_placeholders(format_string)
    _validate_placeholders(placeholders)

    # Perform formatting safely
    try:
        report = format_string.format(student=student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Formatting error: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (for manual testing only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Discipline Record: {student.discipline_record}"
    )
    print(create_student_summary("S001", tmpl))