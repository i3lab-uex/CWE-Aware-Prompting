import re
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Student data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    gpa: float
    home_address: str          # considered sensitive
    disciplinary_record: str   # considered sensitive

# ----------------------------------------------------------------------
# In‑memory database (for demonstration purposes)
# ----------------------------------------------------------------------
STUDENT_DB = {
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
        home_address="456 Oak Ave, Springfield",
        disciplinary_record="Late submission"
    ),
}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "gpa"}
RESTRICTED_FIELDS = {"home_address", "disciplinary_record"}

PLACEHOLDER_REGEX = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str):
    """Return a set of placeholder names found in the template."""
    return {m.group(1) for m in PLACEHOLDER_REGEX.finditer(template)}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report by filling in the placeholders of
    *summary_template* with data from the specified student.

    Parameters
    ----------
    stu_id : str
        Unique identifier of a student.
    summary_template : str
        A template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The fully formatted student report.

    Raises
    ------
    ValueError
        If the *stu_id* is not found, or if the template tries to access a
        restricted field (e.g., `home_address`).
    """
    # Validate student ID
    if stu_id not in STUDENT_DB:
        raise ValueError(f"Invalid student ID: {stu_id}")

    student = STUDENT_DB[stu_id]

    # Find placeholders in the template
    placeholders = _extract_placeholders(summary_template)

    # Check for restricted or unknown fields
    for field in placeholders:
        if field in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Unknown placeholder '{field}' in template.")

    # Build a mapping for formatting
    data_map = {f"student.{k}": getattr(student, k) for k in ALLOWED_FIELDS}

    # Perform the substitution
    try:
        result = summary_template.format(**data_map)
    except KeyError as exc:
        # Should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return result