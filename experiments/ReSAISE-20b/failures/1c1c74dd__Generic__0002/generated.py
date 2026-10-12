import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
# 1.  Student data model and a tiny in‑memory store
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str

# Example in‑memory database (replace with real DB look‑ups as needed)
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2023-04-12"
    ),
}

# --------------------------------------------------------------------------- #
# 2.  Helper: check for disallowed placeholders
# --------------------------------------------------------------------------- #

_DISALLOWED_FIELDS = {"GPA", "home_address"}

_PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _validate_template(template: str) -> None:
    """
    Raises ValueError if the template tries to access a disallowed field.
    """
    for match in _PLACEHOLDER_RE.finditer(template):
        field = match.group(1)
        if field in _DISALLOWED_FIELDS:
            raise ValueError(
                f"Access to sensitive field '{field}' is not permitted in the template."
            )

# --------------------------------------------------------------------------- #
# 3.  Main function
# --------------------------------------------------------------------------- #

def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a student report using the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    custom_template : str
        A format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID is unknown or if the template references a disallowed field.
    """
    # 3.1 Validate that student exists
    student = _STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # 3.2 Validate template
    _validate_template(custom_template)

    # 3.3 Prepare the namespace for formatting
    # Convert dataclass to dict but expose only safe fields
    student_dict = {k: v for k, v in asdict(student).items() if k not in _DISALLOWED_FIELDS}

    # 3.4 Perform the formatting
    try:
        report = custom_template.format(student=student_dict)
    except KeyError as exc:
        raise ValueError(f"Template contains an unknown placeholder: {exc}") from None

    return report