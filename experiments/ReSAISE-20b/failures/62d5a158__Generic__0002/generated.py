import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
#  Student data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str  # sensitive

# ----------------------------------------------------------------------
#  In‑memory student database (for demonstration purposes)
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
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
        course="Mechanical Engineering",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late submission on project"
    ),
}

# ----------------------------------------------------------------------
#  Allowed and restricted attributes
# ----------------------------------------------------------------------
_ALLOWED_ATTRS = {"name", "course", "age", "gpa", "home_address"}
_RESTRICTED_ATTRS = {"disciplinary_record"}

# ----------------------------------------------------------------------
#  Helper: find placeholders in a template string
# ----------------------------------------------------------------------
_placeholder_pattern = re.compile(r"{([^{}]+)}")

def _extract_placeholders(template: str):
    """Return a set of attribute names referenced in the template."""
    return {
        match.group(1).strip()
        for match in _placeholder_pattern.finditer(template)
    }

# ----------------------------------------------------------------------
#  Main function
# ----------------------------------------------------------------------
def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generate a student report by filling the provided template with
    attributes from the Student object identified by stu_id.

    Parameters
    ----------
    stu_id : str
        Unique identifier for the student.
    summary_template : str
        Template containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If stu_id is not found or if the template references restricted data.
    """
    # 1. Validate student ID
    try:
        student = _STUDENT_DB[stu_id]
    except KeyError as exc:
        raise ValueError(f"Invalid student ID: {stu_id}") from exc

    # 2. Check for restricted attributes in the template
    placeholders = _extract_placeholders(summary_template)
    # The placeholder format is expected to be `student.<attr>`
    for ph in placeholders:
        if not ph.startswith("student."):
            raise ValueError(f"Invalid placeholder syntax: {ph}")
        attr_name = ph.split(".", 1)[1]
        if attr_name in _RESTRICTED_ATTRS:
            raise ValueError(f"Access to restricted attribute '{attr_name}' is prohibited.")
        if attr_name not in _ALLOWED_ATTRS:
            raise ValueError(f"Unknown attribute '{attr_name}' referenced in template.")

    # 3. Prepare the context for formatting
    context = {"student": student}

    try:
        report = summary_template.format(**context)
    except KeyError as exc:
        # This should not happen due to the earlier checks, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report