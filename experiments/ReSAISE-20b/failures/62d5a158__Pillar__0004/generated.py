import re
from dataclasses import dataclass

# --------------------------------------------------------------------------- #
#   Student data model and in‑memory repository
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    stu_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # considered sensitive
    disciplinary_record: str  # considered sensitive


# In‑memory storage of students keyed by their ID.
# In a real system this would be replaced with a database or external service.
STUDENT_REPO = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
        disciplinary_record="Late submission of assignment 3"
    ),
}

# --------------------------------------------------------------------------- #
#   Helper for safe template formatting
# --------------------------------------------------------------------------- #

_ALLOWED_ATTRS = {"name", "course", "age", "gpa"}

_PLACEHOLDER_RE = re.compile(r"\{([^\}]+)\}")

def _extract_placeholders(template: str):
    """Return a set of attribute names used in the template."""
    return {match.group(1).strip() for match in _PLACEHOLDER_RE.finditer(template)}

def _safe_format(student: Student, template: str) -> str:
    """
    Format the template using only allowed attributes of the student.
    Raises ValueError if a forbidden attribute is requested or the template
    contains invalid syntax.
    """
    placeholders = _extract_placeholders(template)

    # Ensure all placeholders refer to allowed attributes
    for attr in placeholders:
        if attr not in _ALLOWED_ATTRS:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed")

    # Build a mapping for formatting
    context = {attr: getattr(student, attr) for attr in placeholders}
    try:
        return template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing attribute in student data: {exc}") from None
    except Exception as exc:
        # Catch all formatting errors (e.g., bad syntax)
        raise ValueError(f"Template formatting error: {exc}") from None

# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report by filling the provided template with
    the student's data.

    Parameters:
        stu_id (str): Unique identifier of the student.
        summary_template (str): Template containing placeholders
            such as '{name}' or '{course}'.

    Returns:
        str: The formatted student report.

    Raises:
        ValueError: If the student ID is invalid, or if the template
            tries to access restricted attributes.
    """
    # Validate student ID and retrieve data
    if not isinstance(stu_id, str) or stu_id == "":
        raise ValueError("Student ID must be a non-empty string")

    student = STUDENT_REPO.get(stu_id)
    if student is None:
        raise ValueError(f"Student ID '{stu_id}' not found")

    # Safely format the template
    return _safe_format(student, summary_template)

# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     template = "Student {name} is enrolled in {course}. Age: {age}, GPA: {gpa}"
#     print(create_student_summary("S001", template))