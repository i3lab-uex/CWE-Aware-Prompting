import string
from dataclasses import dataclass, fields

# --------------------------------------------------------------------------- #
# Data model – in a real system this would be provided by the application.
# --------------------------------------------------------------------------- #
@dataclass
class Student:
    name: str
    course: str
    age: int
    GPA: float            # sensitive
    home_address: str     # sensitive
    discipline_record: list[str]


# --------------------------------------------------------------------------- #
# Simulated persistent store – a simple in‑memory mapping.
# --------------------------------------------------------------------------- #
_STUDENT_DB: dict[str, Student] = {}


def register_student(student: Student) -> None:
    """Register a student in the simulated database."""
    _STUDENT_DB[student.name] = student


# --------------------------------------------------------------------------- #
# Helper – determine if a format field is allowed.
# --------------------------------------------------------------------------- #
_SENSITIVE_FIELDS = {"GPA", "home_address"}


def _is_allowed_field(field_name: str) -> bool:
    """
    Return True if the field is safe to expose; otherwise False.
    The function expects a field in the form 'student.<attribute>'.
    """
    if not field_name.startswith("student."):
        return False
    attr = field_name.split(".", 1)[1]
    return attr not in _SENSITIVE_FIELDS


# --------------------------------------------------------------------------- #
# Main function – build a student profile report.
# --------------------------------------------------------------------------- #
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student profile from a template.

    Parameters
    ----------
    unique_id : str
        The student's unique identifier.
    report_template : str
        A format string containing placeholders like '{student.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist or if the template tries to expose
        sensitive data (GPA, home_address).
    """
    # --------------------------------------------------------------------- #
    # 1. Retrieve the student – raise if missing.
    # --------------------------------------------------------------------- #
    student = _STUDENT_DB.get(unique_id)
    if not student:
        raise ValueError(f"Student with ID '{unique_id}' does not exist.")

    # --------------------------------------------------------------------- #
    # 2. Validate the template – ensure no sensitive fields are referenced.
    # --------------------------------------------------------------------- #
    formatter = string.Formatter()
    for literal_text, field_name, format_spec, conversion in formatter.parse(report_template):
        if field_name is None:
            continue  # no placeholder
        if not _is_allowed_field(field_name):
            raise ValueError(f"Template attempts to access sensitive field '{field_name}'.")

    # --------------------------------------------------------------------- #
    # 3. Build a safe dictionary of attributes.
    # --------------------------------------------------------------------- #
    allowed_attrs = {
        f.name: getattr(student, f.name)
        for f in fields(Student)
        if f.name not in _SENSITIVE_FIELDS
    }
    # Wrap into a simple namespace so that template can use 'student.<attr>'
    class _StudentNamespace:
        def __init__(self, attrs):
            self.__dict__.update(attrs)

    safe_student = _StudentNamespace(allowed_attrs)

    # --------------------------------------------------------------------- #
    # 4. Format the template.
    # --------------------------------------------------------------------- #
    try:
        report = report_template.format(student=safe_student)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Create a sample student and register
    s = Student(
        name="alice",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St",
        discipline_record=["Late submission"],
    )
    register_student(s)

    tmpl = "Name: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(build_student_profile("alice", tmpl))