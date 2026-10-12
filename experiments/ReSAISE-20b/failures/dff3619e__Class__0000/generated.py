import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Student model (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str          # Sensitive
    disciplinary_record: str  # Sensitive


# ----------------------------------------------------------------------
# In‑memory "database" of students
# ----------------------------------------------------------------------
_STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission"
    ),
}


# ----------------------------------------------------------------------
# Report builder
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

_PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def build_student_report(learner_id: str, layout: str) -> str:
    """
    Build a student report from a template.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the student ID is not found or if a placeholder refers to a
        restricted/sensitive attribute.
    """
    # ------------------------------------------------------------------
    # Validate student ID
    # ------------------------------------------------------------------
    if learner_id not in _STUDENTS_DB:
        raise ValueError(f"Invalid student ID: {learner_id}")

    student = _STUDENTS_DB[learner_id]

    # ------------------------------------------------------------------
    # Resolve placeholders
    # ------------------------------------------------------------------
    def _replace(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted or unknown field '{field_name}' is not permitted."
            )
        value = getattr(student, field_name)
        return str(value)

    try:
        report = _PLACEHOLDER_RE.sub(_replace, layout)
    except re.error as exc:
        raise ValueError(f"Invalid template syntax: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}"
    )
    print(build_student_report("S001", template))