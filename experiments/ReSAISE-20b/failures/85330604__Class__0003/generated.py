import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Mock student database and data model
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    stu_id: str
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)          # sensitive
    home_address: str = field(repr=False)   # sensitive
    discipline_record: str = field(repr=False)  # sensitive


# In‑memory student store (id → Student)
STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        stu_id="s001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.9,
        home_address="123 Main St, Springfield",
        discipline_record="None",
    ),
    "s002": Student(
        stu_id="s002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Elm St, Shelbyville",
        discipline_record="Late submission of assignment 3",
    ),
}


# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------


def create_student_report(stu_id: str, report_template: str) -> str:
    """
    Generate a student report by rendering the provided template with
    allowed attributes of the specified student.

    Parameters:
        stu_id (str): Unique identifier for the student.
        report_template (str): Format string containing placeholders
            like '{student.name}', '{student.course}', etc.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the student ID does not exist, or if the
            template attempts to access disallowed attributes.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the student record
    # ------------------------------------------------------------------
    student = STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Student with ID '{stu_id}' does not exist.")

    # ------------------------------------------------------------------
    # 2. Identify placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{student\.([a-zA-Z_][a-zA-Z0-9_]*)}")
    placeholders = placeholder_pattern.findall(report_template)

    # ------------------------------------------------------------------
    # 3. Define which attributes are allowed to be exposed
    # ------------------------------------------------------------------
    ALLOWED_FIELDS = {"name", "course", "age"}

    # ------------------------------------------------------------------
    # 4. Validate each placeholder
    # ------------------------------------------------------------------
    for field_name in placeholders:
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive data: '{field_name}'. "
                "Only name, course, and age may be included."
            )

    # ------------------------------------------------------------------
    # 5. Prepare a mapping for formatting
    # ------------------------------------------------------------------
    context = {
        "student": {field: getattr(student, field) for field in ALLOWED_FIELDS}
    }

    # ------------------------------------------------------------------
    # 6. Render the template
    # ------------------------------------------------------------------
    try:
        report = report_template.format(**context)
    except KeyError as e:
        # This should not happen because we validated placeholders
        raise ValueError(f"Missing data for placeholder: {e}") from e

    return report


# ----------------------------------------------------------------------
# Example usage (for manual testing)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
    )
    print(create_student_report("s001", tmpl))