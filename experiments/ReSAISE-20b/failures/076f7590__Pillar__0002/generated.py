import re
from dataclasses import dataclass, fields
from typing import Dict

# -------------------------------------------------------------
# Mocked student database and token registry (would be replaced
# by real persistence in a production system)
# -------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive

# In-memory token -> Student mapping (for demonstration)
STUDENT_DB: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="No violations"
    ),
    "token456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.6,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late assignment on 2024-05-12"
    ),
}

# -------------------------------------------------------------
# Helper utilities
# -------------------------------------------------------------

def _extract_placeholders(template: str) -> set[str]:
    """
    Extracts placeholder names from a format string.
    Only simple `{field}` patterns are supported.
    """
    # The regex matches {field_name} where field_name consists of
    # alphanumerics and underscores.
    return set(re.findall(r"{([a-zA-Z_][a-zA-Z0-9_]*)}", template))

def _validate_placeholders(placeholders: set[str], allowed_attrs: set[str]) -> None:
    """
    Raises ValueError if any placeholder references a disallowed attribute.
    """
    unauthorized = placeholders - allowed_attrs
    if unauthorized:
        raise ValueError(
            f"Unauthorized placeholder(s) detected: {', '.join(sorted(unauthorized))}"
        )

# -------------------------------------------------------------
# Main function
# -------------------------------------------------------------

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generates a student report by filling in the provided template with
    non-sensitive attributes of the student identified by `student_token`.

    Parameters
    ----------
    student_token : str
        Unique identifier for the student.
    report_template : str
        A format string containing placeholders such as '{name}' or
        '{course}'. Placeholders referencing sensitive data are disallowed.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token does not exist, or if the template references
        disallowed attributes.
    """
    # 1. Retrieve student data
    student = STUDENT_DB.get(student_token)
    if not student:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # 2. Determine allowed attributes (exclude sensitive ones)
    all_attrs = {f.name for f in fields(student)}
    # Sensitive attributes that must not be exposed
    sensitive_attrs = {"home_address", "discipline_record"}
    allowed_attrs = all_attrs - sensitive_attrs

    # 3. Validate placeholders in the template
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders, allowed_attrs)

    # 4. Build context dictionary for formatting
    context = {attr: getattr(student, attr) for attr in allowed_attrs}

    # 5. Perform formatting
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This should not happen due to prior validation but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report