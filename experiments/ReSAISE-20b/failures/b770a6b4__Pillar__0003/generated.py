import re
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data model -------------------------------------------------------------
# ----------------------------------------------------------------------
@dataclass
class Student:
    """Represents a student record."""
    code: str
    name: str
    course: str
    age: int
    gpa: float
    address: str
    # Sensitive field that should not be exposed via templates
    disciplinary_record: Dict[str, str] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Simulated persistent storage ------------------------------------------
# ----------------------------------------------------------------------
class StudentDB:
    """
    Context‑manager that simulates a database connection.
    The connection is opened on __enter__ and closed on __exit__,
    ensuring proper resource handling (CWE‑664).
    """
    _students: Dict[str, Student] = {}

    def __init__(self):
        self._connected = False

    def __enter__(self) -> "StudentDB":
        # Simulate opening a database connection
        self._connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Simulate closing the database connection
        self._connected = False

    def add_student(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError("Only Student instances can be added.")
        self._students[student.code] = student

    def get_student(self, code: str) -> Student:
        if not self._connected:
            raise RuntimeError("Database connection is closed.")
        try:
            return self._students[code]
        except KeyError as exc:
            raise ValueError(f"Student with code '{code}' not found.") from exc


# ----------------------------------------------------------------------
# Template processing ----------------------------------------------------
# ----------------------------------------------------------------------
_RE_PLACEHOLDER = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

# List of attributes that are considered sensitive
_RESTRICTED_ATTRS = {"disciplinary_record", "address"}

def _validate_template(template: str):
    """
    Validates that the template only contains allowed placeholders.
    Raises ValueError if a restricted attribute is referenced.
    """
    for match in _RE_PLACEHOLDER.finditer(template):
        attr = match.group(1)
        if attr in _RESTRICTED_ATTRS:
            raise ValueError(
                f"Access to restricted attribute '{attr}' is not allowed in the template."
            )
    # If no placeholders, nothing to validate further


def _render_template(template: str, student: Student) -> str:
    """
    Renders the template using only the allowed attributes of the student.
    """
    def replacer(match):
        attr = match.group(1)
        return str(getattr(student, attr))

    return _RE_PLACEHOLDER.sub(replacer, template)


# ----------------------------------------------------------------------
# Public API -------------------------------------------------------------
# ----------------------------------------------------------------------
def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generates a student report based on the supplied template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for the student.
    profile_template : str
        Template string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the student ID is invalid or if the template attempts to access
        restricted attributes.
    """
    _validate_template(profile_template)

    # Use the context manager to ensure proper resource handling
    with StudentDB() as db:
        student = db.get_student(learner_code)

    return _render_template(profile_template, student)


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module) ----------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup example data
    db = StudentDB()
    with db:
        db.add_student(
            Student(
                code="S123",
                name="Alice Johnson",
                course="Computer Science",
                age=21,
                gpa=3.8,
                address="123 Maple St, Springfield",
                disciplinary_record={"lateness": "3 instances"},
            )
        )

    # Define a template
    tmpl = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
    )

    # Generate report
    print(compile_student_profile("S123", tmpl))