import string
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Student model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)
    home_address: str = field(repr=False)
    discipline_record: str

# ----------------------------------------------------------------------
# In‑memory store of students (for demo purposes)
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of assignments"
    ),
}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _extract_placeholders(template: str):
    """Return a set of placeholder names used in the template."""
    formatter = string.Formatter()
    placeholders = set()
    for _, field_name, _, _ in formatter.parse(template):
        if field_name:
            # Support nested attributes like 'student.name'
            parts = field_name.split(".")
            placeholders.add(parts[0])  # we only care about the top‑level object
    return placeholders

def _validate_template(template: str):
    """Ensure the template does not reference disallowed attributes."""
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(template):
        if not field_name:
            continue
        # Field may be 'student.attribute' or just 'attribute'
        if field_name.startswith("student."):
            attr = field_name.split(".", 1)[1]
        else:
            attr = field_name

        if attr in {"gpa", "home_address"}:
            raise ValueError(
                f"Access to sensitive attribute '{attr}' is prohibited in the template."
            )

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student profile based on the provided template.

    Parameters
    ----------
    unique_id : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders such as '{student.name}' or
        '{student.course}'.  Placeholders for sensitive fields (e.g. GPA,
        home_address) are disallowed.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the `unique_id` does not exist or if the template references
        sensitive attributes.
    """
    # Retrieve student
    try:
        student = _STUDENT_DB[unique_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{unique_id}' not found.") from exc

    # Validate template for forbidden fields
    _validate_template(report_template)

    # Perform formatting
    try:
        report = report_template.format(student=student)
    except Exception as exc:
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report