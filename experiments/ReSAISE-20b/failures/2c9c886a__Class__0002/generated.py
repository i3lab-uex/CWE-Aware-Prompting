import re
from dataclasses import dataclass
from typing import Dict

# --- Mocked system storage ----------------------------------------------- #
@dataclass(frozen=True)
class Student:
    student_number: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str          # sensitive
    discipline_record: str     # sensitive

# In a real system this would be replaced by a database query.
STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        student_number="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Main St, Anytown",
        discipline_record="None"
    ),
    "S002": Student(
        student_number="S002",
        name="Bob Jones",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Othertown",
        discipline_record="Late submission"
    ),
}

# --- Allowed attributes ----------------------------------------------- #
ALLOWED_ATTRIBUTES = {"name", "course", "age", "GPA"}

# --- Helper classes ----------------------------------------------- #
class StudentProxy:
    """
    A proxy that exposes only the allowed attributes of a Student instance.
    Any attempt to access a disallowed attribute raises ValueError.
    """
    def __init__(self, student: Student):
        self._student = student

    def __getattr__(self, item):
        if item in ALLOWED_ATTRIBUTES:
            return getattr(self._student, item)
        raise ValueError(f"Unauthorized access to sensitive attribute '{item}'")

    def __repr__(self):
        attrs = ", ".join(f"{k}={getattr(self._student, k)!r}" for k in ALLOWED_ATTRIBUTES)
        return f"StudentProxy({attrs})"

# --- Core function ----------------------------------------------- #
def draft_student_report(student_number: str, report_template: str) -> str:
    """
    Generate a student report based on the provided template.

    Args:
        student_number: Unique identifier of the student.
        report_template: A format string containing placeholders like
                         '{student.name}', '{student.course}', etc.

    Returns:
        A formatted report string.

    Raises:
        ValueError: If the student_number is unknown, if the template
                    contains disallowed placeholders, or if a sensitive
                    attribute is accessed.
    """
    # Retrieve the student; raise error if not found
    student = STUDENT_DB.get(student_number)
    if not student:
        raise ValueError(f"Student with number '{student_number}' does not exist")

    # Validate placeholders in the template
    placeholder_pattern = r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    placeholders = re.findall(placeholder_pattern, report_template)

    for attr in placeholders:
        if attr not in ALLOWED_ATTRIBUTES:
            raise ValueError(f"Template contains disallowed placeholder '{{student.{attr}}}'")

    # Use the proxy to prevent accidental access to sensitive data
    student_proxy = StudentProxy(student)

    try:
        report = report_template.format(student=student_proxy)
    except AttributeError as exc:
        # This should not happen because of the proxy, but guard anyway
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# --- Example usage (for testing purposes) ------------------------------ #
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "---------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}"
    )
    print(draft_student_report("S001", tmpl))