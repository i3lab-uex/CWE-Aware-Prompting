import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
# Mocked Student database and class definition
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Student:
    """Represents a student in the system."""
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str  # Sensitive
    discipline_record: str  # Sensitive


# In‑memory "database" of students.
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None",
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record="Late submission in 2023",
    ),
}


# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------


def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generates a student report based on the supplied template.

    Parameters
    ----------
    student_number : str
        Unique identifier for a student.
    report_template : str
        A format string that may contain placeholders such as
        `{student.name}`, `{student.course}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student does not exist, or if the template contains
        disallowed placeholders.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the student record
    # ------------------------------------------------------------------
    student = STUDENT_DB.get(student_number)
    if not student:
        raise ValueError(f"Student with number '{student_number}' does not exist.")

    # ------------------------------------------------------------------
    # 2. Define allowed fields (exclude sensitive data)
    # ------------------------------------------------------------------
    allowed_fields = {
        f.name for f in fields(Student) if f.name not in {"home_address", "discipline_record"}
    }

    # ------------------------------------------------------------------
    # 3. Validate placeholders in the template
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{([^{}]+)}")
    for match in placeholder_pattern.finditer(report_template):
        expr = match.group(1).strip()
        # Expecting the form 'student.attribute'
        if not expr.startswith("student."):
            raise ValueError(f"Invalid placeholder '{match.group(0)}': only 'student' namespace is allowed.")
        attr = expr.split(".", 1)[1]
        if attr not in allowed_fields:
            raise ValueError(f"Access to sensitive or unknown attribute '{attr}' is not permitted.")

    # ------------------------------------------------------------------
    # 4. Perform the formatting
    # ------------------------------------------------------------------
    # Build a simple namespace for formatting
    ns = {"student": student}
    try:
        report = report_template.format(**ns)
    except KeyError as exc:
        # This should not happen because we validated, but guard anyway
        raise ValueError(f"Missing placeholder data: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (for manual testing only; remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}\n"
    )
    print(draft_student_report("S001", template))