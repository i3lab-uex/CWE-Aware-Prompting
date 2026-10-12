import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
#  Student model (simplified for this task)
# --------------------------------------------------------------------------- #

@dataclass
class Student:
    student_number: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str = field(repr=False)
    discipline_record: str = field(repr=False)

# --------------------------------------------------------------------------- #
#  In‑memory storage of students
# --------------------------------------------------------------------------- #

_STUDENT_DB: Dict[str, Student] = {}

def _add_student(student: Student) -> None:
    """Utility to add a student to the in‑memory database."""
    _STUDENT_DB[student.student_number] = student

# --------------------------------------------------------------------------- #
#  Populate the database with some example data (for demonstration)
# --------------------------------------------------------------------------- #

_add_student(
    Student(
        student_number="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="No infractions"
    )
)

_add_student(
    Student(
        student_number="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late assignment"
    )
)

# --------------------------------------------------------------------------- #
#  Report generation
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = {"name", "course", "age", "gpa"}

PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Create a customized student report from the given template.

    Parameters
    ----------
    student_number : str
        Unique identifier of the student.
    report_template : str
        Template string containing placeholders like `{student.name}`.

    Returns
    -------
    str
        The report with all placeholders substituted.

    Raises
    ------
    ValueError
        If the student does not exist, or if a placeholder references an
        unauthorized attribute.
    """
    # Retrieve the student record; raise error if missing
    student = _STUDENT_DB.get(student_number)
    if not student:
        raise ValueError(f"Student with number '{student_number}' does not exist.")

    # Function to replace each placeholder
    def _replace(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(
                f"Unauthorized access to sensitive data: '{field_name}'. "
                "Allowed fields are: name, course, age, gpa."
            )
        # Retrieve the attribute value from the student
        return str(getattr(student, field_name))

    # Perform substitution
    try:
        report = PLACEHOLDER_RE.sub(_replace, report_template)
    except ValueError as exc:
        # Re‑raise to satisfy the function contract
        raise exc

    return report

# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa}\n"
    )
    print(draft_student_report("S001", template))