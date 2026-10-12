import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# 1. Student model – only non‑sensitive fields are exposed
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    id: str
    name: str
    course: str
    age: int
    # Sensitive fields – stored but not exposed via the public API
    _gpa: float = field(repr=False, default=0.0)
    _home_address: str = field(repr=False, default="")

# ------------------------------------------------------------------
# 2. In‑memory “database” of students
# ------------------------------------------------------------------
STUDENT_DB: Dict[str, Student] = {
    "s001": Student(
        id="s001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        _gpa=3.8,
        _home_address="123 Maple Ave, Springfield",
    ),
    "s002": Student(
        id="s002",
        name="Bob Jones",
        course="Mathematics",
        age=22,
        _gpa=3.5,
        _home_address="456 Oak St, Shelbyville",
    ),
}

# ------------------------------------------------------------------
# 3. Utility – safe format helper
# ------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

# Attributes that are considered sensitive
SENSITIVE_ATTRS = {"gpa", "home_address"}

def _validate_placeholders(template: str) -> None:
    """
    Ensure that the template does not request any sensitive attributes.
    Raises ValueError if a forbidden placeholder is found.
    """
    for match in PLACEHOLDER_RE.finditer(template):
        attr = match.group(1)
        if attr in SENSITIVE_ATTRS:
            raise ValueError(
                f"Access to sensitive attribute '{attr}' is prohibited in the template."
            )
    # No forbidden placeholders found – safe to proceed

# ------------------------------------------------------------------
# 4. Main function
# ------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report using the provided format string.

    Args:
        id: Unique identifier of the student.
        format_string: A template containing placeholders such as
                       '{student.name}', '{student.course}' etc.

    Returns:
        A formatted string representing the student's report.

    Raises:
        ValueError: If the student id does not exist or if the template
                    attempts to access sensitive attributes.
    """
    # 1. Retrieve student record
    student = STUDENT_DB.get(id)
    if not student:
        raise ValueError(f"Student with id '{id}' does not exist.")

    # 2. Validate template for sensitive data exposure
    _validate_placeholders(format_string)

    # 3. Perform formatting
    try:
        report = format_string.format(student=student)
    except KeyError as exc:
        # If the template references a non‑existent attribute
        raise ValueError(f"Invalid placeholder in format string: {exc}") from exc

    return report

# ------------------------------------------------------------------
# 5. Example usage (for manual testing)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Student: {student.name}\nCourse: {student.course}\nAge: {student.age}"
    print(create_student_summary("s001", tmpl))