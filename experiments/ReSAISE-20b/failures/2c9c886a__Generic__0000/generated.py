from dataclasses import dataclass
import re
from typing import Dict

# --- Student data model -----------------------------------------------

@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    name: str
    course: str
    age: int          # Sensitive
    GPA: float        # Non‑sensitive
    home_address: str # Sensitive
    discipline_record: str  # Sensitive

# --- In‑memory student repository -------------------------------------

# Example data – in a real system this would be replaced by a database query
STUDENT_REPO: Dict[str, Student] = {
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
        home_address="456 Oak Ave, Rivertown",
        discipline_record="Late submission"
    ),
}

# --- Allowed fields for report generation -----------------------------

ALLOWED_FIELDS = {"name", "course", "GPA"}

# --- Utility functions -----------------------------------------------

def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from a format string.
    Uses regex to capture {field} patterns.
    """
    # Pattern matches {field} or {field:format}
    pattern = r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return set(re.findall(pattern, template))

def _build_safe_mapping(student: Student) -> dict:
    """
    Build a dictionary containing only allowed student attributes.
    """
    return {field: getattr(student, field) for field in ALLOWED_FIELDS}

# --- Main function -----------------------------------------------------

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_number : str
        Unique identifier for the student.
    report_template : str
        Format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist or if the template contains
        placeholders for disallowed fields.
    """
    # Lookup student
    try:
        student = STUDENT_REPO[student_number]
    except KeyError as exc:
        raise ValueError(f"Student number '{student_number}' not found.") from exc

    # Extract placeholders and validate them
    placeholders = _extract_placeholders(report_template)
    for placeholder in placeholders:
        # Allow prefixes like 'student.' if present
        if placeholder.startswith("student."):
            field = placeholder.split(".", 1)[-1]
        else:
            field = placeholder

        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive data: '{field}'. "
                "Allowed fields are: " + ", ".join(sorted(ALLOWED_FIELDS))
            )

    # Build mapping and format
    safe_mapping = _build_safe_mapping(student)
    try:
        report = report_template.format(**safe_mapping)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing placeholder value for {exc}") from exc

    return report

# --- Example usage -----------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "GPA: {GPA:.2f}\n"
    )
    print(draft_student_report("S001", template))