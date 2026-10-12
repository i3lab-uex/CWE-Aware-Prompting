import re
from dataclasses import dataclass
from typing import Dict

# ---------- Student model ----------
@dataclass
class Student:
    """Simple student data holder."""
    stu_id: str
    name: str
    course: str
    age: int          # sensitive
    gpa: float        # sensitive
    address: str      # sensitive
    disciplinary_record: str  # sensitive

# ---------- Sample data store ----------
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        address="123 Main St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        address="456 Oak Ave, Springfield",
        disciplinary_record="Late assignment"
    ),
}

# ---------- Summary generation ----------
_ALLOWED_FIELDS = {"name", "course"}

_PLACEHOLDER_RE = re.compile(r"\{student\.([^\}]+)\}")

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report based on the supplied template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    summary_template : str
        Template containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The populated report string.

    Raises
    ------
    ValueError
        If the student ID is unknown, or if the template references a restricted attribute.
    """
    # Validate and retrieve student
    student = STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Invalid student ID: {stu_id}")

    # Scan the template for placeholders and validate each
    for match in _PLACEHOLDER_RE.finditer(summary_template):
        field = match.group(1).strip()
        if field not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Attempt to expose restricted or sensitive field '{field}'. "
                "Only 'name' and 'course' are allowed."
            )

    # Perform safe formatting
    try:
        report = summary_template.format(student=student)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing field in template: {exc}") from exc

    return report