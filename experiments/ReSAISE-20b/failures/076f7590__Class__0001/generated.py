import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
# Dummy in‑memory student store (for illustration only)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # sensitive
    discipline_record: Dict[str, str]  # sensitive

# Example dataset – in a real system this would be fetched from a secure DB
_STUDENT_DB: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record={"late": "2023-01-15"},
    ),
    "token456": Student(
        name="Bob Jones",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record={"detention": "2023-02-20"},
    ),
}

# --------------------------------------------------------------------------- #
# Security helpers
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"home_address", "discipline_record"}

def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from a format string.
    Supports simple `{field}` syntax. Nested or advanced formatting
    is not supported for security reasons.
    """
    # Matches {field} but ignores {{ or }} escape sequences
    pattern = re.compile(r"(?<!{){([a-zA-Z_][a-zA-Z0-9_]*)}(?!})")
    return set(match.group(1) for match in pattern.finditer(template))

def _validate_placeholders(placeholders: set):
    """
    Ensure that no sensitive field is requested.
    Raise ValueError if a forbidden placeholder is detected.
    """
    for ph in placeholders:
        if ph in _SENSITIVE_FIELDS:
            raise ValueError(f"Unauthorized access to sensitive field '{ph}'")

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report based on the supplied template.

    Parameters
    ----------
    student_token : str
        Unique identifier for a student.
    report_template : str
        Format string containing placeholders such as '{name}' or '{course}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token is unknown, or if the template attempts to access
        sensitive information (home_address, discipline_record).
    """
    # 1. Retrieve student data
    student = _STUDENT_DB.get(student_token)
    if student is None:
        raise ValueError("Invalid or unknown student token")

    # 2. Inspect template for placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # 3. Build a safe dictionary of allowed attributes
    student_dict = asdict(student)
    # Remove sensitive fields just in case they slipped through
    for field in _SENSITIVE_FIELDS:
        student_dict.pop(field, None)

    # 4. Perform safe formatting
    try:
        report = report_template.format(**student_dict)
    except KeyError as exc:
        # Placeholder refers to a non‑existent attribute
        raise ValueError(f"Unknown placeholder '{exc.args[0]}' in template") from None

    return report

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "Name: {name}\n"
        "Course: {course}\n"
        "Age: {age}\n"
        "GPA: {gpa:.2f}"
    )
    print(compile_student_report("token123", tmpl))