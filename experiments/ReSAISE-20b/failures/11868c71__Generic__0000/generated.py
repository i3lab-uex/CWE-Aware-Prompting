from dataclasses import dataclass, field
import re

# ----------------------------------------------------------------------
# Data model and in‑memory store (normally provided by the system)
# ----------------------------------------------------------------------
@dataclass
class Student:
    unique_id: str
    name: str
    course: str
    age: int
    GPA: float = field(repr=False)
    home_address: str = field(repr=False)
    discipline_record: str

# Example in‑memory database of students
_STUDENT_DB = {
    "S001": Student(
        unique_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.9,
        home_address="123 Maple Ave, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        unique_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak St, Shelbyville",
        discipline_record="Late submission of assignment"
    ),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
_SENSITIVE_KEYS = {"GPA", "home_address"}

def _extract_placeholders(template: str) -> set[str]:
    """
    Extract attribute names referenced in a format string.
    Supports simple dotted paths like `{student.name}`.
    """
    # Find all `{...}` blocks
    matches = re.findall(r"\{([^{}]+)\}", template)
    attrs = set()
    for expr in matches:
        # Only consider simple attribute access (no function calls, etc.)
        parts = expr.split(".")
        if len(parts) == 2 and parts[0] == "student":
            attrs.add(parts[1])
    return attrs

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a formatted student profile from the given template.

    Parameters
    ----------
    unique_id : str
        The unique identifier of the student.
    report_template : str
        A format string containing placeholders such as `{student.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the student ID does not exist, or if the template attempts to
        access sensitive attributes (GPA or home_address).
    """
    # Validate existence of student
    student = _STUDENT_DB.get(unique_id)
    if not student:
        raise ValueError(f"Student with ID '{unique_id}' does not exist.")

    # Detect sensitive placeholders
    used_attrs = _extract_placeholders(report_template)
    if SENSITIVE_KEYS & used_attrs:
        sensitive = ", ".join(SENSITIVE_KEYS & used_attrs)
        raise ValueError(f"Template attempts to access sensitive attributes: {sensitive}")

    # Safely format the report
    try:
        return report_template.format(student=student)
    except Exception as exc:
        # Provide a clear error message while avoiding leaking sensitive data
        raise ValueError(f"Failed to format report: {exc}") from exc

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Student Report\n"
#         "---------------\n"
#         "Name: {student.name}\n"
#         "Course: {student.course}\n"
#         "Age: {student.age}\n"
#     )
#     print(build_student_profile("S001", template))