import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Student data model
# ----------------------------------------------------------------------
@dataclass
class Student:
    """Represents a student in the system."""
    id: str          # Unique identifier
    name: str
    course: str
    age: int
    GPA: float
    home_address: str
    discipline_record: str

# ----------------------------------------------------------------------
# In‑memory database (for demo purposes)
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "S001": Student(
        id="S001",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        GPA=3.8,
        home_address="123 Maple St, Springfield",
        discipline_record="None"
    ),
    "S002": Student(
        id="S002",
        name="Bob Smith",
        course="Mathematics",
        age=22,
        GPA=3.5,
        home_address="456 Oak Ave, Shelbyville",
        discipline_record="Late submission of Assignment 3"
    ),
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_student_by_id(student_id: str) -> Student:
    """
    Retrieve a student from the database.

    Raises:
        ValueError: If the student_id is not found.
    """
    try:
        return _STUDENT_DB[student_id]
    except KeyError as exc:
        raise ValueError(f"Student with id '{student_id}' not found.") from exc

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report based on the provided template.

    The template may contain placeholders like `{student.name}` or
    `{student.course}`. Only a predefined set of fields are allowed to be
    interpolated; any attempt to access disallowed attributes raises a
    ValueError.

    Args:
        student_id: The unique identifier of the student.
        template:   A string containing placeholders.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the student_id is invalid, or if the template
                    references disallowed fields.
    """
    # 1. Retrieve student data
    student = _get_student_by_id(student_id)

    # 2. Allowed fields for interpolation
    allowed_fields = {
        "name",
        "course",
        "age",
        "GPA",
        "home_address",
        "discipline_record",
    }

    # 3. Regex to find placeholders like {student.field}
    placeholder_pattern = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def _replace_placeholder(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in allowed_fields:
            raise ValueError(f"Disallowed field '{field_name}' accessed in template.")
        # Use getattr to fetch the value
        value = getattr(student, field_name)
        return str(value)

    # 4. Perform substitution
    try:
        report = placeholder_pattern.sub(_replace_placeholder, template)
    except ValueError as exc:
        # Re‑raise with a clear message
        raise ValueError(f"Template processing error: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Student Report\n"
        "==============\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
        "GPA: {student.GPA:.2f}\n"
        "Address: {student.home_address}\n"
        "Discipline Record: {student.discipline_record}"
    )
    print(generate_student_report("S001", tmpl))