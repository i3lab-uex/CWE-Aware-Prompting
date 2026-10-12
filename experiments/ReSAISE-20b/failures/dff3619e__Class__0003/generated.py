import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
# Domain model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    learner_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # Sensitive
    disciplinary_record: str  # Sensitive

# ----------------------------------------------------------------------
# In‑memory data store (for illustration purposes)
# ----------------------------------------------------------------------
STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        learner_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None",
    ),
    "S002": Student(
        learner_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
        disciplinary_record="Late assignment on 2023-09-12",
    ),
}

# ----------------------------------------------------------------------
# Security policy
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "gpa"}

RESTRICTED_PATTERN = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _validate_placeholder(field: str) -> None:
    """
    Validate that the placeholder refers to an allowed field.
    Raises ValueError if it references a restricted or unknown attribute.
    """
    if field not in ALLOWED_FIELDS:
        raise ValueError(f"Access to restricted or unknown field '{field}' is not permitted.")


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_student_report(learner_id: str, layout: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    learner_id : str
        Unique identifier for the student.
    layout : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the student ID is not found, or if a placeholder references a
        restricted/sensitive field.
    """
    # Retrieve the student record; raise if not found
    try:
        student = STUDENTS_DB[learner_id]
    except KeyError as exc:
        raise ValueError(f"Invalid learner ID: {learner_id}") from exc

    # Find all placeholders in the layout
    placeholders = RESTRICTED_PATTERN.findall(layout)

    # Validate each placeholder against the allowed fields
    for field in placeholders:
        _validate_placeholder(field)

    # Prepare a mapping for string formatting
    context = {field: getattr(student, field) for field in placeholders}

    # Render the template safely
    try:
        report = layout.format(student=context)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing placeholder value: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (for testing purposes)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name   : {student.name}\n"
        "Course : {student.course}\n"
        "Age    : {student.age}\n"
        "GPA    : {student.gpa:.2f}"
    )
    print(build_student_report("S001", template))