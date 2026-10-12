import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Data model
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    """Represents a student record."""
    student_id: str
    name: str
    course: str
    age: int
    GPA: float
    home_address: str = field(repr=False)  # sensitive
    discipline_record: str = field(repr=False)  # sensitive


# ------------------------------------------------------------------
# In‑memory datastore (for demonstration purposes)
# ------------------------------------------------------------------
_STUDENTS_DB: Dict[str, Student] = {
    "S001": Student(
        student_id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Townsville",
        discipline_record="None",
    ),
    "S002": Student(
        student_id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Villageton",
        discipline_record="Late submission of assignment #3",
    ),
}


# ------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------
def _get_student_by_id(student_id: str) -> Student:
    """
    Retrieve a student from the datastore.

    Raises:
        ValueError: If the student does not exist.
    """
    try:
        return _STUDENTS_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with ID '{student_id}' not found.") from exc


def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholders of the form {student.field} from a template string.

    Returns:
        A set of field names found in the template.
    """
    pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    return set(pattern.findall(template))


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a report string for the given student based on the supplied template.

    The template may contain placeholders like `{student.name}` or
    `{student.course}`. Only non‑sensitive fields are allowed.

    Args:
        student_id: The unique identifier of the student.
        template: A string containing placeholders.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the student is not found, or if the template contains
                    disallowed placeholders (e.g., sensitive data).
    """
    # Allowed fields – we deliberately exclude sensitive ones.
    ALLOWED_FIELDS = {"name", "course", "age", "GPA"}

    # Retrieve student record
    student = _get_student_by_id(student_id)

    # Validate placeholders
    placeholders = _extract_placeholders(template)
    disallowed = placeholders - ALLOWED_FIELDS
    if disallowed:
        raise ValueError(
            f"Template contains disallowed placeholders: {', '.join(disallowed)}"
        )

    # Build a mapping of allowed attributes
    context = {field: getattr(student, field) for field in ALLOWED_FIELDS}

    # Perform safe formatting
    try:
        report = template.format(student=context)
    except KeyError as exc:
        raise ValueError(f"Missing placeholder in template: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to format template: {exc}") from exc

    return report


# ------------------------------------------------------------------
# Example usage (for manual testing only)
# ------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA}"
    )
    print(generate_student_report("S001", tmpl))