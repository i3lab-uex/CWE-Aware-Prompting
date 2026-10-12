import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Domain model
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Student:
    """
    Immutable representation of a student.
    Sensitive attributes are not exposed through the public API
    and will trigger a ValueError if accessed via the report template.
    """
    learner_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str  # Sensitive


# ------------------------------------------------------------------
# In‑memory data store (for demonstration purposes)
# ------------------------------------------------------------------

_STUDENT_DB: Dict[str, Student] = {
    "s123": Student(
        learner_id="s123",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "s456": Student(
        learner_id="s456",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
        disciplinary_record="Late submission of assignments"
    ),
}


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

_RE_PLACEHOLDER = re.compile(r"\{(?P<attr>[^}]+)\}")

# Attributes that are considered sensitive and must not be exposed
_SENSITIVE_ATTRS = {"disciplinary_record"}


def _get_student(learner_id: str) -> Student:
    """Retrieve a student from the store or raise ValueError."""
    try:
        return _STUDENT_DB[learner_id]
    except KeyError as exc:
        raise ValueError(f"Invalid learner_id: {learner_id}") from exc


def _resolve_placeholder(attr_path: str, student: Student) -> str:
    """
    Resolve a dotted attribute path on the student object.
    For this simple model, only single attributes are supported.
    """
    if "." in attr_path:
        raise ValueError(f"Nested attributes not allowed: {attr_path}")

    if attr_path in _SENSITIVE_ATTRS:
        raise ValueError(f"Access to restricted attribute '{attr_path}' is prohibited")

    if not hasattr(student, attr_path):
        raise ValueError(f"Student has no attribute '{attr_path}'")

    value = getattr(student, attr_path)
    return str(value)


# ------------------------------------------------------------------
# Main API
# ------------------------------------------------------------------

def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a report for the student identified by `learner_id`
    using the provided `layout` template.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID is invalid, if a restricted attribute is accessed,
        or if the template contains unsupported syntax.
    """
    # Ensure that placeholders are prefixed with 'student.'
    for match in _RE_PLACEHOLDER.finditer(layout):
        placeholder = match.group("attr")
        if not placeholder.startswith("student."):
            raise ValueError(f"Unsupported placeholder format: {{{placeholder}}}")

        attr_name = placeholder[len("student.") :]
        student = _get_student(learner_id)
        replacement = _resolve_placeholder(attr_name, student)

        # Replace the placeholder in the layout
        layout = layout.replace(f"{{{placeholder}}}", replacement, 1)

    return layout


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
    )
    print(build_student_report("s123", template))