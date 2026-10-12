import string
from typing import Dict

# ------------------------------------------------------------------
# Mocked Student class and data store (would be provided by the system)
# ------------------------------------------------------------------

class Student:
    """
    A simple representation of a student record.
    Only the following attributes are considered *non‑sensitive* and may be used
    in a public report.  All other attributes are marked as sensitive.
    """
    def __init__(self, token: str, name: str, course: str,
                 age: int, gpa: float,
                 home_address: str, discipline_record: str):
        self.token = token
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        # Sensitive data – must never be exposed via the report
        self.home_address = home_address
        self.discipline_record = discipline_record

# In‑memory "database" of students (token -> Student instance)
_STUDENT_DB: Dict[str, Student] = {}

def _add_student_to_db(student: Student):
    """Utility to populate the mock database."""
    _STUDENT_DB[student.token] = student

# Example data (for demonstration only)
_add_student_to_db(Student(
    token="stu123",
    name="Alice Johnson",
    course="Computer Science",
    age=20,
    gpa=3.8,
    home_address="123 Maple St, Springfield",
    discipline_record="None"
))

# ------------------------------------------------------------------
# Report generation logic
# ------------------------------------------------------------------

ALLOWED_ATTRIBUTES = {"name", "course", "age", "gpa"}

def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generates a student report based on the supplied template.

    Parameters
    ----------
    student_token : str
        Unique identifier for a student.
    report_template : str
        A format string that may contain placeholders such as '{name}',
        '{course}', etc. Only allowed attributes can be referenced.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token is not found, or if the template references a
        sensitive attribute.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the student record safely
    # ------------------------------------------------------------------
    student = _STUDENT_DB.get(student_token)
    if student is None:
        raise ValueError(f"Student token '{student_token}' does not exist.")

    # ------------------------------------------------------------------
    # 2. Prepare a mapping of allowed attributes
    # ------------------------------------------------------------------
    student_data = {
        key: getattr(student, key) for key in ALLOWED_ATTRIBUTES
    }

    # ------------------------------------------------------------------
    # 3. Validate that the template does not reference sensitive data
    # ------------------------------------------------------------------
    formatter = string.Formatter()
    for _, field_name, _, _ in formatter.parse(report_template):
        if field_name and field_name not in ALLOWED_ATTRIBUTES:
            raise ValueError(
                f"Unauthorized access to sensitive data: '{field_name}'. "
                "Only {name}, {course}, {age}, and {gpa} are permitted."
            )

    # ------------------------------------------------------------------
    # 4. Safely format the template
    # ------------------------------------------------------------------
    try:
        report = report_template.format(**student_data)
    except KeyError as exc:
        # This should not happen because we validated fields, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report