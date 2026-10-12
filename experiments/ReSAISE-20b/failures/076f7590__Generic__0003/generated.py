import re
from typing import Dict

# ----------------------------------------------------------------------
# Mocked data layer (in a real system this would query a database or API)
# ----------------------------------------------------------------------
class Student:
    """Represents a student record in the system."""
    def __init__(self, name: str, course: str, age: int,
                 gpa: float, home_address: str, discipline_record: Dict):
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.home_address = home_address          # Sensitive
        self.discipline_record = discipline_record  # Sensitive


# In‑memory storage for demonstration purposes
_STUDENT_DB: Dict[str, Student] = {
    "token123": Student(
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record={"late_submissions": 2}
    ),
    "token456": Student(
        name="Bob Jones",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record={"absences": 1}
    ),
}

def get_student_by_token(token: str) -> Student:
    """Retrieve a student by token. Raises KeyError if not found."""
    return _STUDENT_DB[token]


# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "course", "age", "gpa"}

class _SafeStudentProxy:
    """A proxy that only exposes allowed attributes of a Student."""
    def __init__(self, student: Student):
        self._student = student

    def __getattr__(self, item: str):
        if item in ALLOWED_FIELDS:
            return getattr(self._student, item)
        raise AttributeError(f"Access to '{item}' is not allowed.")


def compile_student_report(student_token: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    student_token : str
        Unique identifier for a student.
    report_template : str
        Format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the token does not exist or if the template attempts to access a
        disallowed field.
    """
    # 1. Retrieve student record
    try:
        student = get_student_by_token(student_token)
    except KeyError as exc:
        raise ValueError(f"Student token '{student_token}' not found.") from exc

    # 2. Validate placeholders in the template
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    for match in placeholder_pattern.finditer(report_template):
        expr = match.group(1).strip()
        # Only allow expressions of the form 'student.<field>'
        parts = expr.split('.')
        if len(parts) != 2 or parts[0] != "student":
            raise ValueError(f"Invalid placeholder '{expr}'. Only 'student.<field>' is allowed.")
        field_name = parts[1]
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is forbidden.")

    # 3. Format the report using a safe proxy
    safe_student = _SafeStudentProxy(student)
    try:
        formatted_report = report_template.format(student=safe_student)
    except Exception as exc:
        raise ValueError(f"Error formatting report: {exc}") from exc

    return formatted_report


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.gpa:.2f}"
    )
    print(compile_student_report("token123", template))