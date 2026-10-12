import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Data model
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Student:
    id: str
    name: str
    course: str
    age: int
    gpa: float = field(repr=False)          # Sensitive
    home_address: str = field(repr=False)   # Sensitive
    discipline_record: str = ""

# ------------------------------------------------------------------
# In‑memory registry of students (for demo purposes)
# ------------------------------------------------------------------
_student_registry: Dict[str, Student] = {}

def register_student(student: Student) -> None:
    """Add a student to the registry."""
    _student_registry[student.id] = student

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
_SENSITIVE_FIELDS = {"gpa", "home_address"}

_PLACEHOLDER_RE = re.compile(r"{\s*student\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _validate_placeholders(template: str) -> None:
    """Ensure the template does not reference sensitive fields."""
    for match in _PLACEHOLDER_RE.finditer(template):
        field_name = match.group(1)
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(
                f"Template references sensitive attribute '{field_name}'. "
                "Access to this data is prohibited."
            )

def _render_template(template: str, student: Student) -> str:
    """Render the template with allowed fields."""
    def replacer(match):
        field_name = match.group(1)
        # All other fields are safe to expose
        return str(getattr(student, field_name))
    return _PLACEHOLDER_RE.sub(replacer, template)

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_student_summary(id: str, format_string: str) -> str:
    """
    Generate a student report based on the provided template.

    Parameters
    ----------
    id : str
        Unique identifier of the student.
    format_string : str
        Template containing placeholders like '{student.name}'.

    Returns
    -------
    str
        Rendered report string.

    Raises
    ------
    ValueError
        If the student ID is unknown or if the template references
        sensitive attributes (GPA, home address).
    """
    # Validate that the student exists
    student = _student_registry.get(id)
    if not student:
        raise ValueError(f"Student with id '{id}' does not exist.")

    # Ensure the template is safe
    _validate_placeholders(format_string)

    # Render and return
    return _render_template(format_string, student)


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Create sample students
    alice = Student(
        id="S001",
        name="Alice Smith",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Maple St",
        discipline_record="None"
    )
    bob = Student(
        id="S002",
        name="Bob Johnson",
        course="Mathematics",
        age=22,
        gpa=3.5,
        home_address="456 Oak Ave",
        discipline_record="Late submission"
    )

    # Register them
    register_student(alice)
    register_student(bob)

    # Define a safe template
    tmpl = (
        "Student Report:\n"
        "Name: {student.name}\n"
        "Course: {student.course}\n"
        "Age: {student.age}\n"
    )

    # Generate report
    print(create_student_summary("S001", tmpl))

    # Attempt to use a sensitive field (will raise ValueError)
    try:
        bad_tmpl = "GPA: {student.gpa}"
        print(create_student_summary("S001", bad_tmpl))
    except ValueError as e:
        print(f"Error: {e}")