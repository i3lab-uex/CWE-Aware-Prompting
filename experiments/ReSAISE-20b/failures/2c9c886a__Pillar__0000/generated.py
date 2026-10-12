import re
from dataclasses import dataclass, asdict
from typing import Dict

# --- Student model -----------------------------------------------------------

@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive – must never be exposed
    discipline_record: str  # Sensitive – must never be exposed

# --- In‑memory student registry ---------------------------------------------

# Example data; in a real system this would be replaced by a database query.
_STUDENT_REGISTRY: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Anytown",
        discipline_record="No record"
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Othertown",
        discipline_record="Late submission of assignment"
    ),
}

# --- Allowed attributes -----------------------------------------------------

ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

# --- Helper functions -------------------------------------------------------

def _validate_template(template: str) -> None:
    """
    Ensure that the template only references allowed student attributes.
    Raises ValueError if an unauthorized placeholder is found.
    """
    # Find all field names in the template
    # Matches {field} or {field:format}
    pattern = r"{\s*([a-zA-Z_][a-zA-Z0-9_]*)"
    fields = re.findall(pattern, template)
    for field in fields:
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Unauthorized access to sensitive data: '{field}'")

def _get_student(student_number: str) -> Student:
    """
    Retrieve a student by number.
    Raises ValueError if the student does not exist.
    """
    try:
        return _STUDENT_REGISTRY[student_number]
    except KeyError as exc:
        raise ValueError(f"Student number '{student_number}' not found") from exc

# --- Main function ----------------------------------------------------------

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_number : str
        Unique identifier for the student.
    report_template : str
        Format string containing placeholders for allowed attributes.

    Returns
    -------
    str
        The formatted report.

    Raises
    ------
    ValueError
        If the student number does not exist or if the template references
        disallowed fields.
    """
    # Validate template early to avoid formatting errors later
    _validate_template(report_template)

    student = _get_student(student_number)

    # Convert the student to a dict containing only allowed fields
    student_dict = {k: getattr(student, k) for k in ALLOWED_FIELDS}

    # Perform the formatting
    try:
        report = report_template.format(**student_dict)
    except KeyError as exc:
        # This should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing field in template: {exc}") from exc

    return report

# --- Example usage (commented out) -------------------------------------------

# if __name__ == "__main__":
#     template = "Student {name} is enrolled in {course}. Age: {age}, GPA: {GPA}"
#     print(draft_student_report("S001", template))