import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------
# Mock database (in a real system this would be replaced by actual DB calls)
# --------------------------------------------------------------------

@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive

# Example data store
_STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        student_id="s001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "s002": Student(
        student_id="s002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission on 2023-08-15",
    ),
}

# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _get_student(student_id: str) -> Student:
    """Retrieve a student from the mock database."""
    try:
        return _STUDENT_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{student_id}' not found.") from exc

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a report string for the given student based on the provided template.

    Parameters
    ----------
    student_id : str
        The unique identifier for the student.
    template : str
        A string containing placeholders like `{student.name}` or `{student.course}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student is not found, if the template contains disallowed fields,
        or if any other error occurs during formatting.
    """
    # Fetch student data
    student = _get_student(student_id)

    # Allowed fields (excluding sensitive ones)
    allowed_fields = {
        "name",
        "course",
        "age",
        "GPA",
    }

    # Regular expression to find all placeholders in the template
    placeholder_pattern = re.compile(r"{student\.([a-zA-Z_][a-zA-Z0-9_]*)}")

    # Extract field names from the template
    fields_in_template = set(match.group(1) for match in placeholder_pattern.finditer(template))

    # Validate fields
    if not fields_in_template.issubset(allowed_fields):
        disallowed = fields_in_template - allowed_fields
        raise ValueError(
            f"Template contains disallowed or sensitive fields: {', '.join(sorted(disallowed))}"
        )

    # Prepare mapping for formatting
    student_dict = {field: getattr(student, field) for field in allowed_fields}

    # Perform formatting
    try:
        report = placeholder_pattern.sub(
            lambda m: str(student_dict[m.group(1)]), template
        )
    except Exception as exc:
        raise ValueError(f"Error while formatting report: {exc}") from exc

    return report