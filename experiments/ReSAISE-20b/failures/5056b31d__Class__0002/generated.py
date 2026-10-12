import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data model and storage (in‑memory for illustration)
# ----------------------------------------------------------------------
@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # sensitive
    discipline_record: str  # sensitive

# Example in‑memory database
_STUDENT_DB: Dict[str, Student] = {
    "s123": Student(
        student_id="s123",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "s456": Student(
        student_id="s456",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of assignment 2"
    ),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_student_by_id(student_id: str) -> Student:
    """Retrieve a student from the in‑memory DB."""
    try:
        return _STUDENT_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{student_id}' not found.") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_id : str
        The unique identifier for the student.
    template : str
        A format string that may contain placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the student is not found, if the template contains a reference to
        sensitive data (home_address or discipline_record), or if any other
        formatting error occurs.
    """
    # 1. Fetch the student object
    student = _get_student_by_id(student_id)

    # 2. Detect any attempt to access sensitive fields
    sensitive_fields = {"student.home_address", "student.discipline_record"}
    # Find all placeholders in the template
    placeholder_pattern = r"\{([^}]+)\}"
    for match in re.finditer(placeholder_pattern, template):
        placeholder = f"{{{match.group(1)}}}"
        if match.group(1) in sensitive_fields:
            raise ValueError(f"Access to sensitive field '{match.group(1)}' is not allowed.")

    # 3. Prepare a safe namespace for formatting
    safe_namespace = {
        "student": {
            "name": student.name,
            "course": student.course,
            "age": student.age,
            "gpa": student.gpa
        }
    }

    # 4. Render the template safely
    try:
        report = template.format(**safe_namespace)
    except KeyError as exc:
        raise ValueError(f"Template references unknown field: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to format template: {exc}") from exc

    return report