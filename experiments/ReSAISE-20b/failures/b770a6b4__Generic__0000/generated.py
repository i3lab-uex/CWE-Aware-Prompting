import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Student data model and a mock in‑memory database
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student with personal and academic information."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    # This field is considered sensitive and must not be exposed via templates.
    disciplinary_record: str = field(repr=False, compare=False)

# Mock database of students keyed by learner_code.
_STUDENT_DB: Dict[str, Student] = {
    "S123": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="No record"
    ),
    "S456": Student(
        name="Bob Smith",
        course="Mechanical Engineering",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Rivertown",
        disciplinary_record="Late submission in 2022"
    ),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _fetch_student(learner_code: str) -> Student:
    """Retrieve a student from the mock database."""
    try:
        return _STUDENT_DB[learner_code]
    except KeyError as exc:
        raise ValueError(f"Invalid learner code: {learner_code}") from exc

def _render_template(template: str, student: Student) -> str:
    """
    Replace placeholders in the form {student.attribute} with actual student data.
    Raises ValueError if a restricted attribute is requested or the placeholder
    syntax is malformed.
    """
    # Pattern matches {student.<attribute>}
    pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

    def _replace(match: re.Match) -> str:
        attr = match.group(1)
        # Disallow access to sensitive fields
        if attr == "disciplinary_record":
            raise ValueError("Access to 'disciplinary_record' is restricted.")
        # Ensure the attribute exists
        if not hasattr(student, attr):
            raise ValueError(f"Unknown student attribute: '{attr}'")
        value = getattr(student, attr)
        return str(value)

    try:
        rendered = pattern.sub(_replace, template)
    except re.error as exc:
        raise ValueError("Invalid placeholder syntax in the template.") from exc

    return rendered

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by substituting placeholders in the provided template.

    Parameters
    ----------
    learner_code : str
        Unique identifier for the student.
    profile_template : str
        Template containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The rendered report with all placeholders replaced by student data.

    Raises
    ------
    ValueError
        If the learner code is unknown, a restricted attribute is accessed,
        or the template contains invalid placeholders.
    """
    student = _fetch_student(learner_code)
    return _render_template(profile_template, student)

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}\n"
        "Address: {student.home_address}\n"
    )
    print(compile_student_profile("S123", template))