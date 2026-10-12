import re
from typing import Dict

# --------------------------------------------------------------------
# Mock definitions (replace with real imports in production)
# --------------------------------------------------------------------

class Student:
    """A simple data holder for student information."""
    def __init__(self, id: str, name: str, course: str,
                 age: int, gpa: float,
                 home_address: str, discipline_record: str):
        self.id = id
        self.name = name
        self.course = course
        self.age = age
        self.gpa = gpa
        self.home_address = home_address          # Sensitive
        self.discipline_record = discipline_record  # Sensitive

class StudentRepository:
    """Simulates a repository that yields Student objects as a context manager."""
    _db: Dict[str, Student] = {
        "S001": Student("S001", "Alice Smith", "Computer Science",
                        20, 3.8,
                        "123 Main St, Springfield", ""),
        "S002": Student("S002", "Bob Johnson", "Mathematics",
                        22, 3.5,
                        "456 Oak Ave, Shelbyville", "Late submission of assignment"),
    }

    @classmethod
    def get_student(cls, student_id: str):
        """Return a Student object if exists; otherwise raise KeyError."""
        try:
            return cls._db[student_id]
        except KeyError as exc:
            raise ValueError(f"Student with ID '{student_id}' not found.") from exc

# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

ALLOWED_FIELDS = {"name", "course", "age", "gpa"}
SENSITIVE_FIELDS = {"home_address", "discipline_record"}

PLACEHOLDER_RE = re.compile(r"\{student\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str):
    """Return a set of placeholder field names found in the template."""
    return set(PLACEHOLDER_RE.findall(template))

def _validate_placeholders(fields: set):
    """Ensure no sensitive fields are requested."""
    for field in fields:
        if field in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field}' is not allowed.")
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Unknown or unsupported field '{field}'.")

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def generate_student_report(student_id: str, template: str) -> str:
    """
    Generate a student report string by applying the provided template
    to the data of the specified student.

    Parameters:
        student_id (str): Unique identifier for the student.
        template (str): Template string containing placeholders like
                        '{student.name}' or '{student.course}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the student cannot be found, if the template
                    contains disallowed fields, or if an error occurs.
    """
    # 1. Retrieve student data (resource acquisition)
    try:
        student = StudentRepository.get_student(student_id)
    except ValueError as exc:
        raise  # Re‑raise with the same message

    # 2. Validate placeholders
    placeholders = _extract_placeholders(template)
    try:
        _validate_placeholders(placeholders)
    except ValueError as exc:
        raise  # Re‑raise with the same message

    # 3. Build a mapping for safe formatting
    mapping = {field: getattr(student, field) for field in placeholders}

    # 4. Perform formatting (no direct eval; safe string interpolation)
    try:
        report = template.format(student=mapping)
    except Exception as exc:  # Catch any formatting errors
        raise ValueError(f"Failed to format template: {exc}") from exc

    # 5. Return the final report
    return report

# --------------------------------------------------------------------
# Example usage (for testing purposes only)
# --------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = ("Student Report\n"
            "Name: {student.name}\n"
            "Course: {student.course}\n"
            "Age: {student.age}\n"
            "GPA: {student.gpa:.2f}")

    try:
        print(generate_student_report("S001", tmpl))
    except ValueError as e:
        print(f"Error: {e}")