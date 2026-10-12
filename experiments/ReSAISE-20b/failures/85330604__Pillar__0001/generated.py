import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
# Mocked Student model (in a real system this would be fetched from DB)
# ----------------------------------------------------------------------
@dataclass
class Student:
    stu_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive

# ----------------------------------------------------------------------
# In‑memory student repository (for demo purposes)
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Elm St, Shelbyville",
        discipline_record="Late assignment"
    ),
}

# ----------------------------------------------------------------------
# Allowed attributes for report generation
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

# Regular expression to capture placeholders in the template
_PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for the student.
    report_template : str
        A format string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist, or if a placeholder refers to a
        sensitive field, or if an unknown placeholder is used.
    """
    # ------------------------------------------------------------------
    # Retrieve the student record
    # ------------------------------------------------------------------
    student = _STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student ID '{stu_id}' does not exist.")

    # ------------------------------------------------------------------
    # Extract placeholders and validate them
    # ------------------------------------------------------------------
    used_fields = set()
    for match in _PLACEHOLDER_RE.finditer(report_template):
        field_name = match.group(1)
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized or unknown placeholder '{field_name}'. "
                "Sensitive data cannot be accessed."
            )
        used_fields.add(field_name)

    # ------------------------------------------------------------------
    # Prepare the mapping for formatting
    # ------------------------------------------------------------------
    allowed_dict = {field: getattr(student, field) for field in used_fields}

    # ------------------------------------------------------------------
    # Perform safe formatting
    # ------------------------------------------------------------------
    try:
        report = report_template.format(student=allowed_dict)
    except KeyError as exc:
        # This should not happen due to earlier validation
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA}\n"
    )
    print(create_student_report("S001", template))