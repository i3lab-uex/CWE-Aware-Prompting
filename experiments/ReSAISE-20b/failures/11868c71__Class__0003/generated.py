import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
#  Data model – in a real system this would come from the database
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    unique_id: str
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)          # Sensitive
    home_address: str = field(repr=False)   # Sensitive
    discipline_record: list[str] = field(default_factory=list)

# ----------------------------------------------------------------------
#  In‑memory "database" of students
# ----------------------------------------------------------------------
STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        unique_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.9,
        home_address="123 Maple St, Springfield",
        discipline_record=["Late submission"],
    ),
    "S002": Student(
        unique_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave, Springfield",
        discipline_record=[],
    ),
}

# ----------------------------------------------------------------------
#  Helper utilities
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"gpa", "home_address"}

def _extract_placeholders(template: str) -> set[str]:
    """
    Extracts all placeholders from a format string.
    Supports simple field names and dotted attributes (e.g. student.name).
    """
    # Regular expression for Python format fields
    field_pattern = re.compile(r"{(?P<field>[^{}]+)}")
    fields = set()
    for match in field_pattern.finditer(template):
        fields.add(match.group("field").strip())
    return fields

def _sanitize_template_and_map(
    student: Student, template: str
) -> tuple[str, dict]:
    """
    Validates that the template does not reference sensitive data,
    then prepares a mapping of allowed attributes for formatting.
    """
    placeholders = _extract_placeholders(template)

    # Detect any reference to a sensitive attribute
    for ph in placeholders:
        if ph.startswith("student."):
            attr = ph.split(".", 1)[1]
            if attr in _SENSITIVE_FIELDS:
                raise ValueError(f"Access to sensitive attribute '{attr}' is not allowed.")
        elif ph in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive attribute '{ph}' is not allowed.")

    # Build a mapping of safe attributes
    safe_attrs = {
        "name": student.name,
        "course": student.course,
        "age": student.age,
    }

    # Replace 'student.' prefix so that str.format works with the mapping
    sanitized_template = re.sub(r"{\s*student\.([^\s}]+)\s*}", r"{\1}", template)

    return sanitized_template, safe_attrs

# ----------------------------------------------------------------------
#  Public API
# ----------------------------------------------------------------------
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student profile using the supplied template.

    Parameters
    ----------
    unique_id : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders such as '{student.name}'.

    Returns
    -------
    str
        The formatted student report.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if the template references
        sensitive attributes (GPA, home address).
    """
    student = STUDENTS_DB.get(unique_id)
    if not student:
        raise ValueError(f"Student with ID '{unique_id}' does not exist.")

    sanitized_template, mapping = _sanitize_template_and_map(student, report_template)

    try:
        return sanitized_template.format(**mapping)
    except KeyError as exc:
        raise ValueError(f"Template references unknown placeholder: {exc}") from None

# ----------------------------------------------------------------------
#  Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}"
    )
    print(build_student_profile("S001", template))