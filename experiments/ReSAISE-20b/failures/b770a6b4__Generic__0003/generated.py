import re
from dataclasses import dataclass, asdict
from typing import Dict

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
    home_address: str
    # Sensitive / restricted fields that should not be exposed via templates
    disciplinary_record: str


# ----------------------------------------------------------------------
# In‑memory student registry (for demo purposes)
# ----------------------------------------------------------------------
_STUDENT_REGISTRY: Dict[str, Student] = {
    "A001": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        disciplinary_record="None"
    ),
    "B002": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        disciplinary_record="Late assignment in 2023"
    ),
    # Add more students as needed
}

# ----------------------------------------------------------------------
# Allowed attributes for templating
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {
    "name",
    "course",
    "age",
    "gpa",
    "home_address"
}

# ----------------------------------------------------------------------
# Helper to extract placeholder names from a format string
# ----------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compile_student_profile(learner_code: str, profile_template: str) -> str:
    """
    Generate a student report by substituting placeholders in the template
    with values from the student's record.

    Parameters
    ----------
    learner_code : str
        Unique identifier for a student.
    profile_template : str
        Template containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the learner_code is unknown, or if the template references a
        restricted/sensitive field.
    """
    # Validate learner_code
    if not isinstance(learner_code, str) or not learner_code:
        raise ValueError("Invalid learner code provided.")

    student = _STUDENT_REGISTRY.get(learner_code)
    if not student:
        raise ValueError(f"Student with code '{learner_code}' does not exist.")

    # Prepare a mapping of allowed attributes
    student_dict = {f"student.{k}": v for k, v in asdict(student).items() if k in _ALLOWED_FIELDS}

    # Check for restricted fields in the template
    placeholders = _extract_placeholders(profile_template)
    for placeholder in placeholders:
        # Expecting format like 'student.name'
        if not placeholder.startswith("student."):
            raise ValueError(f"Unsupported placeholder '{placeholder}'. "
                             "Only 'student.*' placeholders are allowed.")
        field_name = placeholder.split(".", 1)[1]
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(f"Attempt to access restricted field '{field_name}'.")

    # Render the template
    try:
        report = profile_template.format_map(student_dict)
    except KeyError as exc:
        # This should not happen due to earlier checks, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report