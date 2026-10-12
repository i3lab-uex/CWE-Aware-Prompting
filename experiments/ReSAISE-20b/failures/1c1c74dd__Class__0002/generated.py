import re
from typing import Dict

# Example Student data store (in a real system this would come from a database)
STUDENTS_DB: Dict[str, Dict] = {
    "S001": {"name": "Alice Johnson", "course": "Computer Science", "age": 20,
             "GPA": 3.8, "home_address": "123 Maple St.", "discipline_record": []},
    "S002": {"name": "Bob Smith",     "course": "Mathematics",      "age": 22,
             "GPA": 3.5, "home_address": "456 Oak Ave.",   "discipline_record": []},
    # ... more students ...
}

# Sensitive fields that must not be exposed
SENSITIVE_FIELDS = {"GPA", "home_address"}


def _extract_placeholders(template: str):
    """
    Extract placeholder names from a format string.
    Returns a set of strings such as 'student.name', 'student.course'.
    """
    pattern = re.compile(r"\{([^{}]+)\}")
    return set(pattern.findall(template))


def produce_student_report(stu_id: str, custom_template: str) -> str:
    """
    Generate a student report using the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    custom_template : str
        Format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if a sensitive field is requested.
    """
    # Validate student existence
    student = STUDENTS_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # Inspect placeholders for sensitive fields
    placeholders = _extract_placeholders(custom_template)
    for ph in placeholders:
        # Expect format 'student.<field>'
        parts = ph.split(".")
        if len(parts) != 2 or parts[0] != "student":
            continue  # ignore malformed placeholders
        field = parts[1]
        if field in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{field}' is prohibited.")

    # Build a mapping containing only allowed fields
    allowed_fields = {k: v for k, v in student.items() if k not in SENSITIVE_FIELDS}
    # Prefix keys with 'student.' to match placeholder names
    mapping = {f"student.{k}": v for k, v in allowed_fields.items()}

    try:
        report = custom_template.format(**mapping)
    except KeyError as e:
        raise ValueError(f"Missing placeholder for field: {e}") from None

    return report