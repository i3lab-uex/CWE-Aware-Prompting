import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Mock Student database (in a real system this would be replaced with
# secure persistence, authentication and authorization layers)
# ------------------------------------------------------------------
@dataclass
class Student:
    token: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)   # sensitive
    discipline_record: str = field(repr=False)  # sensitive


# In‑memory store of students keyed by their token
_STUDENT_DB: Dict[str, Student] = {
    "abc123": Student(
        token="abc123",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Main St, Anytown",
        discipline_record="No infractions"
    ),
    "def456": Student(
        token="def456",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Othertown",
        discipline_record="Late submission"
    ),
}


# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------
def _get_student(token: str) -> Student:
    """
    Retrieve a student by token. Raise ValueError if not found.
    """
    student = _STUDENT_DB.get(token)
    if not student:
        raise ValueError(f"Student token '{token}' does not exist.")
    return student


def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive fields.
    Allowed placeholders: student.name, student.course, student.age, student.gpa
    """
    # Find all placeholders of the form {student.<field>}
    placeholders = re.findall(r"\{student\.([a-zA-Z_]+)\}", template)
    sensitive = {"home_address", "discipline_record"}
    for field in placeholders:
        if field in sensitive:
            raise ValueError(f"Unauthorized access to sensitive data: '{field}'")


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report from the provided template.

    Parameters
    ----------
    student_token : str
        Unique identifier for the student.
    report_template : str
        Format string containing placeholders like {student.name}.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token is invalid or if the template tries to access
        sensitive student data.
    """
    # Validate token and retrieve student
    student = _get_student(student_token)

    # Ensure template does not expose sensitive data
    _validate_template(report_template)

    # Build a context dictionary for formatting
    context = {
        "student": {
            "name": student.name,
            "course": student.course,
            "age": student.age,
            "gpa": student.gpa
        }
    }

    try:
        # Use str.format with nested dict access via a custom class
        class StudentContext(dict):
            def __missing__(self, key):
                # Provide nested dict access
                if key == "student":
                    return context["student"]
                raise KeyError(key)

        formatted_report = report_template.format(**StudentContext())
    except Exception as exc:
        raise ValueError(f"Failed to format report: {exc}") from exc

    return formatted_report