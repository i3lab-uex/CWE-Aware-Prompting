from dataclasses import dataclass
import re

# ------------------------------
# Sample in‑memory database of students
# ------------------------------

@dataclass(frozen=True)
class Student:
    """Immutable representation of a student."""
    unique_id: str
    name: str
    course: str
    age: int
    gpa: float          # sensitive
    home_address: str   # sensitive
    discipline_record: str

# Dummy data store
_STUDENT_DB = {
    "S001": Student(
        unique_id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.9,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        unique_id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        gpa=3.7,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission in 2023"
    ),
}

# ------------------------------
# Core function
# ------------------------------

def build_student_profile(unique_id: str, report_template: str) -> str:
    """
    Generate a student profile report using the provided template.

    Args:
        unique_id (str): The student's unique identifier.
        report_template (str): A format string containing placeholders
                               such as '{student.name}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the unique_id is unknown, or if the template
                    attempts to access sensitive attributes.
    """
    # Retrieve student record; raise error if not found
    student = _STUDENT_DB.get(unique_id)
    if student is None:
        raise ValueError(f"Student with ID '{unique_id}' not found.")

    # Define sensitive attributes that must not be exposed
    SENSITIVE_FIELDS = {"gpa", "home_address"}

    # Detect any attempt to access sensitive data in the template
    placeholders = re.findall(r"\{[^}]*\}", report_template)
    for ph in placeholders:
        # Strip surrounding braces
        expr = ph[1:-1].strip()
        # Only consider expressions of the form 'student.<attr>'
        if expr.startswith("student."):
            attr = expr.split(".", 1)[1]
            if attr in SENSITIVE_FIELDS:
                raise ValueError(
                    f"Template attempts to access sensitive attribute '{attr}'."
                )

    # Render the report
    try:
        return report_template.format(student=student)
    except Exception as e:
        # Wrap any formatting errors
        raise ValueError(f"Failed to format report: {e}") from e

# ------------------------------
# Example usage (for testing)
# ------------------------------

if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "--------------\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
    )
    print(build_student_profile("S001", tmpl))