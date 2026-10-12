import re
from dataclasses import dataclass, fields

# ------------------------------------------------------------------
# Dummy Student model and in‑memory store
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    name: str
    course: str
    age: int
    GPA: float
    home_address: str   # sensitive
    discipline_record: str  # sensitive


# In‑memory "database" of students keyed by a unique token
STUDENT_DB = {
    # Example entries – in a real system this would be fetched from a database
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
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late assignment on 2024-01-15"
    ),
}


# ------------------------------------------------------------------
# Allowed fields for report generation
# ------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "GPA"}


# ------------------------------------------------------------------
# Helper: find placeholders in a template string
# ------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in PLACEHOLDER_RE.finditer(template)}


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_token : str
        Unique identifier for a student.
    report_template : str
        A format string containing placeholders like `{name}` or `{course}`.

    Returns
    -------
    str
        The formatted report string with placeholders replaced by student data.

    Raises
    ------
    ValueError
        If the token does not exist or if the template attempts to access
        sensitive or non‑existent attributes.
    """
    # Retrieve student record
    student = STUDENT_DB.get(student_token)
    if not student:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # Identify placeholders in the template
    placeholders = _extract_placeholders(report_template)

    # Validate placeholders against allowed fields
    for field in placeholders:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized or unsupported placeholder '{{{field}}}' in report template."
            )

    # Build a mapping of allowed attributes
    student_dict = {f.name: getattr(student, f.name) for f in fields(Student)}

    # Safely format the template
    try:
        report = report_template.format(**{k: student_dict[k] for k in placeholders})
    except KeyError as exc:
        # Should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# ------------------------------------------------------------------
# Example usage (for local testing only; remove in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "--------------\n"
        "Name   : {name}\n"
        "Course : {course}\n"
        "Age    : {age}\n"
        "GPA    : {GPA}\n"
    )
    print(compile_student_report("token123", template))