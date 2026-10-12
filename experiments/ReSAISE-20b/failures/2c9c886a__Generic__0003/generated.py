import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
#  Student data model and in‑memory store (for illustration purposes)
# ----------------------------------------------------------------------
@dataclass
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str = field(repr=False)          # sensitive
    discipline_record: list[str] = field(default_factory=list, repr=False)

# Example in‑memory database
STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Anytown",
        discipline_record=["Late submission of project"],
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Othertown",
        discipline_record=[],
    ),
}

# ----------------------------------------------------------------------
#  Report generation
# ----------------------------------------------------------------------
_ALLOWED_ATTRS = {"name", "course", "age", "GPA"}

_PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_number : str
        Unique identifier for the student.
    report_template : str
        Format string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student number does not exist or if a placeholder references
        an unauthorized attribute.
    """
    # 1. Retrieve the student
    student = STUDENTS_DB.get(student_number)
    if not student:
        raise ValueError(f"Student with number '{student_number}' does not exist.")

    # 2. Verify that all placeholders reference allowed attributes
    for match in _PLACEHOLDER_RE.finditer(report_template):
        attr = match.group(1)
        if attr not in _ALLOWED_ATTRS:
            raise ValueError(
                f"Unauthorized access to sensitive attribute '{attr}'. "
                "Allowed attributes: name, course, age, GPA."
            )

    # 3. Build a dictionary of allowed attributes
    safe_attrs = {attr: getattr(student, attr) for attr in _ALLOWED_ATTRS}

    # 4. Format the template
    try:
        report = report_template.format(student=safe_attrs)
    except KeyError as exc:
        # This should not happen due to the previous check, but guard anyway
        raise ValueError(f"Missing attribute in template: {exc}") from exc

    return report


# ----------------------------------------------------------------------
#  Example usage (commented out; remove comments to run)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}\n"
    )
    print(draft_student_report("S001", template))