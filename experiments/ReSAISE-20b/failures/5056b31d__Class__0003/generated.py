import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Data model (in a real system this would be replaced by ORM or DB access)
# ----------------------------------------------------------------------
@dataclass
class Student:
    student_id: str
    name: str
    course: str
    age: int
    gpa: float
    home_address: str  # sensitive
    discipline_record: Dict[str, Any]  # sensitive


# ----------------------------------------------------------------------
# In‑memory "database" for demonstration purposes
# ----------------------------------------------------------------------
_STUDENT_DB: Dict[str, Student] = {
    "s123": Student(
        student_id="s123",
        name="Alice Johnson",
        course="Computer Science",
        age=20,
        gpa=3.8,
        home_address="123 Main St, Springfield",
        discipline_record={"probation": False},
    ),
    # Add more students as needed
}


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _get_student_by_id(student_id: str) -> Student:
    """Retrieve a student object or raise ValueError."""
    student = _STUDENT_DB.get(student_id)
    if not student:
        raise ValueError(f"Student with ID '{student_id}' not found.")
    return student


def _extract_template_fields(template: str) -> set:
    """
    Extract all field names from a format string.
    Supports nested attributes (e.g., student.name).
    """
    # Regex to find {field} patterns
    pattern = r"{([^{}]+)}"
    fields = re.findall(pattern, template)
    return set(fields)


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report based on the provided template.

    Args:
        student_id: Unique identifier of the student.
        template: Format string that may contain placeholders like
                  '{student.name}', '{student.course}'.

    Returns:
        A string with the placeholders replaced by actual student data.

    Raises:
        ValueError: If the student is not found, if the template references
                    disallowed attributes, or if any other error occurs.
    """
    # Step 1: Retrieve student data
    try:
        student = _get_student_by_id(student_id)
    except Exception as exc:
        raise ValueError(f"Failed to retrieve student data: {exc}") from exc

    # Step 2: Validate template fields
    allowed_attrs = {"name", "course", "age", "gpa"}
    template_fields = _extract_template_fields(template)

    for field in template_fields:
        # Expecting 'student.<attr>' format
        if not field.startswith("student."):
            raise ValueError(f"Unsupported placeholder '{field}'. Only 'student.<attr>' allowed.")
        attr = field.split(".", 1)[1]
        if attr not in allowed_attrs:
            raise ValueError(f"Access to sensitive attribute '{attr}' is denied.")

    # Step 3: Render the report
    try:
        report = template.format(student=student)
    except Exception as exc:
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Student: {student.name}\nCourse: {student.course}\nAge: {student.age}\nGPA: {student.gpa}"
#     print(generate_student_report("s123", tmpl))