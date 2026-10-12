import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Student data model and in‑memory storage
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    id: str
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)            # sensitive
    home_address: str = field(repr=False)     # sensitive
    discipline_record: str = ""


# Simulated database (in a real system this would be replaced by a proper DB)
STUDENTS_DB: Dict[str, Student] = {
    "s123": Student(
        id="s123",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.9,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "s456": Student(
        id="s456",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.6,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission"
    ),
}


# --------------------------------------------------------------------------- #
# 2. Helper functions
# --------------------------------------------------------------------------- #

def _get_student(student_id: str) -> Student:
    """Retrieve a student by ID, raising ValueError if not found."""
    try:
        return STUDENTS_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student ID '{student_id}' does not exist.") from exc


def _validate_template(template: str) -> None:
    """
    Ensure that the template does not reference sensitive attributes.
    Sensitive fields are: gpa, home_address
    """
    # Find all placeholders of the form {student.<field>}
    placeholders = re.findall(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}", template)
    sensitive = {"gpa", "home_address"}
    if any(field in sensitive for field in placeholders):
        raise ValueError(f"Template references sensitive attribute(s): "
                         f"{', '.join(set(placeholders) & sensitive)}")


def _render_template(template: str, student: Student) -> str:
    """
    Render the template with the student's attributes.
    Only public fields are allowed. The function uses a safe mapping.
    """
    # Create a dictionary of non‑sensitive attributes
    allowed_attrs = {
        k: v for k, v in student.__dict__.items()
        if k not in {"gpa", "home_address"}
    }

    # Build a context dict for format_map
    class SafeDict(dict):
        def __missing__(self, key):
            # If the key is missing (e.g., typo), leave placeholder unchanged
            return f"{{student.{key}}}"

    context = SafeDict(**allowed_attrs)

    try:
        return template.format_map(context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc


# --------------------------------------------------------------------------- #
# 3. Public API
# --------------------------------------------------------------------------- #

def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report using the provided template.

    Parameters
    ----------
    id : str
        Unique identifier of the student.
    format_string : str
        Template containing placeholders like '{student.name}'.

    Returns
    -------
    str
        Formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if the template references sensitive data.
    """
    # Validate input
    _validate_template(format_string)

    # Retrieve student record
    student = _get_student(id)

    # Render the template
    return _render_template(format_string, student)


# --------------------------------------------------------------------------- #
# 4. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = "Student {student.name} (ID: {student.id}) is enrolled in {student.course}, age {student.age}."
#     print(create_student_summary("s123", tmpl))