import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------
# Dummy student store (would normally be a database or similar)
# ------------------------------------------------------------
@dataclass
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    # Sensitive fields that must never be exposed in a report
    home_address: str = field(repr=False)
    discipline_record: str = field(repr=False)

# In‑memory registry of students
_STUDENT_REGISTRY: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Townsville",
        discipline_record="No violations"
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Jones",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Villagetown",
        discipline_record="Late submission"
    ),
}

# ------------------------------------------------------------
# Report generation
# ------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_number : str
        Unique identifier of the student.
    report_template : str
        Template string containing placeholders such as `{name}` or `{course}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist, or if the template references a disallowed field.
    """
    # Retrieve the student record
    student = _STUDENT_REGISTRY.get(student_number)
    if not student:
        raise ValueError(f"Student with number '{student_number}' does not exist.")

    # Build a mapping of allowed attributes
    student_dict = {field: getattr(student, field) for field in ALLOWED_FIELDS}

    # Validate that the template only references allowed fields
    placeholders = PLACEHOLDER_RE.findall(report_template)
    for field in placeholders:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive or unknown field '{field}'. "
                "Only the following fields are allowed: "
                f"{', '.join(sorted(ALLOWED_FIELDS))}."
            )

    # Perform the substitution safely
    try:
        report = report_template.format(**student_dict)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing field in report template: {exc}") from exc

    return report