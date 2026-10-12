import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Student data model (simplified for this example)
# ----------------------------------------------------------------------
@dataclass
class Student:
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str  # Sensitive; should not be exposed

# ----------------------------------------------------------------------
# In‑memory "database" of students
# ----------------------------------------------------------------------
STUDENTS: Dict[str, Student] = {
    "S001": Student(
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "S002": Student(
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission of assignments"
    ),
    # Add more students as needed
}

# ----------------------------------------------------------------------
# Allowed attributes that may appear in the template
# ----------------------------------------------------------------------
ALLOWED_ATTRIBUTES = {"student.name", "student.course", "student.age",
                      "student.gpa", "student.home_address"}

# ----------------------------------------------------------------------
# Utility to safely extract placeholders from the template
# ----------------------------------------------------------------------
_PLACEHOLDER_REGEX = re.compile(r"\{([^}]+)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1).strip() for match in _PLACEHOLDER_REGEX.finditer(template)}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for the student.
    summary_template : str
        Template string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the student ID is invalid, or if a placeholder references a
        restricted/sensitive attribute.
    """
    # Validate student ID
    if stu_id not in STUDENTS:
        raise ValueError(f"Invalid student ID: {stu_id}")

    student = STUDENTS[stu_id]

    # Find placeholders
    placeholders = _extract_placeholders(summary_template)

    # Check for restricted attributes
    for placeholder in placeholders:
        if placeholder not in ALLOWED_ATTRIBUTES:
            raise ValueError(
                f"Access to restricted attribute '{placeholder}' is not allowed."
            )

    # Prepare a mapping for formatting
    context = {
        "student.name": student.name,
        "student.course": student.course,
        "student.age": str(student.age),
        "student.gpa": f"{student.gpa:.2f}",
        "student.home_address": student.home_address,
    }

    # Render the template
    try:
        rendered = summary_template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder data: {exc}") from None

    return rendered