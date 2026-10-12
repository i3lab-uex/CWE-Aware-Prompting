import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    gpa: float
    # Sensitive fields – should never be exposed via the report template
    home_address: str
    discipline_record: str

# ----------------------------------------------------------------------
# In‑memory "database" – in a real system this would be replaced by
# persistent storage (e.g. SQL, NoSQL, or an external API)
# ----------------------------------------------------------------------
STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        student_id="s001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "s002": Student(
        student_id="s002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Metropolis",
        discipline_record="Late submission in 2023-01",
    ),
}

# ----------------------------------------------------------------------
# Allowed attributes for templating
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "gpa"}

def _extract_placeholders(template: str) -> set[str]:
    """
    Extracts all placeholders of the form `{student.<field>}` from the template.
    Raises ValueError if a placeholder does not follow the expected format
    or refers to a disallowed field.
    """
    pattern = r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    matches = re.findall(pattern, template)
    placeholders = set(matches)

    # Detect disallowed or unknown fields
    for field in placeholders:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Template references disallowed or unknown field: '{field}'. "
                "Only the following fields are permitted: "
                f"{', '.join(sorted(ALLOWED_FIELDS))}."
            )
    return placeholders

def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a report string for the given student based on the provided template.

    Parameters
    ----------
    student_id : str
        The unique identifier for a student.
    template : str
        Template string containing placeholders of the form `{student.<field>}`.

    Returns
    -------
    str
        The report string with placeholders replaced by the student's data.

    Raises
    ------
    ValueError
        If the student does not exist, if the template contains disallowed fields,
        or if any other unexpected error occurs.
    """
    # Retrieve student record
    try:
        student = STUDENT_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{student_id}' not found.") from exc

    # Validate template placeholders
    try:
        placeholders = _extract_placeholders(template)
    except ValueError as exc:
        raise

    # Build a mapping for formatting
    data = {field: getattr(student, field) for field in placeholders}

    # Safely perform formatting
    try:
        report = template.format(student=data)
    except Exception as exc:
        raise ValueError(f"Error while formatting the template: {exc}") from exc

    return report