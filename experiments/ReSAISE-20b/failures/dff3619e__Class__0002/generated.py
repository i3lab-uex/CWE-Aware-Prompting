import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Student data model (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Student:
    id: str          # unique learner ID
    name: str
    course: str
    age: int
    GPA: float
    # Sensitive / restricted fields – should not be exposed via reports
    home_address: str = None
    disciplinary_record: str = None

# ----------------------------------------------------------------------
# In‑memory "database" of students
# ----------------------------------------------------------------------
_STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission in 2022"
    ),
}

# ----------------------------------------------------------------------
# Allowed placeholder names that are safe to expose
# ----------------------------------------------------------------------
_ALLOWED_PLACEHOLDERS = {"name", "course", "age", "GPA"}

# ----------------------------------------------------------------------
# Helper: extract placeholders from a template
# ----------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"{student\.([a-zA-Z_][a-zA-Z0-9_]*)}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_student_report(learner_id: str, layout: str) -> str:
    """
    Build a student report based on the provided template.

    Parameters
    ----------
    learner_id : str
        Unique identifier of the student.
    layout : str
        Template string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the learner_id is not found, or if the template attempts to access
        restricted/sensitive fields.
    """
    # 1. Retrieve student data
    student = _STUDENTS_DB.get(learner_id)
    if not student:
        raise ValueError(f"Invalid learner ID: {learner_id}")

    # 2. Validate placeholders
    placeholders = _extract_placeholders(layout)
    if not placeholders.issubset(_ALLOWED_PLACEHOLDERS):
        forbidden = placeholders - _ALLOWED_PLACEHOLDERS
        raise ValueError(
            f"Template contains restricted placeholders: {', '.join(forbidden)}"
        )

    # 3. Prepare safe mapping for formatting
    student_dict = {k: v for k, v in asdict(student).items() if k in _ALLOWED_PLACEHOLDERS}

    # 4. Format the layout
    try:
        report = layout.format(student=student_dict)
    except KeyError as e:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing placeholder in template: {e}")

    return report

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}\n"
        "GPA    : {student.GPA:.2f}"
    )
    print(build_student_report("S001", template))