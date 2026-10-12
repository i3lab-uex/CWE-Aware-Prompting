import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
#  Student data model and simple in‑memory repository
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student with basic profile and academic data."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str  # considered sensitive

# In‑memory storage – in a real system this would be replaced by a database
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission on Project X"
    ),
}

# --------------------------------------------------------------------------- #
#  Template rendering with security checks
# --------------------------------------------------------------------------- #

_ALLOWED_ATTRIBUTES = {
    "name",
    "course",
    "age",
    "gpa",
    "home_address"
}

_TEMPLATE_VAR_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_template_vars(template: str) -> set:
    """Return a set of attribute names referenced in the template."""
    return {match.group(1) for match in _TEMPLATE_VAR_RE.finditer(template)}

def _render_template(student: Student, template: str) -> str:
    """
    Render the template safely. Only allowed attributes may be accessed.
    Raises ValueError if a disallowed attribute is requested.
    """
    # Validate all placeholders
    for attr in _extract_template_vars(template):
        if attr not in _ALLOWED_ATTRIBUTES:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed.")

    # Build a mapping for formatting
    safe_dict = {attr: getattr(student, attr) for attr in _ALLOWED_ATTRIBUTES}
    try:
        return template.format(**{"student": safe_dict})
    except KeyError as exc:
        raise ValueError(f"Missing attribute in student data: {exc}") from None

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report by filling in the provided template with
    data from the specified student.

    Parameters
    ----------
    stu_id : str
        Unique identifier of the student.
    summary_template : str
        Template containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID is unknown or if the template requests a
        restricted attribute.
    """
    # Validate input
    if not isinstance(stu_id, str) or not stu_id:
        raise ValueError("Student ID must be a non-empty string.")

    student = _STUDENT_DB.get(stu_id)
    if student is None:
        raise ValueError(f"Student ID '{stu_id}' not found.")

    # Render the template safely
    return _render_template(student, summary_template)

# --------------------------------------------------------------------------- #
#  Example usage (commented out – remove to run)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}"
    )
    print(create_student_summary("S001", template))