import re
from dataclasses import dataclass, field
from typing import Dict

# ---------------------  Data Model  ---------------------

@dataclass
class Student:
    """Represents a student in the management system."""
    stu_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str
    disciplinary_record: str = field(default="No record")

# Simulated in‑memory database of students
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        stu_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
    ),
    "S002": Student(
        stu_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Riverton",
        disciplinary_record="Late submission in 2023",
    ),
}

# ---------------------  Utility Functions  ---------------------

def _extract_placeholders(template: str) -> set:
    """
    Extracts all field names referenced in a format string.
    Supports nested attributes like {student.name}.
    """
    # Regex to match `{...}` blocks, capturing the inner expression
    pattern = re.compile(r"{([^{}]+)}")
    placeholders = set()
    for match in pattern.finditer(template):
        expr = match.group(1).strip()
        # Only consider expressions that start with 'student.'
        if expr.startswith("student."):
            attr = expr.split(".", 1)[1]
            # Ignore any format specifiers after ':' (e.g., {student.name:10})
            attr = attr.split(":")[0].split("[")[0]
            placeholders.add(attr)
    return placeholders

# ---------------------  Core Function  ---------------------

def create_student_summary(stu_id: str, summary_template: str) -> str:
    """
    Generates a student report based on the provided template.

    Parameters
    ----------
    stu_id : str
        Unique identifier for a student.
    summary_template : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID is not found, or if a restricted attribute is requested.
    """
    # 1. Validate student ID
    student = STUDENT_DB.get(stu_id)
    if not student:
        raise ValueError(f"Invalid student ID: {stu_id}")

    # 2. Detect restricted fields
    RESTRICTED_FIELDS = {"gpa", "disciplinary_record"}
    requested_fields = _extract_placeholders(summary_template)

    if RESTRICTED_FIELDS & requested_fields:
        restricted = ", ".join(sorted(RESTRICTED_FIELDS & requested_fields))
        raise ValueError(
            f"Access to restricted fields not allowed: {restricted}"
        )

    # 3. Render the template
    try:
        report = summary_template.format(student=student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Template rendering error: {exc}") from exc

    return report


# ---------------------  Example Usage  ---------------------

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "Address: {student.home_address}"
    )
    print(create_student_summary("S001", tmpl))