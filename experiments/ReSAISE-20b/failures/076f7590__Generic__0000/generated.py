import re
from dataclasses import dataclass, field
from typing import Dict

# --- Student model ----------------------------------------------

@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    name: str
    course: str
    age: int
    GPA: float
    # Sensitive fields – should never appear in a public report
    home_address: str = field(repr=False)
    discipline_record: str = field(repr=False)

# --- In‑memory data store ----------------------------------------

# Example student database keyed by unique token
STUDENT_DB: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "token456": Student(
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of Assignment 3"
    ),
}

# --- Allowed fields for reporting --------------------------------

ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

# --- Main function ----------------------------------------------

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generates a student report from the given template.

    Parameters
    ----------
    student_token : str
        Unique identifier for a student.
    report_template : str
        Template string containing placeholders such as `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token does not exist or if a placeholder refers to a
        disallowed field.
    """
    # 1. Retrieve the student record securely
    student = STUDENT_DB.get(student_token)
    if not student:
        raise ValueError(f"Student token '{student_token}' not found.")

    # 2. Find all placeholders of the form {student.<field>}
    pattern = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = pattern.findall(report_template)

    # 3. Validate each placeholder
    for field_name in placeholders:
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive student data: '{field_name}'."
            )

    # 4. Build a mapping for string formatting
    student_dict = {field: getattr(student, field) for field in ALLOWED_FIELDS}
    # The template may use nested braces like {{ or }} – let str.format handle them

    try:
        report = report_template.format(student=student_dict)
    except KeyError as exc:
        # Should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report

# --- Example usage ----------------------------------------------

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}\n"
    )
    print(compile_student_report("token123", template))